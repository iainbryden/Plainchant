#!/bin/bash
# Restart both backend and frontend servers

cd "$(dirname "$0")"

echo "🔄 Restarting Species Counterpoint Generator..."
echo ""

./stop.sh
sleep 2
./start.sh "$@"
