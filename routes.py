from flask import render_template, request, jsonify, flash, redirect, url_for
from app import app, db
from models import NLPTask, ModelMetrics
from nlp_services import NLPProcessor
from attention_utils import AttentionVisualizer
from stanford_nlp import StanfordNLPProcessor
import time
import logging

# Initialize NLP processors
nlp_processor = NLPProcessor()
attention_visualizer = AttentionVisualizer()
stanford_processor = StanfordNLPProcessor()

@app.route('/')
def index():
    """Main page with NLP interface"""
    recent_tasks = NLPTask.query.order_by(NLPTask.created_at.desc()).limit(10).all()
    model_metrics = ModelMetrics.query.all()
    return render_template('index.html', 
                         recent_tasks=recent_tasks, 
                         model_metrics=model_metrics)

@app.route('/analyze', methods=['POST'])
def analyze_text():
    """Process text with selected NLP model"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        task_type = data.get('task_type', 'sentiment')
        model_name = data.get('model_name', 'bert-base-uncased')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        start_time = time.time()
        
        # Process based on task type
        if task_type == 'sentiment':
            results = nlp_processor.analyze_sentiment(text, model_name)
        elif task_type == 'classification':
            results = nlp_processor.classify_text(text, model_name)
        elif task_type == 'ner':
            results = nlp_processor.named_entity_recognition(text, model_name)
        elif task_type == 'summarization':
            results = nlp_processor.summarize_text(text, model_name)
        elif task_type == 'qa':
            context = data.get('context', '')
            results = nlp_processor.question_answering(text, context, model_name)
        elif task_type == 'attention':
            results = nlp_processor.get_attention_weights(text, model_name)
        else:
            return jsonify({'error': 'Unsupported task type'}), 400
        
        processing_time = time.time() - start_time
        
        # Save to database
        task = NLPTask(
            task_type=task_type,
            input_text=text,
            model_name=model_name,
            processing_time=processing_time
        )
        task.set_results_dict(results)
        
        # Generate attention visualization if applicable
        if task_type in ['sentiment', 'classification', 'attention']:
            attention_data = attention_visualizer.generate_attention_heatmap(
                text, results.get('attention_weights', [])
            )
            task.set_attention_dict(attention_data)
        
        db.session.add(task)
        db.session.commit()
        
        # Update model metrics
        update_model_metrics(model_name, task_type, processing_time)
        
        return jsonify({
            'results': results,
            'processing_time': processing_time,
            'task_id': task.id,
            'attention_data': task.get_attention_dict()
        })
        
    except Exception as e:
        logging.error(f"Error in analyze_text: {str(e)}")
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

@app.route('/stanford_nlp', methods=['POST'])
def stanford_nlp_analysis():
    """Process text with Stanford CoreNLP"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        annotators = data.get('annotators', ['tokenize', 'ssplit', 'pos', 'ner'])
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        start_time = time.time()
        results = stanford_processor.process_text(text, annotators)
        processing_time = time.time() - start_time
        
        # Save to database
        task = NLPTask(
            task_type='stanford_nlp',
            input_text=text,
            model_name='stanford-corenlp',
            processing_time=processing_time
        )
        task.set_results_dict(results)
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify({
            'results': results,
            'processing_time': processing_time,
            'task_id': task.id
        })
        
    except Exception as e:
        logging.error(f"Error in stanford_nlp_analysis: {str(e)}")
        return jsonify({'error': f'Stanford NLP processing failed: {str(e)}'}), 500

@app.route('/compare_models', methods=['POST'])
def compare_models():
    """Compare multiple models on the same text"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        models = data.get('models', ['bert-base-uncased', 'roberta-base'])
        task_type = data.get('task_type', 'sentiment')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        results = {}
        for model in models:
            start_time = time.time()
            
            if task_type == 'sentiment':
                model_results = nlp_processor.analyze_sentiment(text, model)
            elif task_type == 'classification':
                model_results = nlp_processor.classify_text(text, model)
            elif task_type == 'ner':
                model_results = nlp_processor.named_entity_recognition(text, model)
            else:
                continue
            
            processing_time = time.time() - start_time
            
            results[model] = {
                'results': model_results,
                'processing_time': processing_time
            }
        
        return jsonify({'comparison': results})
        
    except Exception as e:
        logging.error(f"Error in compare_models: {str(e)}")
        return jsonify({'error': f'Model comparison failed: {str(e)}'}), 500

@app.route('/attention_visualization/<int:task_id>')
def get_attention_visualization(task_id):
    """Get attention visualization data for a specific task"""
    try:
        task = NLPTask.query.get_or_404(task_id)
        attention_data = task.get_attention_dict()
        
        if not attention_data:
            return jsonify({'error': 'No attention data available for this task'}), 404
        
        return jsonify(attention_data)
        
    except Exception as e:
        logging.error(f"Error in get_attention_visualization: {str(e)}")
        return jsonify({'error': f'Failed to get attention visualization: {str(e)}'}), 500

@app.route('/model_metrics')
def get_model_metrics():
    """Get performance metrics for all models"""
    try:
        metrics = ModelMetrics.query.all()
        metrics_data = []
        
        for metric in metrics:
            metrics_data.append({
                'model_name': metric.model_name,
                'task_type': metric.task_type,
                'avg_processing_time': metric.avg_processing_time,
                'accuracy_score': metric.accuracy_score,
                'total_requests': metric.total_requests,
                'last_updated': metric.last_updated.isoformat()
            })
        
        return jsonify({'metrics': metrics_data})
        
    except Exception as e:
        logging.error(f"Error in get_model_metrics: {str(e)}")
        return jsonify({'error': f'Failed to get model metrics: {str(e)}'}), 500

def update_model_metrics(model_name, task_type, processing_time):
    """Update performance metrics for a model"""
    try:
        metric = ModelMetrics.query.filter_by(
            model_name=model_name, 
            task_type=task_type
        ).first()
        
        if metric:
            # Update existing metrics
            total_time = metric.avg_processing_time * metric.total_requests + processing_time
            metric.total_requests += 1
            metric.avg_processing_time = total_time / metric.total_requests
        else:
            # Create new metrics
            metric = ModelMetrics(
                model_name=model_name,
                task_type=task_type,
                avg_processing_time=processing_time,
                total_requests=1
            )
            db.session.add(metric)
        
        db.session.commit()
        
    except Exception as e:
        logging.error(f"Error updating model metrics: {str(e)}")

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': nlp_processor.get_loaded_models(),
        'stanford_nlp_status': stanford_processor.is_available()
    })
