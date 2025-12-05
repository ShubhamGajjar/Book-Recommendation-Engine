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
python backend/app.py > backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to initialize..."
sleep 5

# Check if backend is running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ Backend failed to start. Check backend.log for errors"
    exit 1
fi

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
echo "✅ Backend running (PID: $BACKEND_PID)"
echo "✅ Frontend running on http://localhost:3000 (PID: $FRONTEND_PID)"
echo "   (Backend port will be shown in backend output)"
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
