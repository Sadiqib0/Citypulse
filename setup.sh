#!/bin/bash
# CityPulse Setup Script
# This script sets up the entire CityPulse platform

set -e

echo "🌆 CityPulse - Setup Script"
echo "============================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}⚠️  Docker is not installed. Please install Docker first.${NC}"
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}⚠️  Docker Compose is not installed. Please install Docker Compose first.${NC}"
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${BLUE}✓${NC} Docker and Docker Compose are installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}📝 Creating .env file...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓${NC} .env file created"
else
    echo -e "${GREEN}✓${NC} .env file already exists"
fi

echo ""
echo -e "${BLUE}🐳 Building and starting Docker containers...${NC}"
echo "This may take a few minutes on first run..."
echo ""

# Build and start containers
docker-compose up -d --build

echo ""
echo -e "${GREEN}✓${NC} Containers are starting up..."
echo ""

# Wait for services to be healthy
echo -e "${BLUE}⏳ Waiting for services to be ready...${NC}"
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo -e "${GREEN}✓${NC} Services are running!"
else
    echo -e "${YELLOW}⚠️  Some services may not be running correctly${NC}"
    docker-compose ps
fi

echo ""
echo "================================================="
echo -e "${GREEN}🎉 CityPulse is now running!${NC}"
echo "================================================="
echo ""
echo "Access the application:"
echo -e "  ${BLUE}Frontend:${NC}     http://localhost:3000"
echo -e "  ${BLUE}Backend API:${NC}  http://localhost:8000"
echo -e "  ${BLUE}API Docs:${NC}     http://localhost:8000/docs"
echo ""
echo "Useful commands:"
echo "  View logs:        docker-compose logs -f"
echo "  Stop services:    docker-compose down"
echo "  Restart:          docker-compose restart"
echo ""
echo -e "${YELLOW}Note:${NC} The frontend may take a minute to compile on first run."
echo ""
