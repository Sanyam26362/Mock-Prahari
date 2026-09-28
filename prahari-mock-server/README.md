---
title: Prahari Extreme Weather Intelligence API
emoji: 🌪️
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# Prahari: Extreme Weather Intelligence
### High-Resolution Extreme Weather Forecasting & Early Warning Platform
**Smart India Hackathon (SIH 2026) | Problem Statement: PS 26078**

---

## 1. Executive Summary & Problem Statement

Extreme meteorological events across the Indian subcontinent—such as super cyclones in the Bay of Bengal, extreme urban deluges, cloudbursts along the Himalayan foothills, and severe heatwaves over the northern plains—demand rapid, high-resolution predictive intelligence.

Conventional Numerical Weather Prediction (NWP) models (e.g., ECMWF-HRES, IMD-GFS) provide coarse spatial grids (~12km–25km) and require high-performance supercomputing clusters, incurring hours of compute latency. **Prahari** bridges this gap by delivering a **two-stage hybrid Deep Learning architecture**:
1. **Stage 1 (Global/Regional Dynamics):** Spherical Graph Neural Network (GNN) on an icosahedral hexagonal mesh tracking atmospheric vorticity and cyclone trajectories at 12km resolution.
2. **Stage 2 (Local Downscaling):** Conditional Diffusion Super-Resolution model downscaling atmospheric fields from 12km to 5km terrain-aware grids in sub-second inference latencies.
3. **Stage 3 (Decision Support):** Automated Extreme Forecast Index (EFI) computation and Common Alerting Protocol (CAP) compliant emergency warning generation.

This repository hosts the **Prahari Mock Server**, designed as a production-grade, zero-dependency temporary backend providing deterministic API responses, realistic latency emulation, live Doppler radar harvesting, and strict schema validation for rapid frontend development.

---

## 2. Mock Server Architecture & Core Capabilities

```text
prahari-mock-server/
├── app/
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── latency.py          # Configurable artificial latency (150ms-450ms)
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── dashboard.py        # 6 Dashboard KPI & overview routes
│   │   ├── event_detail.py     # Event deep-dive, interactive map, & CAP alerts
│   │   ├── event_monitor.py    # Live cyclone/storm telemetry & trajectories
│   │   ├── historical_replay.py# Historical event comparisons & verification
│   │   ├── model_analysis.py   # GNN & Diffusion pipeline metrics & charts
│   │   └── radar.py            # Doppler radar station & frame scanner
│   ├── __init__.py
│   ├── loader.py               # Path-safe JSON loader with case-insensitive keyed lookup
│   ├── main.py                 # FastAPI application, CORS, lifespan, & static mounting
│   ├── radar_scanner.py        # Regex filename parser & ISO-8601 frame sorting
│   └── validator.py            # 4-rule startup consistency verification engine
├── config/
│   └── radar_sources.json      # Live IMD Doppler radar feed configuration
├── data/                       # Domain-accurate mock JSON fixtures
│   ├── dashboard/              # Basin overview, storm KPIs, active anomalies
│   ├── eventDetail/            # Event maps, metrics, hazard polygons, CAP alerts
│   ├── eventMonitor/           # Telemetry, diagnostics, intensity distributions
│   ├── historicalReplay/       # Amphan, Biparjoy, Mumbai Deluge case studies
│   ├── modelAnalysis/          # Verification curves, track error charts, latencies
│   ├── radar/                  # Station metadata and Doppler frame storage
│   └── shared/                 # Operational system status
├── scripts/
│   ├── capture_radar.py        # Doppler radar ingestion daemon (live & simulation)
│   └── test_all_endpoints.ps1  # Automated PowerShell test harness (43 endpoints)
├── tests/                      # Automated Python test suites (Phases 1-6)
└── requirements.txt            # Python dependencies (fastapi, uvicorn, httpx)
```

