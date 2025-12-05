#!/bin/bash

echo "🚀 Starting Book Recommendation Engine..."
echo ""

# Check if CSV file exists
if [ ! -f "goodreads_books_2024.csv" ]; then
    echo "❌ Error: goodreads_books_2024.csv not found in project root"
    echo "Please download the dataset and place it in the project root directory"
    exit 1
fi

# Start backend in background
echo "📡 Starting backend server..."
cd "$(dirname "$0")"

# Check if backend is already running on port 5001
if lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Port 5001 is already in use. Stopping existing process..."
    lsof -ti:5001 | xargs kill -9 2>/dev/null
    sleep 2
fi

python backend/app.py > backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to initialize..."
sleep 3

# Check if backend process is still running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ Backend process died. Check backend.log for errors:"
    echo ""
    tail -20 backend.log
    exit 1
fi

# Wait a bit more and check if it's responding
sleep 3
if ! curl -s http://localhost:5001/api/health > /dev/null 2>&1; then
    echo "⚠️  Backend process is running but not responding. Check backend.log:"
    echo ""
    tail -20 backend.log
    echo ""
    echo "Continuing anyway..."
fi

echo "✅ Backend started successfully (PID: $BACKEND_PID)"

# Start frontend
echo "🎨 Starting frontend server..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Backend running on http://localhost:5001 (PID: $BACKEND_PID)"
echo "✅ Frontend running on http://localhost:3000 (PID: $FRONTEND_PID)"
echo ""
echo "📝 Backend logs: tail -f backend.log"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

# Trap Ctrl+C
trap cleanup INT

# Wait for processes
wait
