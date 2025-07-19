module Api
  module V1
    class HealthController < ApplicationController
      def check
        nlp_processor = NlpProcessor.instance
        
        health_data = {
          status: 'healthy',
          timestamp: Time.current.iso8601,
          services: {
            nlp_processor: 'running',
            models_loaded: nlp_processor.get_loaded_models.length,
            memory_usage: get_memory_usage
          },
          version: '1.0.0',
          uptime: get_uptime
        }
        
        render_success(health_data, 'System is healthy')
      end
      
      private
      
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
      
      def get_uptime
        if File.exist?('/proc/uptime')
          uptime_seconds = File.read('/proc/uptime').split.first.to_f
          hours = (uptime_seconds / 3600).to_i
          minutes = ((uptime_seconds % 3600) / 60).to_i
          "#{hours}h #{minutes}m"
        else
          'unavailable'
        end
      end
    end
  end
end