### Key Technical Features
- **Bare Resource Returns:** All endpoints return raw JSON objects without artificial nesting (`{ "data": ... }` or `{ "result": ... }`), perfectly matching the frontend TypeScript API contracts.
- **Case-Insensitive Dynamic Lookups:** Keyed queries (e.g. `/api/events/BOB-02` vs `/api/events/bob-02`) normalize keys via `.strip().lower()`, ensuring cross-platform client compatibility.
- **Static Route Prioritization:** Specific sub-routes (such as `/api/historical-events/comparison-modes` and `/api/event-detail/events`) are registered before parameterized `/{eventId}` routes to eliminate route shadowing.
- **Doppler Radar Image Harvesting & Static Serving:**
  - Automated scanner parses filenames conforming to `<stationId>_<product>_<YYYYMMDDTHHMMZ>.png`.
  - Normalizes timestamps to ISO-8601 (`YYYY-MM-DDTHH:MM:00Z`).
  - Sorts frames chronologically (oldest to newest).
  - Dynamically supports `from`, `to`, and `limit` query parameters.
  - Image files are served statically with standard `image/png` MIME types under `/static/radar/...`.
- **Configurable Artificial Latency:**
  - Emulates ML inference and radar synchronization delays (default: 150ms – 450ms).
  - Selectively excludes `/api/health` and `/static/*` requests.
  - Easily toggled via environment variable `MOCK_LATENCY=false`.
- **Startup Integrity Validator:** Modern `@asynccontextmanager` FastAPI lifespan executes 4 automated checks at boot time to guarantee zero corrupted or missing fixtures.

---

## 3. Complete API Endpoint Inventory

| Method | Endpoint Route | Description / Fixture | Tag |
|---|---|---|---|
| `GET` | `/api/health` | Service health status (`{"status": "ok"}`) | Core Health |
| `GET` | `/api/system-status` | AI pipeline operational state & active model metadata | Shared System |
| `GET` | `/api/dashboard/overview` | Monitored oceanic basins & current threat level | Dashboard |
| `GET` | `/api/dashboard/kpis` | Active storm cells, risk population, & downscale metrics | Dashboard |
| `GET` | `/api/dashboard/anomaly-overview` | Summary of all active extreme meteorological anomalies | Dashboard |
| `GET` | `/api/dashboard/active-anomalies` | Telemetry for active storm tracking | Dashboard |
| `GET` | `/api/dashboard/forecast-timeline` | Multi-day lead time forecast steps & confidence scores | Dashboard |
| `GET` | `/api/dashboard/processing-pipeline` | Latencies per pipeline stage (GNN, Diffusion, CAP) | Dashboard |
| `GET` | `/api/model-analysis/overview` | Production model inference stats & ensemble dispersion | Model Analysis |
| `GET` | `/api/model-analysis/models` | Registry of active & standby model weights | Model Analysis |
| `GET` | `/api/model-analysis/pipeline` | Detailed breakdown of atmospheric ingestion pipeline | Model Analysis |
| `GET` | `/api/model-analysis/configuration` | Hyperparameters, diffusion steps, & mesh resolution | Model Analysis |
| `GET` | `/api/model-analysis/metrics` | RMSE, ACC, Brier Skill Score, & Equitable Threat Score | Model Analysis |
| `GET` | `/api/model-analysis/verification` | Ground-truth verification against IMD AWS / Radar | Model Analysis |
| `GET` | `/api/model-analysis/track-error-chart` | Lead-time track error comparison (Prahari vs Numerical) | Model Analysis |
| `GET` | `/api/model-analysis/baseline-comparison` | Speedup and energy efficiency benchmarks | Model Analysis |
| `GET` | `/api/events/` | Selectable active event options | Event Monitor |
| `GET` | `/api/events/{eventId}` | Detailed storm telemetry and estimated landfall | Event Monitor |
| `GET` | `/api/events/{eventId}/trajectory` | Historical and predicted cone of uncertainty waypoints | Event Monitor |
| `GET` | `/api/events/{eventId}/timeline` | Lifecycle progression stages (Genesis -> Alert -> Landfall)| Event Monitor |
| `GET` | `/api/events/{eventId}/telemetry` | Surface pressure, sea surface temperature, wind shear | Event Monitor |
| `GET` | `/api/events/{eventId}/diagnostics` | GNN confidence scores & convective coupling indices | Event Monitor |
| `GET` | `/api/events/{eventId}/intensity-distribution` | Probability distribution across IMD intensity categories | Event Monitor |
| `GET` | `/api/events/{eventId}/risk-alerts` | Downstream CAP-compliant warning alerts (snake_case) | Event Monitor |
| `GET` | `/api/historical-events/` | Catalog of benchmark historical weather events | Historical Replay |
| `GET` | `/api/historical-events/comparison-modes` | Supported comparison baselines (GNN vs Numerical) | Historical Replay |
| `GET` | `/api/historical-events/{eventId}` | Replay telemetry for Super Cyclone Amphan, Biparjoy, etc. | Historical Replay |
| `GET` | `/api/historical-events/{eventId}/timeline` | Replayed temporal lifecycle steps | Historical Replay |
| `GET` | `/api/historical-events/{eventId}/track` | Ground-truth track vs Prahari replayed model track | Historical Replay |
| `GET` | `/api/historical-events/{eventId}/hazard-envelope`| Storm surge height, inundation area, & wind swaths | Historical Replay |
| `GET` | `/api/historical-events/{eventId}/map-layers` | Composite reflectivity, wind vectors, & surge masks | Historical Replay |
| `GET` | `/api/historical-events/{eventId}/metrics` | Landfall timing error and skill scores | Historical Replay |
| `GET` | `/api/event-detail/events` | List of event detail options | Event Detail |
| `GET` | `/api/event-detail/{eventId}` | Primary event details and affected administrative districts | Event Detail |
| `GET` | `/api/event-detail/{eventId}/overview` | Synopsis and evacuation priority | Event Detail |
| `GET` | `/api/event-detail/{eventId}/map` | Interactive map coordinates, zoom level, & radar overlays | Event Detail |
| `GET` | `/api/event-detail/{eventId}/metrics` | Sustained winds, gusts, and storm surge estimates | Event Detail |
| `GET` | `/api/event-detail/{eventId}/hazard` | Infrastructure risk zones (ports, transmission lines) | Event Detail |
| `GET` | `/api/event-detail/{eventId}/alerts` | Active CAP emergency alerts with urgency and severity | Event Detail |
| `GET` | `/api/radar/stations` | Doppler Weather Radar stations metadata | Doppler Radar |
| `GET` | `/api/radar/{stationId}/frames` | Scanned Doppler frames with `from`, `to`, `limit` filtering | Doppler Radar |
| `GET` | `/api/radar/{stationId}/latest` | Most recent single Doppler frame | Doppler Radar |
| `GET` | `/static/radar/{station}/{product}/{file}`| Binary Doppler radar image file download (`image/png`) | Static Radar |

