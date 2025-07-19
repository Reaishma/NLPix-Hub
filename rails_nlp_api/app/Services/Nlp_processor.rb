require 'singleton'
require 'json'

class NlpProcessor
  include Singleton
  
  def initialize
    @device = 'cpu'
    @models = {}
    @tokenizers = {}
    @pipelines = {}
    
    load_mock_models
    Rails.logger.info "Mock NLP models initialized successfully"
  end
  
  def analyze_sentiment(text, model_name = nil)
    # Mock sentiment analysis based on simple keyword detection
    positive_words = %w[good great excellent amazing wonderful fantastic love like happy best]
    negative_words = %w[bad terrible awful hate dislike sad worst horrible angry]
    
    text_lower = text.downcase
    pos_score = positive_words.count { |word| text_lower.include?(word) }
    neg_score = negative_words.count { |word| text_lower.include?(word) }
    
    if pos_score > neg_score
      sentiment = 'POSITIVE'
      score = [0.9, 0.6 + (pos_score * 0.1)].min
    elsif neg_score > pos_score
      sentiment = 'NEGATIVE'
      score = [0.9, 0.6 + (neg_score * 0.1)].min
    else
      sentiment = 'NEUTRAL'
      score = 0.5 + rand(-0.1..0.1)
    end
    
    results = [{ label: sentiment, score: score }]
    attention_weights = generate_mock_attention(text)
    
    {
      task: 'sentiment_analysis',
      predictions: results,
      model_used: model_name || "cardiffnlp/twitter-roberta-base-sentiment-latest",
      attention_weights: attention_weights
    }
  end
  
  def classify_text(text, model_name = nil, labels = [])
    labels = ["positive", "negative", "neutral", "business", "technology", "sports", "politics"] if labels.empty?
    
    text_lower = text.downcase
    scores = labels.map do |label|
      case label.downcase
      when 'business'
        0.1 + (%w[company business profit market money].any? { |word| text_lower.include?(word) } ? 0.5 : 0)
      when 'technology'
        0.1 + (%w[tech computer software ai digital].any? { |word| text_lower.include?(word) } ? 0.5 : 0)
      when 'sports'
        0.1 + (%w[game sport player team win].any? { |word| text_lower.include?(word) } ? 0.5 : 0)
      when 'politics'
        0.1 + (%w[government political election policy].any? { |word| text_lower.include?(word) } ? 0.5 : 0)
      else
        rand(0.1..0.8)
      end
    end
    
    # Normalize scores
    total = scores.sum
    scores = scores.map { |s| s / total }
    
    # Sort by score
    label_scores = labels.zip(scores).sort_by { |_, score| -score }
    
    results = {
      labels: label_scores.map(&:first),
      scores: label_scores.map(&:last)
    }
    
    {
      task: 'text_classification',
      predictions: results,
      model_used: model_name || "facebook/bart-large-mnli",
      labels_used: labels
    }
  end
  
  def named_entity_recognition(text, model_name = nil)
    entities = []
    entities_by_type = {}
    
    # Simple patterns for common entity types
    patterns = {
      'PERSON' => /\b[A-Z][a-z]+ [A-Z][a-z]+\b/,
      'ORG' => /\b(Company|Corp|Inc|LLC|Ltd|University|College)\b/,
      'GPE' => /\b(New York|London|Paris|Tokyo|California|Texas|United States|UK|USA)\b/,
      'DATE' => /\b\d{4}\b|\b\d{1,2}\/\d{1,2}\/\d{4}\b|\b(January|February|March|April|May|June|July|August|September|October|November|December)\b/,
      'MONEY' => /\$\d+|\b\d+\s*(dollars|USD|euros|pounds)\b/
    }
    
    patterns.each do |entity_type, pattern|
      text.scan(pattern) do |match|
        match_data = Regexp.last_match
        entity = {
          entity_group: entity_type,
          word: match_data.to_s,
          start: match_data.begin(0),
          end: match_data.end(0),
          score: rand(0.8..0.95)
        }
        entities << entity
        
        entities_by_type[entity_type] ||= []
        entities_by_type[entity_type] << {
          text: match_data.to_s,
          confidence: entity[:score],
          start: match_data.begin(0),
          end: match_data.end(0)
        }
      end
    end
    
    {
      task: 'named_entity_recognition',
      entities: entities,
      entities_by_type: entities_by_type,
      model_used: model_name || "dbmdz/bert-large-cased-finetuned-conll03-english"
    }
  end
  
  def summarize_text(text, model_name = nil, max_length = 150, min_length = 30)
    sentences = text.split('. ')
    
    summary = if sentences.length <= 2
      text
    else
      "#{sentences.first}. #{sentences.last}"
    end
    
    summary += '.' unless summary.end_with?('.')
    
    words = summary.split
    if words.length > max_length
      summary = words.first(max_length).join(' ') + '...'
    elsif words.length < min_length && sentences.length > 2
      middle_sentence = sentences[sentences.length / 2]
      summary = "#{sentences.first}. #{middle_sentence}. #{sentences.last}"
    end
    
    {
      task: 'text_summarization',
      summary: summary,
      original_length: text.split.length,
      summary_length: summary.split.length,
      compression_ratio: summary.split.length.to_f / text.split.length,
      model_used: model_name || "facebook/bart-large-cnn"
    }
  end
  
  def question_answering(question, context, model_name = nil)
    question_lower = question.downcase
    context_sentences = context.split('. ')
    
    best_sentence = ""
    best_score = 0
    start_pos = 0
    end_pos = 0
    
    question_words = question.split.select { |word| word.length > 2 }.map(&:downcase)
    
    context_sentences.each do |sentence|
      sentence_lower = sentence.downcase
      score = question_words.count { |word| sentence_lower.include?(word) }
      
      if score > best_score
        best_score = score
        best_sentence = sentence.strip
        start_pos = context.index(sentence) || 0
        end_pos = start_pos + sentence.length
      end
    end
    
    if best_sentence.empty?
      best_sentence = context_sentences.first || "No answer found"
      start_pos = 0
      end_pos = best_sentence.length
    end
    
    confidence = [0.9, 0.3 + (best_score * 0.1)].min
    
    {
      task: 'question_answering',
      question: question,
      answer: best_sentence,
      confidence: confidence,
      start_position: start_pos,
      end_position: end_pos,
      model_used: model_name || "distilbert-base-cased-distilled-squad"
    }
  end
  
  def get_attention_weights(text, model_name = "bert-base-uncased")
    attention_weights = generate_mock_attention(text)
    
    {
      task: 'attention_analysis',
      text: text,
      attention_weights: attention_weights,
      model_used: model_name
    }
  end
  
  def get_loaded_models
    @models_loaded.map { |task, model_name| "#{task}: #{model_name}" }
  end
  
  def clear_cache
    Rails.logger.info "Mock model cache cleared"
  end
  
  private
  
  def load_mock_models
    @models_loaded = {
      'sentiment' => 'cardiffnlp/twitter-roberta-base-sentiment-latest',
      'classification' => 'facebook/bart-large-mnli',
      'ner' => 'dbmdz/bert-large-cased-finetuned-conll03-english',
      'summarization' => 'facebook/bart-large-cnn',
      'qa' => 'distilbert-base-cased-distilled-squad'
    }
  end
  
  def generate_mock_attention(text)
    words = text.split
    return [] if words.empty?
    
    words = words.first(20) if words.length > 20
    n_words = words.length
    
    attention_matrix = []
    
    n_words.times do |i|
      row = []
      n_words.times do |j|
        attention = if i == j
          rand(0.3..0.8)  # Self-attention tends to be higher
        elsif (i - j).abs == 1
          rand(0.2..0.5)  # Adjacent words have moderate attention
        else
          rand(0.05..0.3)  # Distant words have lower attention
        end
        row << attention
      end
      
      # Normalize row to sum to 1
      row_sum = row.sum
      row = row.map { |x| row_sum > 0 ? x / row_sum : 0 }
      attention_matrix << row
    end
    
    attention_matrix
  end
end
