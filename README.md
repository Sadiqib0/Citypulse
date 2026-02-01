# 🌆 CityPulse - Real-Time Event & Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61dafb.svg)](https://react.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7+-red.svg)](https://redis.io/)

A production-grade real-time data platform that collects, streams, analyzes, and visualizes city events, traffic patterns, weather data, and IoT sensor readings. Built with modern technologies and scalable architecture.

## 🎯 Features

- **Real-Time Data Streaming**: WebSocket-based live data feeds with fallback to SSE
- **Multi-Source Data Collection**: Traffic, weather, social events, and simulated IoT sensors
- **Advanced Analytics**: Time-series analysis, anomaly detection, and predictive insights
- **Interactive Dashboards**: Beautiful, responsive UI with live charts and maps
- **Alert System**: Configurable threshold-based alerting with notification channels
- **RESTful API**: Comprehensive API with OpenAPI documentation
- **Scalable Architecture**: Microservices-ready with Docker containerization
- **Data Persistence**: PostgreSQL for structured data, Redis for caching and real-time state

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   External  │────▶│  Data        │────▶│  FastAPI    │
│   APIs      │     │  Collectors  │     │  Backend    │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                 │
                    ┌────────────────────────────┼────────────────┐
                    │                            │                │
              ┌─────▼─────┐              ┌──────▼──────┐   ┌─────▼─────┐
              │ PostgreSQL│              │    Redis    │   │ WebSocket │
              │  Database │              │    Cache    │   │  Server   │
              └───────────┘              └─────────────┘   └─────┬─────┘
                                                                  │
                                                            ┌─────▼─────┐
                                                            │   React   │
                                                            │  Frontend │
                                                            └───────────┘
```

## 📁 Project Structure

```
citypulse/
├── backend/                    # Python FastAPI backend
│   ├── app/
│   │   ├── api/               # API endpoints
│   │   │   ├── v1/
│   │   │   │   ├── endpoints/ # Route handlers
│   │   │   │   └── deps.py    # Dependencies
│   │   │   └── websocket.py   # WebSocket handlers
│   │   ├── core/              # Core configurations
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── events.py
│   │   ├── db/                # Database layer
│   │   │   ├── base.py
│   │   │   ├── session.py
│   │   │   └── init_db.py
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   │   ├── collectors/    # Data collectors
│   │   │   ├── analytics/     # Analytics engine
│   │   │   └── alerts/        # Alert system
│   │   ├── utils/             # Utilities
│   │   └── main.py            # Application entry point
│   ├── tests/                 # Backend tests
│   ├── alembic/               # Database migrations
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── dashboard/
│   │   │   ├── charts/
│   │   │   ├── maps/
│   │   │   └── common/
│   │   ├── hooks/             # Custom React hooks
│   │   ├── services/          # API client services
│   │   ├── store/             # State management
│   │   ├── utils/             # Utilities
│   │   ├── styles/            # Global styles
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── public/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml          # Docker orchestration
├── .env.example               # Environment variables template
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **Node.js 18+** and npm
- **Docker & Docker Compose** (recommended)
- **PostgreSQL 15+** (if running locally)
- **Redis 7+** (if running locally)

### Option 1: Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/citypulse.git
   cd citypulse
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Option 2: Local Development

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database
alembic upgrade head

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## 🔧 Configuration

Key environment variables (see `.env.example`):

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/citypulse
REDIS_URL=redis://localhost:6379/0

# API Keys (Optional - for real data)
OPENWEATHER_API_KEY=your_key_here
TRAFFIC_API_KEY=your_key_here

# Application
SECRET_KEY=your-secret-key-here
ENVIRONMENT=development
```

## 📊 API Endpoints

### Events
- `GET /api/v1/events` - List all events
- `GET /api/v1/events/{id}` - Get event details
- `GET /api/v1/events/live` - Real-time event stream (SSE)

### Analytics
- `GET /api/v1/analytics/overview` - Dashboard overview
- `GET /api/v1/analytics/traffic` - Traffic analytics
- `GET /api/v1/analytics/weather` - Weather trends
- `GET /api/v1/analytics/predictions` - Predictive analytics

### Sensors
- `GET /api/v1/sensors` - List IoT sensors
- `GET /api/v1/sensors/{id}/data` - Sensor data stream

### Alerts
- `GET /api/v1/alerts` - List alerts
- `POST /api/v1/alerts` - Create alert rule
- `PUT /api/v1/alerts/{id}` - Update alert

### WebSocket
- `WS /ws/events` - Real-time event stream
- `WS /ws/sensors/{id}` - Sensor data stream

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v --cov=app
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📦 Deployment

### AWS Deployment

1. **Set up infrastructure** (EC2, RDS, ElastiCache)
2. **Configure security groups** and VPC
3. **Deploy with Docker Compose** or use ECS/EKS
4. **Set up CloudFront** for frontend CDN

### Environment-specific configs
- `docker-compose.yml` - Development
- `docker-compose.prod.yml` - Production

## 🎨 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **Redis** - Caching and real-time state
- **WebSockets** - Real-time communication

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **Recharts** - Data visualization
- **Leaflet** - Interactive maps
- **TanStack Query** - Data fetching
- **Tailwind CSS** - Styling

### Database
- **PostgreSQL** - Primary data store
- **Redis** - Cache and pub/sub

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **GitHub Actions** - CI/CD (optional)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

## 🙏 Acknowledgments

- Weather data from OpenWeatherMap
- Traffic data simulation inspired by real-world patterns
- Icon design by Heroicons

---

⭐ If you found this project helpful, please give it a star!