---

## 4. Quickstart & Verification Runbook (Windows PowerShell)

### Step 1: Environment Setup
```powershell
# Navigate into the project folder
cd "d:\projects\mock prahari\prahari-mock-server"

# Initialize virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Launch the FastAPI Mock Server
```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
> **Interactive Documentation:** Once started, open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser to test endpoints interactively via Swagger UI.

### Step 3: Run Doppler Radar Ingestion (Single Sweep or Daemon)
In a separate terminal:
```powershell
# Run a single capture sweep (with fallback/simulation for offline environments)
python scripts\capture_radar.py --once --simulate

# Run continuous background daemon polling every 10 minutes (600s)
python scripts\capture_radar.py --interval 600
```

### Step 4: Run Automated Verification Tests
```powershell
# Execute complete unit and integration test suites
python tests\test_phase2.py
python tests\test_phase3.py
python tests\test_phase4.py
python tests\test_phase5.py
python tests\test_phase6.py

# Run comprehensive end-to-end benchmark across all 43 endpoints
powershell -ExecutionPolicy Bypass -File scripts\test_all_endpoints.ps1
```

---

## 5. Post-Hackathon Migration Architecture & Swap Strategy

When transitioning from the mock prototype to the **production Prahari real-time inference platform**, the codebase is architected for zero-downtime, modular component swapping without altering frontend TypeScript contracts.

