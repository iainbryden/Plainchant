#!/bin/bash
# Stop both backend and frontend servers

cd "$(dirname "$0")/.."

echo "🛑 Stopping Species Counterpoint Generator..."

# Stop backend
if [ -f logs/backend.pid ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo "📦 Stopping backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
        rm logs/backend.pid
    else
        echo "⚠️  Backend not running"
        rm logs/backend.pid
    fi
else
    echo "⚠️  Backend PID file not found"
fi

# Stop frontend
if [ -f logs/frontend.pid ]; then
    FRONTEND_PID=$(cat logs/frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        echo "🎨 Stopping frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
        rm logs/frontend.pid
    else
        echo "⚠️  Frontend not running"
        rm logs/frontend.pid
    fi
else
    echo "⚠️  Frontend PID file not found"
fi

echo "✅ Servers stopped"
