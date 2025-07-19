class AttentionVisualizer
  def initialize
    @color_map = 'Blues'
  end
  
  def generate_attention_heatmap(text, attention_weights)
    return { error: 'No attention weights provided' } if attention_weights.empty?
    
    tokens = text.split
    
    # Ensure matrix dimensions match tokens
    if attention_weights.length != tokens.length
      if attention_weights.length > tokens.length
        attention_weights = attention_weights.first(tokens.length)
        attention_weights = attention_weights.map { |row| row.first(tokens.length) }
      else
        pad_size = tokens.length - attention_weights.length
        pad_size.times do
          attention_weights << Array.new(tokens.length, 0.0)
        end
        attention_weights.each do |row|
          while row.length < tokens.length
            row << 0.0
          end
        end
      end
    end
    
    # Calculate min/max values
    flat_weights = attention_weights.flatten
    max_attention = flat_weights.empty? ? 1.0 : flat_weights.max
    min_attention = flat_weights.empty? ? 0.0 : flat_weights.min
    avg_attention = flat_weights.empty? ? 0.0 : flat_weights.sum / flat_weights.length
    
    # Generate heatmap data
    heatmap_data = {
      tokens: tokens,
      attention_matrix: attention_weights,
      max_attention: max_attention,
      min_attention: min_attention,
      avg_attention: avg_attention
    }
    
    # Generate token-level attention scores
    token_scores = calculate_token_importance(attention_weights)
    heatmap_data[:token_importance] = token_scores
    
    heatmap_data
  end
  
  def analyze_attention_patterns(attention_matrix, tokens)
    return { error: 'No attention matrix or tokens provided' } if attention_matrix.empty? || tokens.empty?
    
    analysis = {}
    n_tokens = tokens.length
    
    # Find tokens with highest self-attention
    self_attention = (0...n_tokens).map { |i| attention_matrix[i][i] }
    high_self_attention_indices = self_attention.each_with_index.sort_by { |val, _| -val }.first(3).map(&:last)
    
    analysis[:high_self_attention] = high_self_attention_indices.map do |i|
      { token: tokens[i], score: self_attention[i] }
    end
    
    # Find most influential tokens (highest outgoing attention)
    outgoing_attention = attention_matrix.map(&:sum)
    most_influential_indices = outgoing_attention.each_with_index.sort_by { |val, _| -val }.first(3).map(&:last)
    
    analysis[:most_influential] = most_influential_indices.map do |i|
      { token: tokens[i], total_attention: outgoing_attention[i] }
    end
    
    # Find most attended tokens (highest incoming attention)
    incoming_attention = (0...n_tokens).map do |i|
      attention_matrix.sum { |row| row[i] }
    end
    most_attended_indices = incoming_attention.each_with_index.sort_by { |val, _| -val }.first(3).map(&:last)
    
    analysis[:most_attended] = most_attended_indices.map do |i|
      { token: tokens[i], total_attention: incoming_attention[i] }
    end
    
    # Calculate attention diversity (simplified entropy)
    attention_entropy = attention_matrix.map do |row|
      row_sum = row.sum
      if row_sum > 0
        row_normalized = row.map { |x| x / row_sum }
        -row_normalized.sum { |p| p > 0 ? p * Math.log(p + 1e-10) : 0 }
      else
        0
      end
    end
    
    unless attention_entropy.empty?
      analysis[:attention_diversity] = {
        mean_entropy: attention_entropy.sum / attention_entropy.length,
        max_entropy: attention_entropy.max,
        min_entropy: attention_entropy.min
      }
    end
    
    analysis
  end
  
  private
  
  def calculate_token_importance(attention_matrix)
    return [] if attention_matrix.empty?
    
    n_tokens = attention_matrix.length
    token_scores = []
    
    n_tokens.times do |i|
      # Sum attention weights for each token (both as source and target)
      incoming_attention = attention_matrix.sum { |row| row[i] }
      outgoing_attention = attention_matrix[i].sum
      
      # Normalize scores
      max_incoming = (0...n_tokens).map { |k| attention_matrix.sum { |row| row[k] } }.max
      max_outgoing = attention_matrix.map(&:sum).max
      
      incoming_normalized = max_incoming > 0 ? incoming_attention / max_incoming : 0
      outgoing_normalized = max_outgoing > 0 ? outgoing_attention / max_outgoing : 0
      
      # Combine scores
      combined_score = (incoming_normalized + outgoing_normalized) / 2
      
      token_scores << {
        index: i,
        importance: combined_score,
        incoming_attention: incoming_normalized,
        outgoing_attention: outgoing_normalized
      }
    end
    
    token_scores
  end
end
