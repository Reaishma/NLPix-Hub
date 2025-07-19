Rails.application.routes.draw do
  namespace :api do
    namespace :v1 do
      # Hugging Face NLP endpoints
      post '/sentiment', to: 'nlp#sentiment_analysis'
      post '/classification', to: 'nlp#text_classification'
      post '/ner', to: 'nlp#named_entity_recognition'
      post '/summarization', to: 'nlp#text_summarization'
      post '/qa', to: 'nlp#question_answering'
      post '/attention', to: 'nlp#attention_analysis'
      
      # Stanford CoreNLP endpoints
      post '/stanford/annotate', to: 'stanford_nlp#annotate'
      
      # Model management
      get '/models/status', to: 'models#status'
      get '/models/list', to: 'models#list'
      post '/models/clear_cache', to: 'models#clear_cache'
      
      # System health
      get '/health', to: 'health#check'
    end
  end
  
  # Serve the frontend from root
  get '/', to: 'frontend#index'
  get '/*path', to: 'frontend#index'
end