```text
┌───────────────────────────────────────────────────────────────┐
│                    Frontend (React / Vite)                    │
│             Standard REST & WebSocket Client API              │
└───────────────────────────────▲───────────────────────────────┘
                                │ HTTP / JSON (Unchanged Routes)
┌───────────────────────────────┴───────────────────────────────┐
│               FastAPI Application Layer (Gateway)             │
│            CORS • Rate Limiting • Authentication • Routers     │
└───────┬───────────────────────┬───────────────────────────────┘
        │                       │
   (Reads Data)           (Submits Jobs)
        │                       │
┌───────▼──────────────┐ ┌──────▼───────────────────────────────┐
│ PostGIS Database     │ │ Redis / Celery Task Queue            │
│ (Spatial Polygons,   │ └──────────────────────┬───────────────┘
│  Events, CAP Alerts, │                        │
│  Radar Station Meta) │           ┌────────────▼──────────────┐
└──────────────────────┘           │ Async ML Inference Workers│
                                   │ (NVIDIA H100 / TensorRT)  │
                                   │ • Stage 1: Mesh-GNN 12km  │
                                   │ • Stage 2: Diffusion 5km  │
                                   └────────────┬──────────────┘
                                                │ Writes
                                   ┌────────────▼──────────────┐
                                   │ Object Storage (S3 / GCS) │
                                   │ NetCDF4 / Zarr / Cloud-   │
                                   │ Optimized GeoTIFF (COG)   │
                                   └────────────┬──────────────┘
                                                │ Dynamic Tiles
                                   ┌────────────▼──────────────┐
                                   │ TiTiler / GeoServer Tile  │
                                   │ Map Services (WMS/WMTS)   │
                                   └───────────────────────────┘
```

### Migration Roadmap: Step-by-Step

#### 1. Database Layer: Replacing `app/loader.py` with SQLAlchemy & PostGIS
- **Current State:** Reads JSON files from `data/` using `load_json` and `load_keyed_json`.
- **Target State:**
  - Introduce **PostgreSQL with PostGIS** for spatial data.
  - Convert `data/eventDetail/hazard.json` and `data/historicalReplay/hazardEnvelope.json` into PostGIS geometries (`Polygon`, `MultiPolygon`) with spatial indexing (`GIST`).
  - Replace `load_json` in routers with asynchronous ORM sessions:
    ```python
    @router.get("/overview")
    async def get_overview(db: AsyncSession = Depends(get_db)):
        return await db.scalars(select(DashboardOverview)).first()
    ```

#### 2. Model Inference Pipeline: Connecting Celery / Redis Workers
- **Current State:** Returns static model analysis predictions and execution timing fixtures.
- **Target State:**
  - Atmospheric data from IMD/NCMRWF (NetCDF format) triggers an ingestion worker.
  - Tasks dispatched to a Celery worker pool running PyTorch with NVIDIA TensorRT execution providers.
  - Stage 1 Spherical GNN predicts trajectory tensors.
  - Stage 2 Conditional Diffusion model generates 5km high-resolution precipitation and wind speed arrays.
  - Execution latencies recorded directly into telemetry tables.

#### 3. High-Resolution Tensor Grids: NetCDF, Zarr & Cloud-Optimized GeoTIFFs (COG)
- **Current State:** Discrete waypoints and scalar metrics served via JSON.
- **Target State:**
  - High-resolution weather grids are packaged as **Cloud-Optimized GeoTIFFs (COG)** or **Zarr hierarchies** stored in S3/MinIO.
  - Deploy **TiTiler** (or FastAPI dynamic tile endpoints) serving XYZ map tiles (`/api/tiles/{z}/{x}/{y}.png`) directly into Mapbox GL / Leaflet on the frontend.
  - Retain all existing summary and KPI endpoints so frontend UI components continue operating without modification.

#### 4. Real-Time Emergency Alerts: WebSocket & CAP Push Engine
- **Current State:** Polling `/api/events/{eventId}/risk-alerts` via REST.
- **Target State:**
  - Connect a WebSocket channel (`/ws/alerts`) streaming CAP 1.2 XML/JSON alerts when EFI thresholds exceed `0.85`.
  - Automated integration with National Disaster Management Authority (NDMA) Sachet portal endpoints.

---

## 6. License & Contributors
Developed for **Smart India Hackathon 2026 (Problem Statement 26078)**.
Project **Prahari** — Advancing National Extreme Weather Resilience through Artificial Intelligence.
