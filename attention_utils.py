import random
import math
from typing import List, Dict, Any, Tuple
import logging

class AttentionVisualizer:
    def __init__(self):
        self.color_map = 'Blues'
    
    def generate_attention_heatmap(self, text: str, attention_weights: List[List[float]]) -> Dict[str, Any]:
        """Generate attention heatmap data for visualization"""
        try:
            if not attention_weights:
                return {'error': 'No attention weights provided'}
            
            # Tokenize text (simple whitespace tokenization)
            tokens = text.split()
            
            # Ensure matrix dimensions match tokens
            if len(attention_weights) != len(tokens):
                # Truncate or pad as needed
                if len(attention_weights) > len(tokens):
                    attention_weights = attention_weights[:len(tokens)]
                    for i in range(len(attention_weights)):
                        attention_weights[i] = attention_weights[i][:len(tokens)]
                else:
                    # Pad with zeros
                    pad_size = len(tokens) - len(attention_weights)
                    for i in range(pad_size):
                        attention_weights.append([0.0] * len(tokens))
                    for i in range(len(attention_weights)):
                        while len(attention_weights[i]) < len(tokens):
                            attention_weights[i].append(0.0)
            
            # Calculate min/max values
            flat_weights = [weight for row in attention_weights for weight in row]
            max_attention = max(flat_weights) if flat_weights else 1.0
            min_attention = min(flat_weights) if flat_weights else 0.0
            avg_attention = sum(flat_weights) / len(flat_weights) if flat_weights else 0.0
            
            # Generate heatmap data
            heatmap_data = {
                'tokens': tokens,
                'attention_matrix': attention_weights,
                'max_attention': max_attention,
                'min_attention': min_attention,
                'avg_attention': avg_attention
            }
            
            # Generate token-level attention scores
            token_scores = self._calculate_token_importance(attention_weights)
            heatmap_data['token_importance'] = token_scores
            
            return heatmap_data
            
        except Exception as e:
            logging.error(f"Error generating attention heatmap: {str(e)}")
            return {'error': f'Failed to generate heatmap: {str(e)}'}
    
    def _calculate_token_importance(self, attention_matrix: List[List[float]]) -> List[Dict[str, float]]:
        """Calculate importance scores for each token"""
        try:
            if not attention_matrix:
                return []
            
            n_tokens = len(attention_matrix)
            token_scores = []
            
            for i in range(n_tokens):
                # Sum attention weights for each token (both as source and target)
                incoming_attention = sum(attention_matrix[j][i] for j in range(n_tokens))
                outgoing_attention = sum(attention_matrix[i])
                
                # Normalize scores
                max_incoming = max(sum(attention_matrix[j][k] for j in range(n_tokens)) for k in range(n_tokens))
                max_outgoing = max(sum(row) for row in attention_matrix)
                
                incoming_normalized = incoming_attention / max_incoming if max_incoming > 0 else 0
                outgoing_normalized = outgoing_attention / max_outgoing if max_outgoing > 0 else 0
                
                # Combine scores
                combined_score = (incoming_normalized + outgoing_normalized) / 2
                
                token_scores.append({
                    'index': i,
                    'importance': combined_score,
                    'incoming_attention': incoming_normalized,
                    'outgoing_attention': outgoing_normalized
                })
            
            return token_scores
            
        except Exception as e:
            logging.error(f"Error calculating token importance: {str(e)}")
            return []
    
    def analyze_attention_patterns(self, attention_matrix: List[List[float]], tokens: List[str]) -> Dict[str, Any]:
        """Analyze attention patterns and provide insights"""
        try:
            if not attention_matrix or not tokens:
                return {'error': 'No attention matrix or tokens provided'}
            
            analysis = {}
            n_tokens = len(tokens)
            
            # Find tokens with highest self-attention
            self_attention = [attention_matrix[i][i] for i in range(min(n_tokens, len(attention_matrix)))]
            high_self_attention_indices = sorted(range(len(self_attention)), key=lambda i: self_attention[i], reverse=True)[:3]
            analysis['high_self_attention'] = [
                {'token': tokens[i], 'score': self_attention[i]}
                for i in high_self_attention_indices if i < len(tokens)
            ]
            
            # Find most influential tokens (highest outgoing attention)
            outgoing_attention = [sum(row) for row in attention_matrix]
            most_influential_indices = sorted(range(len(outgoing_attention)), key=lambda i: outgoing_attention[i], reverse=True)[:3]
            analysis['most_influential'] = [
                {'token': tokens[i], 'total_attention': outgoing_attention[i]}
                for i in most_influential_indices if i < len(tokens)
            ]
            
            # Find most attended tokens (highest incoming attention)
            incoming_attention = [sum(attention_matrix[j][i] for j in range(len(attention_matrix))) for i in range(n_tokens)]
            most_attended_indices = sorted(range(len(incoming_attention)), key=lambda i: incoming_attention[i], reverse=True)[:3]
            analysis['most_attended'] = [
                {'token': tokens[i], 'total_attention': incoming_attention[i]}
                for i in most_attended_indices if i < len(tokens)
            ]
            
            # Calculate attention diversity (simplified entropy)
            attention_entropy = []
            for i in range(len(attention_matrix)):
                row = attention_matrix[i]
                row_sum = sum(row)
                if row_sum > 0:
                    # Normalize row
                    row_normalized = [x / row_sum for x in row]
                    # Calculate entropy
                    entropy = -sum(p * math.log(p + 1e-10) for p in row_normalized if p > 0)
                    attention_entropy.append(entropy)
                else:
                    attention_entropy.append(0)
            
            if attention_entropy:
                analysis['attention_diversity'] = {
                    'mean_entropy': sum(attention_entropy) / len(attention_entropy),
                    'max_entropy': max(attention_entropy),
                    'min_entropy': min(attention_entropy)
                }
            
            return analysis
            
        except Exception as e:
            logging.error(f"Error analyzing attention patterns: {str(e)}")
            return {'error': f'Analysis failed: {str(e)}'}