class FrontendController < ApplicationController
  def index
    # Serve the frontend application
    # For now, we'll serve a simple API documentation page
    
    api_info = {
      name: "NLP Platform Rails API",
      version: "1.0.0",
      description: "Advanced Natural Language Processing API built with Ruby on Rails",
      base_url: request.base_url,
      endpoints: {
        nlp: {
          sentiment: "POST /api/v1/sentiment",
          classification: "POST /api/v1/classification", 
          ner: "POST /api/v1/ner",
          summarization: "POST /api/v1/summarization",
          qa: "POST /api/v1/qa",
          attention: "POST /api/v1/attention"
        },
        system: {
          health: "GET /api/v1/health",
          models_status: "GET /api/v1/models/status",
          models_list: "GET /api/v1/models/list",
          clear_cache: "POST /api/v1/models/clear_cache"
        }
      },
      documentation: {
        swagger_url: "#{request.base_url}/api/docs",
        examples: {
          sentiment_analysis: {
            url: "#{request.base_url}/api/v1/sentiment",
            method: "POST",
            body: {
              text: "I love this amazing product!",
              model_name: "default"
            }
          },
          text_classification: {
            url: "#{request.base_url}/api/v1/classification",
            method: "POST", 
            body: {
              text: "This is a great software development article",
              labels: ["technology", "business", "sports", "politics"]
            }
          },
          named_entity_recognition: {
            url: "#{request.base_url}/api/v1/ner",
            method: "POST",
            body: {
              text: "John Smith works at Apple Inc in New York."
            }
          }
        }
      },
      timestamp: Time.current.iso8601
    }
    
    render json: api_info, status: :ok
  end
end
