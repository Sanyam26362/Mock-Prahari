#!/bin/bash
set -e

# If running from repository root where prahari-mock-server is a subfolder, navigate into it
if [ -d "prahari-mock-server" ]; then
    cd prahari-mock-server
fi

# Render provides the port in the $PORT environment variable. Default to 8000 for local runs.
PORT_TO_USE="${PORT:-8000}"

echo "[STARTUP] Launching Doppler Radar Harvester Daemon in background..."
python scripts/capture_radar.py --interval 600 --simulate &

echo "[STARTUP] Launching Prahari FastAPI Application on port $PORT_TO_USE..."
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT_TO_USE"
