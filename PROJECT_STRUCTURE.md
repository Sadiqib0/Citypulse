# 📁 Project Structure Documentation

## Complete Directory Tree

```
citypulse/
│
├── README.md                      # Main project documentation
├── GITHUB_GUIDE.md               # GitHub deployment guide
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore rules
├── docker-compose.yml            # Docker orchestration
├── setup.sh                      # Quick setup script
│
├── backend/                      # Python FastAPI backend
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic.ini              # Database migration config
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application entry point
│   │   │
│   │   ├── api/                 # API layer
│   │   │   ├── __init__.py
│   │   │   ├── websocket.py     # WebSocket handlers
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── deps.py      # API dependencies
│   │   │       └── endpoints/   # API route handlers
│   │   │           ├── __init__.py
│   │   │           ├── events.py      # Events CRUD
│   │   │           └── analytics.py   # Analytics endpoints
│   │   │
│   │   ├── core/                # Core configurations
│   │   │   ├── __init__.py
│   │   │   ├── config.py        # Settings management
│   │   │   ├── security.py      # Auth utilities
│   │   │   └── events.py        # Lifecycle events
│   │   │
│   │   ├── db/                  # Database layer
│   │   │   ├── __init__.py
│   │   │   ├── base.py          # Base models
│   │   │   └── session.py       # Session management
│   │   │
│   │   ├── models/              # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   └── events.py        # Event, Sensor, Alert models
│   │   │
│   │   ├── schemas/             # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   └── events.py        # Request/response schemas
│   │   │
│   │   └── services/            # Business logic
│   │       ├── __init__.py
│   │       ├── collectors/      # Data collection
│   │       │   ├── __init__.py
│   │       │   └── data_collector.py
│   │       └── analytics/       # Analytics engine
│   │           ├── __init__.py
│   │           └── analytics_service.py
│   │
│   ├── alembic/                 # Database migrations
│   │   ├── env.py
│   │   └── versions/
│   │
│   └── tests/                   # Backend tests
│
├── frontend/                    # React frontend
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.js          # Vite configuration
│   ├── tailwind.config.js      # Tailwind CSS config
│   ├── postcss.config.js       # PostCSS config
│   ├── index.html              # HTML entry point
│   │
│   ├── public/                 # Static assets
│   │
│   └── src/
│       ├── main.jsx            # React entry point
│       ├── App.jsx             # Main App component
│       │
│       ├── components/         # React components
│       │   ├── dashboard/
│       │   │   ├── Dashboard.jsx       # Main dashboard
│       │   │   ├── MetricCard.jsx      # Metric display
│       │   │   ├── LiveEventsFeed.jsx  # Live events
│       │   │   └── WeatherWidget.jsx   # Weather display
│       │   ├── charts/
│       │   │   └── TrafficChart.jsx    # Traffic visualization
│       │   └── maps/
│       │       └── CityMap.jsx         # Interactive map
│       │
│       ├── services/           # API services
│       │   └── api.js          # API client
│       │
│       └── styles/             # Styling
│           └── index.css       # Global styles
│
└── docs/                       # Additional documentation
    └── ARCHITECTURE.md         # Architecture overview
```

## Component Responsibilities

### Backend Components

#### Core Layer (`app/core/`)
- **config.py**: Central configuration management using Pydantic
- **security.py**: Authentication and authorization utilities
- **events.py**: Application lifecycle event handlers

#### Database Layer (`app/db/`)
- **base.py**: SQLAlchemy base models and mixins
- **session.py**: Database session management with async support

#### Models (`app/models/`)
- **events.py**: Database models for Event, Sensor, SensorData, Alert

#### Schemas (`app/schemas/`)
- **events.py**: Pydantic schemas for request/response validation

#### API Layer (`app/api/`)
- **websocket.py**: WebSocket connection management for real-time data
- **v1/endpoints/**: REST API endpoints organized by resource

#### Services (`app/services/`)
- **collectors/data_collector.py**: Simulates and collects city data
- **analytics/analytics_service.py**: Data analysis and insights

### Frontend Components

#### Dashboard Components (`src/components/dashboard/`)
- **Dashboard.jsx**: Main dashboard orchestrator
- **MetricCard.jsx**: Reusable metric display card
- **LiveEventsFeed.jsx**: Real-time event stream display
- **WeatherWidget.jsx**: Weather information widget

#### Visualization Components
- **charts/TrafficChart.jsx**: Traffic data visualization using Recharts
- **maps/CityMap.jsx**: Interactive city map using Leaflet

#### Services (`src/services/`)
- **api.js**: Centralized API client with axios and WebSocket support

## Data Flow

```
┌─────────────────┐
│  Data Sources   │ (External APIs / Simulated)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Data Collectors │ (Background Tasks)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Redis Pub/Sub   │ (Event Streaming)
└────────┬────────┘
         │
         ├──────────────┐
         │              │
         ▼              ▼
┌────────────┐   ┌──────────────┐
│ PostgreSQL │   │  WebSocket   │
│  Database  │   │    Server    │
└─────┬──────┘   └──────┬───────┘
      │                 │
      ▼                 ▼
┌─────────────────────────────┐
│     FastAPI Backend         │
│  (REST API + WebSockets)    │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      React Frontend         │
│  (Dashboard + Visualizations)│
└─────────────────────────────┘
```

## Technology Stack Breakdown

### Backend
- **FastAPI**: Modern Python web framework with async support
- **SQLAlchemy**: ORM for database operations
- **Alembic**: Database migration tool
- **Pydantic**: Data validation and settings management
- **Redis**: In-memory data store for caching and pub/sub
- **PostgreSQL**: Primary relational database
- **Uvicorn**: ASGI server

### Frontend
- **React 18**: UI library
- **Vite**: Build tool and dev server
- **TanStack Query**: Data fetching and caching
- **Recharts**: Data visualization library
- **Leaflet**: Interactive maps
- **Framer Motion**: Animation library
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration

## Key Features Implementation

### 1. Real-Time Data Streaming
- Redis pub/sub for event broadcasting
- WebSocket connections for bi-directional communication
- Connection manager for handling multiple clients

### 2. Data Collection
- Background tasks using asyncio
- Simulated data for traffic, weather, and sensors
- Configurable collection intervals

### 3. Analytics Engine
- Statistical analysis using pandas/numpy
- Anomaly detection with z-score
- Time-series predictions

### 4. API Design
- RESTful endpoints following best practices
- OpenAPI documentation
- Versioned API (v1)
- Comprehensive error handling

### 5. Frontend Architecture
- Component-based design
- Custom hooks for data fetching
- Responsive layout with Tailwind
- Real-time updates via WebSocket

## Performance Considerations

- **Database Indexing**: Event type, severity, and timestamp columns
- **Connection Pooling**: PostgreSQL and Redis connection pools
- **Caching**: Redis for frequently accessed data
- **Async Operations**: All I/O operations are asynchronous
- **Lazy Loading**: Components load data progressively

## Security Features

- CORS configuration
- Environment-based secrets
- SQL injection prevention (SQLAlchemy ORM)
- Input validation (Pydantic)

## Scalability

- Stateless API design
- Horizontal scaling ready
- Containerized architecture
- Database migrations for schema evolution
