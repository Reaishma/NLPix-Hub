from app import db
from datetime import datetime
import json

class NLPTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_type = db.Column(db.String(100), nullable=False)
    input_text = db.Column(db.Text, nullable=False)
    model_name = db.Column(db.String(200), nullable=False)
    results = db.Column(db.Text)  # JSON string
    attention_data = db.Column(db.Text)  # JSON string for attention weights
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processing_time = db.Column(db.Float)
    
    def get_results_dict(self):
        return json.loads(self.results) if self.results else {}
    
    def set_results_dict(self, results_dict):
        self.results = json.dumps(results_dict)
    
    def get_attention_dict(self):
        return json.loads(self.attention_data) if self.attention_data else {}
    
    def set_attention_dict(self, attention_dict):
        self.attention_data = json.dumps(attention_dict)

class ModelMetrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(200), nullable=False)
    task_type = db.Column(db.String(100), nullable=False)
    avg_processing_time = db.Column(db.Float)
    accuracy_score = db.Column(db.Float)
    total_requests = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
