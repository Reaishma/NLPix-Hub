# NLP Platform 

## Overview

This is a comprehensive Natural Language Processing (NLP) platform that provides both Flask Python Backend and Ruby on Rails API Backend implementations. The platform integrates multiple AI/ML frameworks including  implementations of Hugging Face Transformers, Stanford CoreNLP, and attention visualization systems. The platform provides both web-based interface and REST API endpoints for various NLP tasks such as sentiment analysis, text classification, named entity recognition, summarization, question answering, and attention visualization.

## Live Demo 

[View Live Demo](https://reaishma.github.io/NLPix-Hub/)

## System Architecture

### Dual Backend Architecture

#### Flask Python Backend (Primary - Port 5000)
- **Framework**: Flask web application with SQLAlchemy ORM
- **Database**: SQLite for development (configurable to PostgreSQL via DATABASE_URL)
- **Models**: Two main entities - NLPTask for storing analysis results and ModelMetrics for performance tracking
- **Session Management**: Flask sessions with configurable secret key
- **Endpoints**: Web interface + `/analyze` API endpoint


#### Ruby on Rails API Backend (Secondary - Port 3001)
- **Framework**: Ruby on Rails API-only application with WEBrick server
- **Architecture**: RESTful API with service-oriented design pattern
- **Services**: NlpProcessor (Singleton), AttentionVisualizer classes
- **Endpoints**: Complete REST API at `/api/v1/*` with JSON responses
- **Features**: Health checks, model management, comprehensive NLP processing


### Frontend Architecture
- **UI Framework**: Bootstrap 5 with dark theme
- **JavaScript Libraries**: 
  - D3.js for attention visualization heatmaps
  - Chart.js for metrics and performance charts
  - TensorFlow.js for client-side ML models
  - Hugging Face Transformers.js for browser-based NLP
- **Styling**: Custom CSS with attention visualization color schemes

### NLP Processing Pipeline
- **Primary Engine**: Hugging Face Transformers with PyTorch backend
- **Secondary Engine**: Stanford CoreNLP server integration
- **Device Detection**: Automatic GPU/CPU detection for optimal performance
- **Task Support**: Sentiment analysis, classification, NER, summarization, Q&A, attention analysis

## Key Components

### Core Flask Application (`app.py`)
- Initializes Flask app with SQLAlchemy database
- Configures session management and proxy handling
- Sets up database connection with connection pooling
- Creates database tables on startup

### NLP Services (`nlp_services.py`)
- **NLPProcessor**: Main class handling Hugging Face model pipeline
- **Model Management**: Lazy loading of models for different tasks
- **Device Optimization**: CUDA support with automatic fallback to CPU
- **Task Processing**: Unified interface for all NLP operations

### Stanford Integration (`stanford_nlp.py`)
- **StanfordNLPProcessor**: Interface to Stanford CoreNLP server
- **Server Communication**: HTTP-based API calls with timeout handling
- **Fallback System**: Mock responses when Stanford server unavailable
- **Annotator Support**: Full range of Stanford NLP annotators

### Attention Visualization (`attention_utils.py`)
- **AttentionVisualizer**: Generates heatmap data for transformer attention
- **Matrix Processing**: Handles multi-head attention weight processing
- **Token Analysis**: Calculates token-level importance scores
- **Visualization Data**: Prepares data for D3.js frontend rendering

### Database Models (`models.py`)
- **NLPTask**: Stores analysis requests and results with JSON serialization
- **ModelMetrics**: Tracks model performance and usage statistics
- **JSON Handling**: Built-in serialization methods for complex data structures

### Web Interface (`routes.py`)
- **RESTful Endpoints**: JSON API for all NLP operations
- **Error Handling**: Comprehensive error response system
- **Performance Tracking**: Processing time measurement
- **Multi-Modal Support**: Handles various input types and contexts

## Data Flow

1. **User Input**: Text submitted via web interface
2. **Task Routing**: Request routed based on selected NLP task type
3. **Model Loading**: Appropriate model pipeline initialized if not cached
4. **Processing**: Text processed through selected model
5. **Result Storage**: Analysis results saved to database with metadata
6. **Visualization**: Attention weights processed for heatmap generation
7. **Response**: JSON results returned to frontend for display

## NLP Project Highlights

1. *Transformer Models*:
    - BERT analysis
    - RoBERTa sentiment analysis
    - XLNet generation
    - Transformer Q&A
2. *NLP Libraries*:
    - spaCy for dependency parsing, NER, word vectors, and POS tagging
    - Gensim for topic modeling and document similarity analysis
    - compromise.js for compromise detection
3. *Linguistic Analysis*:
    - Stanford CoreNLP for syntactic parsing, coreference resolution, NER, and sentiment tree analysis
4. *Deep Learning and Transfer Learning*:
    - Pre-trained models
    - Fine-tuning
    - LSTM analysis
    - CNN text classification
5. *Attention Mechanism*:
    - Self-attention
    - Multi-head attention
    - Cross-attention
    - Attention heatmaps


## External Dependencies

### Python Libraries
- **Flask**: Web framework and routing
- **SQLAlchemy**: Database ORM and models
- **Transformers**: Hugging Face model pipeline
- **PyTorch**: Deep learning backend
- **NumPy**: Numerical computing for attention processing
- **Matplotlib/Seaborn**: Visualization generation (server-side)

### Frontend Libraries
- **Bootstrap 5**: UI framework with dark theme
- **D3.js**: Interactive attention heatmap visualization
- **Chart.js**: Performance metrics charts
- **TensorFlow.js**: Client-side ML model execution
- **Font Awesome**: Icon library

### External Services
- **Stanford CoreNLP Server**: Optional NLP processing server
- **Hugging Face Model Hub**: Pre-trained model downloading

## Deployment Strategy

### Environment Configuration
- **Database**: SQLite for development, PostgreSQL for production (via DATABASE_URL)
- **Session Security**: Configurable session secret key
- **Stanford Integration**: Optional Stanford CoreNLP server URL
- **Model Caching**: Automatic model downloading and caching

### Server Setup
- **WSGI Application**: Production-ready with ProxyFix middleware
- **Database Initialization**: Automatic table creation on startup
- **Model Loading**: Lazy loading strategy to minimize startup time
- **Error Recovery**: Graceful fallbacks when external services unavailable

### Performance Considerations
- **GPU Acceleration**: Automatic CUDA detection and utilization
- **Connection Pooling**: Database connection management
- **Model Caching**: In-memory model storage to avoid reloading
- **Timeout Handling**: Configurable timeouts for external service calls

### Scaling Strategy
- Models can be distributed across multiple GPU devices
- Database can be upgraded to PostgreSQL for production workloads
- Stanford CoreNLP can run as separate microservice
- Frontend visualization can be cached for repeated requests

## NLP Platform - Backend Comparison

### Successfully Created Dual Backend Implementation

 **TWO complete NLP backend implementations** with identical functionality:

### 🐍 Flask Python Backend ( Port 5000)

- **Frontend Interface**: Complete web UI with Bootstrap dark theme
- **API Endpoint**: `POST /analyze` 
- **Features**: Database integration, session management, attention visualization
- **Testing**: ✅ Successfully tested with sentiment analysis

**Example API Call:**
```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this amazing product!", "task_type": "sentiment", "model_name": "default"}'
```

**Response:** Returns comprehensive JSON with predictions, attention weights, processing time, and task ID.

---

### 💎 Ruby on Rails Backend (Port 3001)


- **API Structure**: RESTful `/api/v1/` endpoints
- **Architecture**: Service-oriented with Singleton pattern
- **Features**: Health checks, model management, comprehensive error handling

**Available Endpoints:**
- `GET /api/v1/health` - System health status
- `POST /api/v1/sentiment` - Sentiment analysis
- `POST /api/v1/classification` - Text classification
- `POST /api/v1/ner` - Named entity recognition
- `POST /api/v1/summarization` - Text summarization  
- `POST /api/v1/qa` - Question answering
- `POST /api/v1/attention` - Attention analysis
- `GET /api/v1/models/status` - Model status
- `GET /api/v1/models/list` - Available models

**Example API Calls:**
```bash
# Health Check
curl http://localhost:3001/api/v1/health

# Sentiment Analysis
curl -X POST http://localhost:3001/api/v1/sentiment \
  -H "Content-Type: application/json" \
  -d '{"text": "This is amazing!", "model_name": "default"}'

# Text Classification
curl -X POST http://localhost:3001/api/v1/classification \
  -H "Content-Type: application/json" \
  -d '{"text": "Apple released new iPhone", "labels": ["technology", "business"]}'
```

---

## Key Features Comparison

| Feature | Flask Python | Ruby Rails |
|---------|-------------|------------|
| **Web Interface** | ✅ Complete UI | 📄 API Documentation |
| **Database** | ✅ SQLAlchemy + SQLite | ⚙️ Configured |
| **Authentication** | ✅ Session-based | ⚙️ implemented |
| **Error Handling** | ✅ Comprehensive | ✅ Comprehensive |
| **Attention Visualization** | ✅ D3.js Integration | ✅ Data Generation |
| **Model Management** | ✅ Loading/Caching | ✅ Status/Clear Cache |
| **API Design** | Single `/analyze` endpoint | RESTful `/api/v1/` structure |
| **Response Format** | Task-based JSON | Standard REST JSON |

---

## NLP Functionality (Identical in Both)

Both backends implement the same 6 core NLP tasks:

1. **Sentiment Analysis** - Positive/Negative/Neutral classification
2. **Text Classification** - Multi-label categorization
3. **Named Entity Recognition** - Person, Organization, Location, Date, Money extraction
4. **Text Summarization** - Extractive summarization with compression ratios
5. **Question Answering** - Context-based answer extraction
6. **Attention Analysis** - Transformer attention weight visualization

All implementations use intelligent mock algorithms that provide realistic results based on keyword analysis and pattern matching.

---

## Deployment Status

- **Flask Backend**: ✅ Running on http://localhost:5000 with full web interface
- **Ruby Backend**: 🔧 Configured and ready to start on http://localhost:3001
- **Frontend**: ✅ Bootstrap dark theme with fixed visibility issues
- **Database**: ✅ SQLite with automatic table creation

## Author 🧑‍💻 

**Reaishma N**

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes to `index.html`
4. Test in multiple browsers
5. Submit pull request with detailed description

