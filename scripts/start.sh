#!/bin/bash
# Start both backend and frontend servers
# Usage: ./scripts/start.sh [browser]
# Example: ./scripts/start.sh chrome

cd "$(dirname "$0")/.."

echo "🚀 Starting Species Counterpoint Generator..."

# Start backend
echo "📦 Starting backend server..."
cd backend
source .venv/bin/activate
python3 -m uvicorn app.main:app --reload > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > ../logs/backend.pid
cd ..

# Wait for backend to start
sleep 2

# Start frontend
echo "🎨 Starting frontend server..."
cd frontend
npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../logs/frontend.pid
cd ..

echo ""
echo "✅ Servers started!"
echo "   Backend PID: $BACKEND_PID (http://localhost:8000)"
echo "   Frontend PID: $FRONTEND_PID (http://localhost:5173)"
echo ""
echo "📝 Logs:"
echo "   Backend:  tail -f logs/backend.log"
echo "   Frontend: tail -f logs/frontend.log"
echo ""
echo "🛑 To stop: ./scripts/stop.sh"

# Wait a moment then open browser
sleep 3
echo "🌐 Opening browser..."

# Browser selection
BROWSER=${1:-default}
case $BROWSER in
  chrome)
    open -a "Google Chrome" http://localhost:5173
    ;;
  firefox)
    open -a "Firefox" http://localhost:5173
    ;;
  safari)
    open -a "Safari" http://localhost:5173
    ;;
  *)
    open http://localhost:5173
    ;;
esac
