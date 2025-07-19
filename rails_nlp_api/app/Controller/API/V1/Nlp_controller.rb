module Api
  module V1
    class NlpController < ApplicationController
      before_action :initialize_nlp_processor
      
      def sentiment_analysis
        text = params[:text]
        model_name = params[:model_name]
        
        if text.blank?
          return render_error('Text parameter is required')
        end
        
        result = measure_processing_time do
          @nlp_processor.analyze_sentiment(text, model_name)
        end
        
        render_success(result, 'Sentiment analysis completed')
        
      rescue => e
        Rails.logger.error "Sentiment analysis error: #{e.message}"
        render_error("Sentiment analysis failed: #{e.message}", :internal_server_error)
      end
      
      def text_classification
        text = params[:text]
        model_name = params[:model_name]
        labels = params[:labels] || []
        
        if text.blank?
          return render_error('Text parameter is required')
        end
        
        result = measure_processing_time do
          @nlp_processor.classify_text(text, model_name, labels)
        end
        
        render_success(result, 'Text classification completed')
        
      rescue => e
        Rails.logger.error "Text classification error: #{e.message}"
        render_error("Text classification failed: #{e.message}", :internal_server_error)
      end
      
      def named_entity_recognition
        text = params[:text]
        model_name = params[:model_name]
        
        if text.blank?
          return render_error('Text parameter is required')
        end
        
        result = measure_processing_time do
          @nlp_processor.named_entity_recognition(text, model_name)
        end
        
        render_success(result, 'Named entity recognition completed')
        
      rescue => e
        Rails.logger.error "NER error: #{e.message}"
        render_error("Named entity recognition failed: #{e.message}", :internal_server_error)
      end
      
      def text_summarization
        text = params[:text]
        model_name = params[:model_name]
        max_length = (params[:max_length] || 150).to_i
        min_length = (params[:min_length] || 30).to_i
        
        if text.blank?
          return render_error('Text parameter is required')
        end
        
        result = measure_processing_time do
          @nlp_processor.summarize_text(text, model_name, max_length, min_length)
        end
        
        render_success(result, 'Text summarization completed')
        
      rescue => e
        Rails.logger.error "Summarization error: #{e.message}"
        render_error("Text summarization failed: #{e.message}", :internal_server_error)
      end
      
      def question_answering
        question = params[:question]
        context = params[:context]
        model_name = params[:model_name]
        
        if question.blank? || context.blank?
          return render_error('Question and context parameters are required')
        end
        
        result = measure_processing_time do
          @nlp_processor.question_answering(question, context, model_name)
        end
        
        render_success(result, 'Question answering completed')
        
      rescue => e
        Rails.logger.error "Q&A error: #{e.message}"
        render_error("Question answering failed: #{e.message}", :internal_server_error)
      end
      
      def attention_analysis
        text = params[:text]
        model_name = params[:model_name] || 'bert-base-uncased'
        
        if text.blank?
          return render_error('Text parameter is required')
        end
        
        result = measure_processing_time do
          @nlp_processor.get_attention_weights(text, model_name)
        end
        
        # Generate attention visualization data
        attention_viz = AttentionVisualizer.new
        heatmap_data = attention_viz.generate_attention_heatmap(text, result[:attention_weights])
        result[:heatmap_data] = heatmap_data
        
        render_success(result, 'Attention analysis completed')
        
      rescue => e
        Rails.logger.error "Attention analysis error: #{e.message}"
        render_error("Attention analysis failed: #{e.message}", :internal_server_error)
      end
      
      private
      
      def initialize_nlp_processor
        @nlp_processor = NlpProcessor.instance
      end
    end
  end
end
