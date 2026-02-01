# 🚀 Getting Started with CityPulse

Welcome to CityPulse! This guide will help you get the project running on your Mac.

## 📋 Prerequisites

### Required Software

1. **Docker Desktop for Mac**
   - Download from: https://www.docker.com/products/docker-desktop/
   - Version: 4.0 or higher
   - Docker Compose is included with Docker Desktop

2. **VS Code** (Recommended)
   - Download from: https://code.visualstudio.com/
   - Extensions to install:
     - Python
     - ESLint
     - Prettier
     - Docker
     - Tailwind CSS IntelliSense

3. **Git**
   - Pre-installed on macOS
   - Verify: `git --version`

### Optional (for local development without Docker)

- **Python 3.11+**
- **Node.js 18+** with npm
- **PostgreSQL 15+**
- **Redis 7+**

## 🎯 Quick Start (Docker - Recommended)

### Method 1: Automated Setup

```bash
# 1. Extract the project
tar -xzf citypulse.tar.gz
cd citypulse

# 2. Run the setup script
chmod +x setup.sh
./setup.sh
```

That's it! The script will:
- Create environment file
- Build Docker images
- Start all services
- Show you the URLs to access

### Method 2: Manual Docker Setup

```bash
# 1. Extract and navigate
tar -xzf citypulse.tar.gz
cd citypulse

# 2. Create environment file
cp .env.example .env

# 3. Start with Docker Compose
docker-compose up -d --build

# 4. Check status
docker-compose ps

# 5. View logs
docker-compose logs -f
```

## 🌐 Accessing the Application

Once running, access:

- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## 🛠️ Local Development Setup (Without Docker)

If you prefer to run services locally:

### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up database (requires PostgreSQL running)
# Update DATABASE_URL in .env to your local PostgreSQL
alembic upgrade head

# Start backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Required Services

You'll need PostgreSQL and Redis running locally:

```bash
# Using Homebrew on Mac
brew install postgresql@15 redis

# Start services
brew services start postgresql@15
brew services start redis
```

## 📝 Configuration

### Environment Variables

Edit `.env` file to configure:

```env
# Database
DATABASE_URL=postgresql://citypulse:citypulse123@db:5432/citypulse

# Redis
REDIS_URL=redis://redis:6379/0

# Application
SECRET_KEY=your-secret-key-here
ENVIRONMENT=development

# API Keys (optional)
OPENWEATHER_API_KEY=your_key_here
```

### Development vs Production

- **Development**: Uses `.env` with debug enabled
- **Production**: Use environment variables directly, disable debug

## 🐛 Troubleshooting

### Port Already in Use

If ports 3000 or 8000 are taken:

```bash
# Find process using port
lsof -i :3000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or change ports in docker-compose.yml
```

### Docker Issues

```bash
# Clean up and restart
docker-compose down -v
docker-compose up -d --build

# View detailed logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Access container shell
docker-compose exec backend bash
docker-compose exec frontend sh
```

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker-compose ps db

# Reset database
docker-compose down -v  # Warning: deletes data
docker-compose up -d
```

### Frontend Not Loading

```bash
# Frontend takes 1-2 minutes to compile on first run
# Check logs
docker-compose logs -f frontend

# If stuck, restart
docker-compose restart frontend
```

## 🧪 Testing

### Backend Tests

```bash
# In Docker
docker-compose exec backend pytest tests/ -v

# Locally
cd backend
pytest tests/ -v --cov=app
```

### Frontend Tests

```bash
# In Docker
docker-compose exec frontend npm test

# Locally
cd frontend
npm test
```

## 📊 Viewing Data

### Access Database

```bash
# Using Docker
docker-compose exec db psql -U citypulse -d citypulse

# Common queries
SELECT COUNT(*) FROM events;
SELECT * FROM events ORDER BY created_at DESC LIMIT 10;
```

### Access Redis

```bash
# Using Docker
docker-compose exec redis redis-cli

# Check pub/sub channels
PUBSUB CHANNELS
```

## 🔄 Common Development Tasks

### Add Python Dependency

```bash
# Add to backend/requirements.txt
echo "package-name==version" >> backend/requirements.txt

# Rebuild
docker-compose up -d --build backend
```

### Add Frontend Dependency

```bash
# In frontend directory
docker-compose exec frontend npm install package-name

# Or rebuild
cd frontend && npm install package-name
docker-compose up -d --build frontend
```

### Create Database Migration

```bash
# Access backend container
docker-compose exec backend bash

# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```

### View API Documentation

Navigate to:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🎨 Customization

### Change Color Scheme

Edit `frontend/tailwind.config.js`:

```javascript
colors: {
  primary: {
    // Your custom colors
  }
}
```

### Add New API Endpoint

1. Create route in `backend/app/api/v1/endpoints/`
2. Add schema in `backend/app/schemas/`
3. Update main router in `backend/app/main.py`

### Add New Component

```bash
cd frontend/src/components
mkdir your-component
touch your-component/YourComponent.jsx
```

## 📦 Deployment

### Build for Production

```bash
# Backend
cd backend
docker build -t citypulse-backend .

# Frontend
cd frontend
npm run build
```

### Deploy to AWS/GCP

See deployment guides in `/docs` directory.

## 🆘 Getting Help

### Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### Check Service Health

```bash
# Health endpoint
curl http://localhost:8000/health

# Check all containers
docker-compose ps
```

### Reset Everything

```bash
# Stop and remove all containers and volumes
docker-compose down -v

# Remove images
docker-compose down --rmi all

# Start fresh
docker-compose up -d --build
```

## 📚 Next Steps

1. **Explore the Dashboard**: Navigate to http://localhost:3000
2. **Check API Docs**: Visit http://localhost:8000/docs
3. **View Real-Time Data**: Watch events stream in real-time
4. **Customize**: Modify components to match your needs
5. **Deploy**: Push to GitHub and deploy to cloud

## 🎓 Learning Resources

- **FastAPI**: https://fastapi.tiangolo.com/
- **React**: https://react.dev/
- **Docker**: https://docs.docker.com/
- **PostgreSQL**: https://www.postgresql.org/docs/
- **Tailwind CSS**: https://tailwindcss.com/docs

---

**Need Help?** Open an issue on GitHub or check the documentation in `/docs`.

Happy coding! 🚀
