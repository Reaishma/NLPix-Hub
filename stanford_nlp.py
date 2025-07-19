import requests
import json
import logging
from typing import Dict, List, Any, Optional
import os

class StanfordNLPProcessor:
    def __init__(self):
        self.server_url = os.environ.get('STANFORD_NLP_URL', 'http://localhost:9000')
        self.timeout = 30
        self.available_annotators = [
            'tokenize', 'ssplit', 'pos', 'lemma', 'ner', 
            'parse', 'depparse', 'coref', 'sentiment', 'relation'
        ]
    
    def is_available(self) -> bool:
        """Check if Stanford CoreNLP server is available"""
        try:
            response = requests.get(f"{self.server_url}/", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def process_text(self, text: str, annotators: List[str] = None) -> Dict[str, Any]:
        """Process text with Stanford CoreNLP"""
        try:
            if not self.is_available():
                return self._mock_stanford_output(text, annotators)
            
            if annotators is None:
                annotators = ['tokenize', 'ssplit', 'pos', 'ner']
            
            # Validate annotators
            valid_annotators = [ann for ann in annotators if ann in self.available_annotators]
            
            # Prepare request
            data = {
                'annotators': ','.join(valid_annotators),
                'outputFormat': 'json',
                'timeout': self.timeout * 1000  # Convert to milliseconds
            }
            
            # Send request
            response = requests.post(
                f"{self.server_url}/?properties={json.dumps(data)}",
                data=text.encode('utf-8'),
                headers={'Content-Type': 'text/plain; charset=utf-8'},
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return self._process_stanford_output(result, valid_annotators)
            else:
                logging.error(f"Stanford NLP request failed: {response.status_code}")
                return self._mock_stanford_output(text, annotators)
                
        except Exception as e:
            logging.error(f"Error in Stanford NLP processing: {str(e)}")
            return self._mock_stanford_output(text, annotators)
    
    def _process_stanford_output(self, raw_output: Dict[str, Any], annotators: List[str]) -> Dict[str, Any]:
        """Process raw Stanford CoreNLP output into structured format"""
        try:
            processed = {
                'annotators_used': annotators,
                'sentences': [],
                'tokens': [],
                'entities': [],
                'dependencies': [],
                'sentiment': None
            }
            
            # Process sentences
            for sentence in raw_output.get('sentences', []):
                sentence_data = {
                    'index': sentence.get('index', 0),
                    'text': ' '.join([token['word'] for token in sentence.get('tokens', [])]),
                    'tokens': [],
                    'parse': sentence.get('parse', ''),
                    'sentiment': sentence.get('sentiment', 'Neutral')
                }
                
                # Process tokens
                for token in sentence.get('tokens', []):
                    token_data = {
                        'index': token.get('index', 0),
                        'word': token.get('word', ''),
                        'lemma': token.get('lemma', ''),
                        'pos': token.get('pos', ''),
                        'ner': token.get('ner', 'O'),
                        'characterOffsetBegin': token.get('characterOffsetBegin', 0),
                        'characterOffsetEnd': token.get('characterOffsetEnd', 0)
                    }
                    sentence_data['tokens'].append(token_data)
                    processed['tokens'].append(token_data)
                
                # Process dependencies
                if 'basicDependencies' in sentence:
                    for dep in sentence['basicDependencies']:
                        if dep['dep'] != 'ROOT':
                            processed['dependencies'].append({
                                'dependent': dep['dependent'],
                                'governor': dep['governor'],
                                'relation': dep['dep'],
                                'dependentGloss': dep['dependentGloss'],
                                'governorGloss': dep['governorGloss']
                            })
                
                processed['sentences'].append(sentence_data)
            
            # Extract named entities
            current_entity = None
            for token in processed['tokens']:
                if token['ner'] != 'O':
                    if current_entity is None or token['ner'] != current_entity['type']:
                        # Start new entity
                        if current_entity:
                            processed['entities'].append(current_entity)
                        current_entity = {
                            'text': token['word'],
                            'type': token['ner'],
                            'start': token['characterOffsetBegin'],
                            'end': token['characterOffsetEnd'],
                            'tokens': [token]
                        }
                    else:
                        # Continue current entity
                        current_entity['text'] += ' ' + token['word']
                        current_entity['end'] = token['characterOffsetEnd']
                        current_entity['tokens'].append(token)
                else:
                    # End current entity
                    if current_entity:
                        processed['entities'].append(current_entity)
                        current_entity = None
            
            # Add final entity if exists
            if current_entity:
                processed['entities'].append(current_entity)
            
            # Overall sentiment (average of sentence sentiments)
            if processed['sentences']:
                sentiment_scores = {'Negative': 0, 'Neutral': 1, 'Positive': 2}
                avg_sentiment = sum(sentiment_scores.get(s['sentiment'], 1) for s in processed['sentences']) / len(processed['sentences'])
                if avg_sentiment < 0.5:
                    processed['sentiment'] = 'Negative'
                elif avg_sentiment > 1.5:
                    processed['sentiment'] = 'Positive'
                else:
                    processed['sentiment'] = 'Neutral'
            
            return processed
            
        except Exception as e:
            logging.error(f"Error processing Stanford output: {str(e)}")
            return {'error': f'Failed to process Stanford output: {str(e)}'}
    
    def _mock_stanford_output(self, text: str, annotators: List[str]) -> Dict[str, Any]:
        """Provide mock output when Stanford CoreNLP is not available"""
        try:
            # Simple tokenization and basic analysis
            sentences = text.split('.')
            words = text.split()
            
            mock_output = {
                'annotators_used': annotators or ['tokenize', 'ssplit'],
                'sentences': [],
                'tokens': [],
                'entities': [],
                'dependencies': [],
                'sentiment': 'Neutral',
                'note': 'Stanford CoreNLP server not available - using mock output'
            }
            
            # Mock sentence processing
            for i, sentence in enumerate(sentences):
                if sentence.strip():
                    sentence_words = sentence.strip().split()
                    mock_output['sentences'].append({
                        'index': i,
                        'text': sentence.strip(),
                        'tokens': [{'word': word, 'pos': 'NN', 'ner': 'O'} for word in sentence_words],
                        'sentiment': 'Neutral'
                    })
            
            # Mock token processing
            for i, word in enumerate(words):
                mock_output['tokens'].append({
                    'index': i + 1,
                    'word': word,
                    'lemma': word.lower(),
                    'pos': 'NN',  # Default to noun
                    'ner': 'O',   # Default to no entity
                    'characterOffsetBegin': 0,
                    'characterOffsetEnd': len(word)
                })
            
            return mock_output
            
        except Exception as e:
            logging.error(f"Error creating mock Stanford output: {str(e)}")
            return {'error': f'Failed to create mock output: {str(e)}'}
    
    def get_dependency_tree(self, text: str) -> Dict[str, Any]:
        """Get dependency parse tree"""
        try:
            result = self.process_text(text, ['tokenize', 'ssplit', 'pos', 'depparse'])
            
            if 'dependencies' in result:
                # Create tree structure
                tree_data = {
                    'nodes': [],
                    'edges': [],
                    'text': text
                }
                
                # Add nodes (tokens)
                for token in result['tokens']:
                    tree_data['nodes'].append({
                        'id': token['index'],
                        'label': token['word'],
                        'pos': token['pos']
                    })
                
                # Add edges (dependencies)
                for dep in result['dependencies']:
                    tree_data['edges'].append({
                        'source': dep['governor'],
                        'target': dep['dependent'],
                        'relation': dep['relation']
                    })
                
                return tree_data
            
            return {'error': 'No dependency information available'}
            
        except Exception as e:
            logging.error(f"Error getting dependency tree: {str(e)}")
            return {'error': f'Failed to get dependency tree: {str(e)}'}
    
    def analyze_coreference(self, text: str) -> Dict[str, Any]:
        """Analyze coreference chains"""
        try:
            result = self.process_text(text, ['tokenize', 'ssplit', 'pos', 'ner', 'coref'])
            
            # Extract coreference information from result
            # This would need the actual Stanford CoreNLP output format
            return {
                'text': text,
                'coreference_chains': [],
                'note': 'Coreference analysis requires Stanford CoreNLP server'
            }
            
        except Exception as e:
            logging.error(f"Error in coreference analysis: {str(e)}")
            return {'error': f'Coreference analysis failed: {str(e)}'}
