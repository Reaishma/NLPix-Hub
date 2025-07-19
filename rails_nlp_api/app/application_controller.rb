class ApplicationController < ActionController::API
  protect_from_forgery with: :null_session
  
  private
  
  def render_success(data, message = 'Success')
    render json: {
      status: 'success',
      message: message,
      data: data,
      timestamp: Time.current.iso8601
    }
  end
  
  def render_error(message, status = :bad_request)
    render json: {
      status: 'error',
      message: message,
      timestamp: Time.current.iso8601
    }, status: status
  end
  
  def measure_processing_time
    start_time = Time.current
    result = yield
    processing_time = ((Time.current - start_time) * 1000).round(2)
    
    if result.is_a?(Hash)
      result[:processing_time_ms] = processing_time
    end
    
    result
  end
end
