#!/bin/bash

# --------------------------
# 1. Kill processes on ports
# --------------------------
echo "Checking and killing any process on port 8000 (backend)..."
PID_8000=$(lsof -ti :8000)
if [ -n "$PID_8000" ]; then
    kill -9 $PID_8000
    echo "Killed backend process $PID_8000"
fi

echo "Checking and killing any process on port 3000 (frontend)..."
PID_3000=$(lsof -ti :3000)
if [ -n "$PID_3000" ]; then
    kill -9 $PID_3000
    echo "Killed frontend process $PID_3000"
fi

# --------------------------
# 2. Start backend
# --------------------------
echo "Starting backend..."
cd backend

# Create venv if not exists
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Created virtual environment"
fi

# Activate venv
source venv/bin/activate

# Install dependencies if missing
pip install --upgrade pip
pip install -r requirements.txt

# Start backend in background on port 8000
uvicorn realtime:app --reload --port 8000 &

# --------------------------
# 3. Start frontend
# --------------------------
echo "Starting frontend..."
cd ../frontend

# Start HTTP server on port 3000
python3 -m http.server 3000

