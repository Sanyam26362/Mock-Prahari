#!/bin/bash
set -e

echo "[STARTUP] Starting Doppler Radar Harvester Daemon in background..."
python scripts/capture_radar.py --interval 600 --simulate &

echo "[STARTUP] Starting Prahari FastAPI server on port 7860..."
exec uvicorn app.main:app --host 0.0.0.0 --port 7860
