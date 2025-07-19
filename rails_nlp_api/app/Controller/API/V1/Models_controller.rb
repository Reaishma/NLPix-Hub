module Api
  module V1
    class ModelsController < ApplicationController
      before_action :initialize_nlp_processor
      
      def status
        loaded_models = @nlp_processor.get_loaded_models
        
        model_status = {
          models_loaded: loaded_models.length,
          models: loaded_models,
          device: 'cpu',
          memory_usage: get_memory_usage,
          last_updated: Time.current.iso8601
        }
        
        render_success(model_status, 'Model status retrieved')
      end
      
      def list
        available_models = {
          sentiment_analysis: [
            'cardiffnlp/twitter-roberta-base-sentiment-latest',
            'nlptown/bert-base-multilingual-uncased-sentiment',
            'cardiffnlp/twitter-xlm-roberta-base-sentiment'
          ],
          text_classification: [
            'facebook/bart-large-mnli',
            'microsoft/DialoGPT-medium',
            'distilbert-base-uncased-finetuned-sst-2-english'
          ],
          named_entity_recognition: [
            'dbmdz/bert-large-cased-finetuned-conll03-english',
            'xlm-roberta-large-finetuned-conll03-english',
            'dslim/bert-base-NER'
          ],
          text_summarization: [
            'facebook/bart-large-cnn',
            'sshleifer/distilbart-cnn-12-6',
            'google/pegasus-xsum'
          ],
          question_answering: [
            'distilbert-base-cased-distilled-squad',
            'deepset/roberta-base-squad2',
            'bert-large-uncased-whole-word-masking-finetuned-squad'
          ]
        }
        
        render_success(available_models, 'Available models listed')
      end
      
      def clear_cache
        @nlp_processor.clear_cache
        
        cache_status = {
          cache_cleared: true,
          timestamp: Time.current.iso8601,
          message: 'Model cache has been cleared'
        }
        
        render_success(cache_status, 'Model cache cleared successfully')
      end
      
      private
      
      def initialize_nlp_processor
        @nlp_processor = NlpProcessor.instance
      end
      
      def get_memory_usage
        if File.exist?('/proc/self/status')
          status = File.read('/proc/self/status')
          if match = status.match(/VmRSS:\s*(\d+)\s*kB/)
            "#{match[1].to_i / 1024} MB"
          else
            'unknown'
          end
        else
          'unavailable'
        end
      end
    end
  end
end
