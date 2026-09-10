#!/bin/bash

# JARVIS AI Start Script
# Starts both backend and frontend servers

echo "🚀 Starting JARVIS AI"
echo "====================="

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Please run: bash setup.sh"
    exit 1
fi

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: bash setup.sh"
    exit 1
fi

source venv/bin/activate

echo ""
echo "📋 Starting servers..."
echo ""
echo "Backend will start on: http://localhost:8000"
echo "Frontend will start on: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start backend in background
echo "Starting backend..."
python backend/main.py &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 3

# Check if backend started successfully
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ Backend failed to start"
    exit 1
fi

echo "✓ Backend started (PID: $BACKEND_PID)"
echo ""

# Start frontend if Node.js is available
if command -v node &> /dev/null; then
    echo "Starting frontend..."
    cd frontend
    npm start &
    FRONTEND_PID=$!
    cd ..
    echo "✓ Frontend started (PID: $FRONTEND_PID)"
else
    echo "⚠️  Node.js not found, skipping frontend"
    FRONTEND_PID=""
fi

echo ""
echo "✅ JARVIS AI is running!"
echo ""
echo "Open your browser and visit:"
echo "  http://localhost:3000"
echo ""

# Keep script running and handle Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'JARVIS AI stopped'; exit 0" SIGINT
wait
