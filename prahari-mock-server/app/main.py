from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.loader import load_json
from app.middleware.latency import ArtificialLatencyMiddleware
from app.validator import validate_system_consistency
from app.routers import (
    dashboard,
    model_analysis,
    event_monitor,
    historical_replay,
    event_detail,
    radar,
)

# Define base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n[STARTUP] Running Prahari Consistency Validator...")
    is_valid = validate_system_consistency()
    if not is_valid:
        print("[STARTUP WARNING] Fixture inconsistencies detected.\n")
    else:
        print("[STARTUP SUCCESS] All fixture consistency checks passed cleanly.\n")
    yield
    print("[SHUTDOWN] Stopping mock server.")


app = FastAPI(
    title="Prahari Extreme Weather Intelligence - Mock Server",
    version="1.0.0",
    lifespan=lifespan,
)

# Middleware registration
app.add_middleware(ArtificialLatencyMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", status_code=200)
async def health_check():
    return {"status": "ok"}


@app.get("/api/system-status")
async def get_system_status():
    return load_json("shared/systemStatus.json")


# Mount API routers
app.include_router(dashboard.router)
app.include_router(model_analysis.router)
app.include_router(event_monitor.router)
app.include_router(historical_replay.router)
app.include_router(event_detail.router)
app.include_router(radar.router)

# Mount static radar images
app.mount(
    "/static/radar",
    StaticFiles(directory=DATA_DIR / "radar"),
    name="radar_static",
)
