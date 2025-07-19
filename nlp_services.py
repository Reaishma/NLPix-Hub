import re
import random
import logging
from typing import Dict, List, Any, Optional
import os
import json

class NLPProcessor:
    def __init__(self):
        self.device = 'cpu'  # CPU-only for now
        self.models = {}
        self.tokenizers = {}
        self.pipelines = {}
        
        # Initialize mock models for demonstration
        self._load_mock_models()
    
    def _load_mock_models(self):
        """Load mock models for demonstration purposes"""
        try:
            # Initialize mock models status
            self.models_loaded = {
                'sentiment': 'cardiffnlp/twitter-roberta-base-sentiment-latest',
                'classification': 'facebook/bart-large-mnli', 
                'ner': 'dbmdz/bert-large-cased-finetuned-conll03-english',
                'summarization': 'facebook/bart-large-cnn',
                'qa': 'distilbert-base-cased-distilled-squad'
            }
            
            logging.info("Mock models initialized successfully")
            
        except Exception as e:
            logging.error(f"Error loading mock models: {str(e)}")
    
    def analyze_sentiment(self, text: str, model_name: str = None) -> Dict[str, Any]:
        """Analyze sentiment of text (mock implementation)"""
        try:
            # Mock sentiment analysis based on simple keyword detection
            positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'like', 'happy', 'best']
            negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'sad', 'worst', 'horrible', 'angry']
            
            text_lower = text.lower()
            pos_score = sum(1 for word in positive_words if word in text_lower)
            neg_score = sum(1 for word in negative_words if word in text_lower)
            
            if pos_score > neg_score:
                sentiment = 'POSITIVE'
                score = min(0.9, 0.6 + (pos_score * 0.1))
            elif neg_score > pos_score:
                sentiment = 'NEGATIVE' 
                score = min(0.9, 0.6 + (neg_score * 0.1))
            else:
                sentiment = 'NEUTRAL'
                score = 0.5 + random.uniform(-0.1, 0.1)
            
            results = [{'label': sentiment, 'score': score}]
            attention_weights = self._generate_mock_attention(text)
            
            return {
                'task': 'sentiment_analysis',
                'predictions': results,
                'model_used': model_name or "cardiffnlp/twitter-roberta-base-sentiment-latest",
                'attention_weights': attention_weights
            }
            
        except Exception as e:
            logging.error(f"Error in sentiment analysis: {str(e)}")
            raise Exception(f"Sentiment analysis failed: {str(e)}")
    
    def classify_text(self, text: str, model_name: str = None, labels: List[str] = None) -> Dict[str, Any]:
        """Classify text into categories (mock implementation)"""
        try:
            if labels is None:
                labels = ["positive", "negative", "neutral", "business", "technology", "sports", "politics"]
            
            # Mock classification based on keyword matching
            text_lower = text.lower()
            scores = []
            
            for label in labels:
                if label.lower() == 'business':
                    score = 0.1 + (0.5 if any(word in text_lower for word in ['company', 'business', 'profit', 'market', 'money']) else 0)
                elif label.lower() == 'technology':
                    score = 0.1 + (0.5 if any(word in text_lower for word in ['tech', 'computer', 'software', 'ai', 'digital']) else 0)
                elif label.lower() == 'sports':
                    score = 0.1 + (0.5 if any(word in text_lower for word in ['game', 'sport', 'player', 'team', 'win']) else 0)
                elif label.lower() == 'politics':
                    score = 0.1 + (0.5 if any(word in text_lower for word in ['government', 'political', 'election', 'policy']) else 0)
                else:
                    score = random.uniform(0.1, 0.8)
                scores.append(score)
            
            # Normalize scores
            total = sum(scores)
            scores = [s/total for s in scores]
            
            # Sort by score
            label_scores = list(zip(labels, scores))
            label_scores.sort(key=lambda x: x[1], reverse=True)
            
            results = {
                'labels': [item[0] for item in label_scores],
                'scores': [item[1] for item in label_scores]
            }
            
            return {
                'task': 'text_classification',
                'predictions': results,
                'model_used': model_name or "facebook/bart-large-mnli",
                'labels_used': labels
            }
            
        except Exception as e:
            logging.error(f"Error in text classification: {str(e)}")
            raise Exception(f"Text classification failed: {str(e)}")
    
    def named_entity_recognition(self, text: str, model_name: str = None) -> Dict[str, Any]:
        """Extract named entities from text (mock implementation)"""
        try:
            # Mock NER using simple patterns
            entities = []
            entities_by_type = {}
            
            # Simple patterns for common entity types
            patterns = {
                'PERSON': r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',
                'ORG': r'\b(Company|Corp|Inc|LLC|Ltd|University|College)\b',
                'GPE': r'\b(New York|London|Paris|Tokyo|California|Texas|United States|UK|USA)\b',
                'DATE': r'\b\d{4}\b|\b\d{1,2}/\d{1,2}/\d{4}\b|\b(January|February|March|April|May|June|July|August|September|October|November|December)\b',
                'MONEY': r'\$\d+|\b\d+\s*(dollars|USD|euros|pounds)\b'
            }
            
            for entity_type, pattern in patterns.items():
                matches = re.finditer(pattern, text)
                for match in matches:
                    entity = {
                        'entity_group': entity_type,
                        'word': match.group(),
                        'start': match.start(),
                        'end': match.end(),
                        'score': random.uniform(0.8, 0.95)
                    }
                    entities.append(entity)
                    
                    if entity_type not in entities_by_type:
                        entities_by_type[entity_type] = []
                    entities_by_type[entity_type].append({
                        'text': match.group(),
                        'confidence': entity['score'],
                        'start': match.start(),
                        'end': match.end()
                    })
            
            return {
                'task': 'named_entity_recognition',
                'entities': entities,
                'entities_by_type': entities_by_type,
                'model_used': model_name or "dbmdz/bert-large-cased-finetuned-conll03-english"
            }
            
        except Exception as e:
            logging.error(f"Error in NER: {str(e)}")
            raise Exception(f"Named entity recognition failed: {str(e)}")
    
    def summarize_text(self, text: str, model_name: str = None, max_length: int = 150, min_length: int = 30) -> Dict[str, Any]:
        """Summarize text (mock implementation)"""
        try:
            # Simple extractive summarization - pick first and last sentences
            sentences = text.split('. ')
            if len(sentences) <= 2:
                summary = text
            else:
                # Take first sentence and last sentence as summary
                summary = sentences[0] + '. ' + sentences[-1]
                if not summary.endswith('.'):
                    summary += '.'
            
            # Ensure summary meets length requirements
            words = summary.split()
            if len(words) > max_length:
                summary = ' '.join(words[:max_length]) + '...'
            elif len(words) < min_length and len(sentences) > 2:
                # Add middle sentence if too short
                summary = sentences[0] + '. ' + sentences[len(sentences)//2] + '. ' + sentences[-1]
            
            return {
                'task': 'text_summarization',
                'summary': summary,
                'original_length': len(text.split()),
                'summary_length': len(summary.split()),
                'compression_ratio': len(summary.split()) / len(text.split()),
                'model_used': model_name or "facebook/bart-large-cnn"
            }
            
        except Exception as e:
            logging.error(f"Error in text summarization: {str(e)}")
            raise Exception(f"Text summarization failed: {str(e)}")
    
    def question_answering(self, question: str, context: str, model_name: str = None) -> Dict[str, Any]:
        """Answer questions based on context (mock implementation)"""
        try:
            # Simple keyword matching for Q&A
            question_lower = question.lower()
            context_sentences = context.split('. ')
            
            best_sentence = ""
            best_score = 0
            start_pos = 0
            end_pos = 0
            
            # Find sentence with most question keywords
            question_words = [word.lower() for word in question.split() if len(word) > 2]
            
            for sentence in context_sentences:
                sentence_lower = sentence.lower()
                score = sum(1 for word in question_words if word in sentence_lower)
                if score > best_score:
                    best_score = score
                    best_sentence = sentence.strip()
                    start_pos = context.find(sentence)
                    end_pos = start_pos + len(sentence)
            
            if not best_sentence:
                best_sentence = context_sentences[0] if context_sentences else "No answer found"
                start_pos = 0
                end_pos = len(best_sentence)
            
            confidence = min(0.9, 0.3 + (best_score * 0.1))
            
            return {
                'task': 'question_answering',
                'question': question,
                'answer': best_sentence,
                'confidence': confidence,
                'start_position': start_pos,
                'end_position': end_pos,
                'model_used': model_name or "distilbert-base-cased-distilled-squad"
            }
            
        except Exception as e:
            logging.error(f"Error in question answering: {str(e)}")
            raise Exception(f"Question answering failed: {str(e)}")
    
    def get_attention_weights(self, text: str, model_name: str = "bert-base-uncased") -> Dict[str, Any]:
        """Get attention weights from transformer model (mock implementation)"""
        try:
            attention_weights = self._generate_mock_attention(text)
            
            return {
                'task': 'attention_analysis',
                'text': text,
                'attention_weights': attention_weights,
                'model_used': model_name
            }
            
        except Exception as e:
            logging.error(f"Error getting attention weights: {str(e)}")
            raise Exception(f"Attention analysis failed: {str(e)}")
    
    def _generate_mock_attention(self, text: str) -> List[List[float]]:
        """Generate mock attention weights for visualization"""
        try:
            words = text.split()
            if len(words) == 0:
                return []
            
            # Limit to reasonable size for visualization
            if len(words) > 20:
                words = words[:20]
            
            n_words = len(words)
            attention_matrix = []
            
            for i in range(n_words):
                row = []
                for j in range(n_words):
                    if i == j:
                        # Self-attention tends to be higher
                        attention = random.uniform(0.3, 0.8)
                    elif abs(i - j) == 1:
                        # Adjacent words have moderate attention
                        attention = random.uniform(0.2, 0.5)
                    else:
                        # Distant words have lower attention
                        attention = random.uniform(0.05, 0.3)
                    row.append(attention)
                
                # Normalize row to sum to 1
                row_sum = sum(row)
                if row_sum > 0:
                    row = [x / row_sum for x in row]
                attention_matrix.append(row)
            
            return attention_matrix
            
        except Exception as e:
            logging.error(f"Error generating mock attention: {str(e)}")
            return []
    
    def get_loaded_models(self) -> List[str]:
        """Return list of currently loaded models"""
        loaded_models = []
        for task, model_name in self.models_loaded.items():
            loaded_models.append(f"{task}: {model_name}")
        return loaded_models
    
    def clear_cache(self):
        """Clear model cache to free memory"""
        try:
            logging.info("Mock model cache cleared")
        except Exception as e:
            logging.error(f"Error clearing cache: {str(e)}")