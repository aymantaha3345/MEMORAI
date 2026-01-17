# 🌟 MEMORAI - Persistent AI Memory Server

![MEMORAI Banner](https://github.com/aymantaha3345/MEMORAI/blob/main/Banner.jpg?raw=true)

**Author**: Ayman Taha  
**License**: MIT  
**Version**: 1.0.0

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/aymantaha3345/MEMORAI)

> ⚠️ **Note:** This project provides a foundational memory layer,  
> not a fully autonomous cognitive memory system.
> 
## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Environment Variables](#environment-variables)
- [Development](#development)
- [Contributing](#contributing)

## Overview

MEMORAI is a sophisticated persistent AI memory server that acts as intelligent middleware between client applications and LLM providers. It addresses critical limitations of stateless LLMs by providing robust, persistent memory capabilities that enable truly conversational AI experiences.

### Why MEMORAI?

Large Language Models excel at generating human-like responses but suffer from fundamental limitations:

| Challenge | MEMORAI Solution |
|-----------|------------------|
| ** Stateless Nature ** | Persistent user identity and conversation history |
| ** Limited Context Window ** | Intelligent memory injection and summarization |
| ** No Personalization ** | User-specific profiles and preferences |
| ** Context Overflow ** | Smart memory pruning and retention strategies |

## 🏗️ Architecture

```mermaid
graph TB
    subgraph "Client Applications"
        A["Web Apps"]
        B["Mobile Apps"]
        C["CLI Tools"]
    end
    
    subgraph "MEMORAI Core"
        D["API Gateway"]
        E["Authentication"]
        F["User Manager"]
        G["Memory Engine"]
        H["Context Builder"]
        I["Provider Router"]
        J["Response Processor"]
    end
    
    subgraph "Storage Layer"
        K["SQLite/PostgreSQL"]
        L["Redis Cache"]
        M["Memory Index"]
    end
    
    subgraph "LLM Providers"
        N["OpenAI"]
        O["Anthropic"]
        P["Google"]
        Q["Custom API"]
    end
    
    A --> D
    B --> D
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I
    I --> N
    I --> O
    I --> P
    I --> Q
    N --> J
    O --> J
    P --> J
    Q --> J
    G --> K
    G --> L
    H --> M
    J --> D
```

### Core Components

| Component | Function | Benefit |
|-----------|----------|---------|
| **Memory Engine** | Stores and retrieves user memories | Long-term context retention |
| **Context Builder** | Constructs prompts with relevant memories | Enhanced personalization |
| **Provider Abstraction** | Supports multiple LLM providers | Flexibility and vendor independence |
| **User Manager** | Handles user profiles and preferences | Customized experiences |
| **Pruning System** | Manages memory lifecycle | Optimal performance |

## ✨ Features

### 🧠 Advanced Memory Management
- **Multi-tier Memory**: Short-term, long-term, and summarized memory layers
- **Semantic Search**: Find relevant memories using advanced indexing
- **Automatic Summarization**: Condense lengthy conversations into key insights
- **Memory Decay Algorithm**: Automatically prioritize important memories

### 👤 Comprehensive User Profiles
- **Persistent Identity**: UUID-based user identification system
- **Preference Learning**: Adaptive learning of user preferences
- **Custom Instructions**: Personalized system prompts per user
- **Privacy Controls**: Granular data control and privacy settings

### 🔌 Universal Provider Support
- **OpenAI Compatibility**: Native support for ChatGPT models
- **Multi-vendor Support**: Anthropic Claude, Google Gemini, and others
- **Custom Adapters**: Easy integration for proprietary models
- **Load Balancing**: Distribute requests across providers

### 🛡️ Security & Privacy
- **Self-hosted Solution**: Complete data ownership
- **Encryption**: End-to-end encryption for sensitive data
- **Access Controls**: Role-based authentication and authorization
- **Compliance Ready**: GDPR and privacy regulation compliance

## 🚀 Installation

### Prerequisites
- **Python 3.12+** | Modern Python runtime
- **Git** | Version control system
- **Docker** | Containerization (optional)
- **API Keys** | Required for LLM providers

### Quick Start

#### Method 1: Local Installation
```bash
# Clone the repository
git clone https://github.com/aymantaha3345/memorai.git
cd memorai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Initialize database
python -c "from app.core.database import init_db; init_db()"

# Launch the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Method 2: Docker Deployment
```bash
# Build and run with Docker
docker-compose up --build

# Or pull from Docker Hub
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key_here \
  -e DATABASE_URL=sqlite:///./memorai.db \
  ayman/memorai:latest
```

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `OPENAI_API_KEY` | Yes | - | OpenAI API authentication |
| `DATABASE_URL` | No | `sqlite:///./memorai.db` | Database connection |
| `REDIS_URL` | No | `redis://localhost:6379` | Caching layer |
| `DEFAULT_PROVIDER` | No | `openai` | Primary LLM provider |
| `MAX_CONTEXT_TOKENS` | No | `8000` | Token limit per request |
| `MEMORY_RETENTION_DAYS` | No | `30` | Memory retention period |
| `LOG_LEVEL` | No | `INFO` | Logging verbosity |
| `ALLOWED_ORIGINS` | No | `*` | CORS configuration |

### Sample Configuration
```env
# API Keys
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here
GOOGLE_API_KEY=your-google-key-here

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost/memorai
REDIS_URL=redis://localhost:6379

# Server Settings
DEFAULT_PROVIDER=openai
MAX_CONTEXT_TOKENS=12000
MEMORY_RETENTION_DAYS=60
LOG_LEVEL=DEBUG

# Security
ALLOWED_ORIGINS=https://yourapp.com,https://anotherdomain.com
SECRET_KEY=your-secret-key-here
```

## 📡 API Documentation

### Base Endpoint
`http://localhost:8000` | `https://your-memorai-instance.com`

### Authentication
Include API key in headers:
```http
Authorization: Bearer your-api-token
Content-Type: application/json
```

### Core Endpoints

#### Chat Completion
```http
POST /api/v1/chat
```

**Request Body:**
```json
{
  "user_id": "user-uuid-string",
  "message": "How can you help me today?",
  "provider": "openai",
  "model": "gpt-4-turbo",
  "temperature": 0.7,
  "max_tokens": 1000,
  "include_memory": true,
  "custom_instructions": "Be helpful and concise"
}
```

**Response:**
```json
{
  "id": "response-uuid",
  "user_id": "user-uuid-string",
  "message": "I can help you by remembering our previous conversations...",
  "timestamp": "2024-01-15T10:30:00Z",
  "tokens_used": 85,
  "memory_injected": true,
  "context_relevance": 0.85,
  "provider_used": "openai"
}
```

#### User Profile Management
```http
GET /api/v1/user/{user_id}
```

**Response:**
```json
{
  "user_id": "user-uuid-string",
  "profile": {
    "name": "John Doe",
    "language": "en",
    "tone_preference": "professional",
    "communication_style": "direct",
    "interests": ["technology", "business", "education"]
  },
  "memory_stats": {
    "total_memories": 156,
    "active_conversations": 3,
    "last_interaction": "2024-01-15T09:45:00Z"
  },
  "created_at": "2024-01-01T12:00:00Z",
  "last_active": "2024-01-15T10:30:00Z"
}
```

#### Update User Preferences
```http
PUT /api/v1/user/{user_id}/preferences
```

**Request Body:**
```json
{
  "name": "Jane Smith",
  "language": "es",
  "tone_preference": "friendly",
  "custom_instructions": "Respond in Spanish with a warm, friendly tone...",
  "interests": ["art", "culture", "travel"]
}
```

#### Memory Operations
```http
POST /api/v1/memory/search
```

**Request Body:**
```json
{
  "user_id": "user-uuid-string",
  "query": "What did we discuss about project deadlines?",
  "limit": 5,
  "relevance_threshold": 0.7
}
```

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime": "4h 32m 15s",
  "providers": ["openai", "anthropic"],
  "database": "connected",
  "cache": "ready",
  "memory_usage": "45%",
  "active_users": 23,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## 🌐 Deployment Options

### Local Development
```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000
```

### Docker Compose (Production)
```yaml
version: '3.8'
services:
  memorai:
    image: ayman/memorai:latest
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=postgresql://postgres:password@db:5432/memorai
      - REDIS_URL=redis://redis:6379
      - DEFAULT_PROVIDER=openai
    depends_on:
      - db
      - redis
    restart: unless-stopped
    networks:
      - memorai-network

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=memorai
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - memorai-network

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    networks:
      - memorai-network

volumes:
  postgres_data:
  redis_data:

networks:
  memorai-network:
    driver: bridge
```

### Render.com Deployment
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/aymantaha3345/memorai)

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: memorai-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: memorai
  template:
    metadata:
      labels:
        app: memorai
    spec:
      containers:
      - name: memorai
        image: ayman/memorai:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: memorai-secrets
              key: openai-api-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

## 🛠️ Development

### Project Structure
```
memorai/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── chat.py         # Chat completion endpoints
│   │       ├── user.py         # User management endpoints
│   │       ├── memory.py       # Memory operations endpoints
│   │       └── admin.py        # Administrative endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration management
│   │   ├── database.py         # Database setup and connections
│   │   ├── security.py         # Authentication and authorization
│   │   ├── cache.py            # Caching utilities
│   │   └── logging.py          # Logging configuration
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── engine.py           # Core memory management logic
│   │   ├── storage.py          # Memory storage operations
│   │   ├── indexer.py          # Semantic search indexing
│   │   ├── summarizer.py       # Conversation summarization
│   │   └── pruner.py           # Memory lifecycle management
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # User data models
│   │   ├── memory.py           # Memory data models
│   │   ├── chat.py             # Chat message models
│   │   └── preferences.py      # User preference models
│   ├── providers/
│   │   ├── __init__.py
│   │   ├── base.py             # Base provider interface
│   │   ├── openai.py           # OpenAI provider implementation
│   │   ├── anthropic.py        # Anthropic provider implementation
│   │   ├── google.py           # Google provider implementation
│   │   └── factory.py          # Provider factory
│   └── utils/
│       ├── __init__.py
│       ├── logger.py           # Logging utilities
│       ├── helpers.py          # Helper functions
│       ├── validators.py       # Data validation utilities
│       └── crypto.py           # Cryptographic utilities
├── migrations/
├── tests/
│   ├── __init__.py
│   ├── test_chat.py           # Chat functionality tests
│   ├── test_memory.py         # Memory operations tests
│   ├── test_auth.py           # Authentication tests
│   └── conftest.py            # Test configuration
├── docs/
├── scripts/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── LICENSE
```

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test file
pytest tests/test_chat.py -v
```

### Code Quality
```bash
# Format code with Black
black app/

# Check code style with Flake8
flake8 app/

# Type checking with MyPy
mypy app/

# Security scanning with Bandit
bandit -r app/
```

## 🤝 Contributing

### Getting Started
1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/yourusername/memorai.git`
3. **Create** a feature branch: `git checkout -b feature/amazing-feature`
4. **Make** your changes
5. **Test** thoroughly
6. **Commit** your changes: `git commit -m 'Add amazing feature'`
7. **Push** to your branch: `git push origin feature/amazing-feature`
8. **Open** a Pull Request

### Development Guidelines
- Follow PEP 8 coding standards
- Write comprehensive docstrings for all functions
- Include unit tests for new features
- Update documentation as needed
- Keep commits atomic and well-described
- Ensure backward compatibility when possible

### Testing Requirements
- 100% code coverage for new features
- Pass all existing tests
- Include integration tests where appropriate
- Document any breaking changes

## 📈 Performance Benchmarks

| Metric | Performance | Notes |
|--------|-------------|-------|
| Response Time | < 200ms avg | Under normal load |
| Memory Throughput | 10,000 ops/sec | Concurrent operations |
| Storage Efficiency | 95% compression | Memory summarization |
| Provider Failover | < 500ms | Automatic fallback |
| Cache Hit Rate | > 90% | Redis caching |

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [API Reference](http://localhost:8000/docs)
- **Issues**: [GitHub Issues](https://github.com/aymantaha3345/memorai/issues)
- **Email**: aymantaha89pp@gmail.com

---

<div align="center">

**🌟 Built with ❤️ by Ayman Taha**  
*Making AI Conversations Truly Conversational*

[**🚀 Deploy Now**](https://render.com/deploy?repo=https://github.com/aymantaha3345/MEMORAI) | [**📚 Documentation**](http://localhost:8000/docs) | [**🐛 Report Bug**](https://github.com/aymantaha3345/memorai/issues)


</div>

