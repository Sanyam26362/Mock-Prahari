# Render Native Python Deployment Preparation & Verification Report

**Project:** Prahari Extreme Weather Intelligence API (SIH 2026, PS 26078)  
**Target Environment:** Render Cloud Platform (Native Python Web Service)  
**Date:** September 2026  
**Status:** Verification Passed & Production-Ready  

---

## 1. Executive Summary

This report documents the preparation, hardening, and deployment configuration for running the **Prahari Extreme Weather Intelligence Mock Server** as a native Python Web Service on **Render**.

All operational requirements—including universal CORS (`*`) propagation, dynamic `$PORT` environment variable binding with local fallback, Unix LF line endings enforcement, infrastructure blueprint creation (`render.yaml`), and zero-regression test verification—have been completed.

---

## 2. Technical Modifications & Implementations

### 2.1 Universal CORS Configuration (`app/main.py`)
`CORSMiddleware` has been verified and enforced with wildcard access across all API endpoints:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
- **External Frontends:** Eliminates cross-origin blocking for frontends hosted on Vercel, Netlify, Render, GitHub Pages, or localhost (`3000`, `5173`).
- **Header Reflection:** Complies with Starlette/FastAPI CORS specifications by dynamically reflecting the caller's origin while allowing credentialed requests.

### 2.2 Dynamic Port Resolution (`start.sh`)
Render dynamically allocates a port for each container instance via the `$PORT` environment variable. The entrypoint script `start.sh` has been upgraded:

```bash
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
```
- **Port Flexibility:** Automatically adopts `$PORT` in Render cloud (e.g., `10000`), `$PORT=7860` in Hugging Face / Docker, or defaults to `8000` in local developer shells.
- **Root/Subdirectory Agnostic:** Automatically checks if `prahari-mock-server/` subfolder exists and navigates into it, ensuring execution succeeds whether the user configures Render root directory or leaves it blank.
- **Background Doppler Harvester:** Launches `capture_radar.py --interval 600 --simulate &` asynchronously before invoking Uvicorn.
- **Signal Handling:** Uses `exec uvicorn` to replace the shell process as PID 1, ensuring SIGTERM / SIGINT shutdown signals from Render orchestrators are received cleanly.
- **Line Endings:** Unix `LF` formatting strictly validated and locked via `.gitattributes` (`*.sh text eol=lf`).

### 2.3 Render Blueprint (`render.yaml`)
Added `render.yaml` infrastructure-as-code specification for automated Render service creation:

```yaml
services:
  - type: web
    name: prahari-mock-server
    runtime: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: bash start.sh
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.9
      - key: MOCK_LATENCY
        value: "true"
      - key: MOCK_LATENCY_MIN_MS
        value: "150"
      - key: MOCK_LATENCY_MAX_MS
        value: "450"
```

---

## 3. Test Suite Regression Results

All existing unit and integration test suites were executed sequentially:

| Test Suite | Result | Key Capabilities Verified |
|:---|:---:|:---|
| `tests/test_phase2.py` | **PASS (100%)** | Dashboard endpoints (overview, KPIs, anomalies, timeline, pipeline), 404/400 validation, CORS reflection. |
| `tests/test_phase3.py` | **PASS (100%)** | Model analysis, event monitor, historical replay, case-insensitive ID lookups, OpenAPI tags. |
| `tests/test_phase4.py` | **PASS (100%)** | Radar station directory scanner, ISO-8601 sorting, `/frames` filtering, static PNG streaming. |
| `tests/test_phase5.py` | **PASS (100%)** | System consistency validator (4 rules, 0 issues), artificial latency simulation & health route bypass. |
| `tests/test_phase6.py` | **PASS (100%)** | Doppler radar harvester simulation sweep, hot frame discovery, README operational coverage. |
| `tests/test_hf_prep.py` | **PASS (100%)** | Docker security directives, non-root user setup, YAML frontmatter, dynamic port resolution. |

**Zero regressions detected.**

---

## 4. Git Deployment & Repository Status

- **Remote:** `origin` &rarr; `https://github.com/Sanyam26362/Mock-Prahari.git`
- **Branch:** `main`
- **Commit Type:** `chore(deploy)`
- **Commit Subject:** `prepare configuration for render native python and enable universal cors`

---

## 5. Render Dashboard Setup Reference

When creating the Web Service on the Render Dashboard, enter the following parameters:

| Render Setting | Value to Enter | Notes |
|:---|:---|:---|
| **Service Type** | Web Service | Native Python application |
| **Repository** | `https://github.com/Sanyam26362/Mock-Prahari` | Connected GitHub repo |
| **Name** | `prahari-mock-server` | Service identifier |
| **Region** | Singapore (or closest) | Free tier available |
| **Branch** | `main` | Production branch |
| **Runtime** | `Python 3` | Python runtime |
| **Build Command** | `pip install -r requirements.txt` | Installs FastAPI & Uvicorn |
| **Start Command** | `bash start.sh` | Launches daemon & ASGI server |
| **Instance Type** | `Free` | 512 MB RAM, shared CPU |

### Environment Variables on Render
Set under **Environment** tab:

| Key | Value | Purpose |
|:---|:---|:---|
| `PYTHON_VERSION` | `3.11.9` | Locks Python version on Render build machine |
| `MOCK_LATENCY` | `true` | Enables realistic cloud network latency emulation |
| `MOCK_LATENCY_MIN_MS` | `150` | Minimum artificial latency |
| `MOCK_LATENCY_MAX_MS` | `450` | Maximum artificial latency |

---

## 6. Live Verification & API Endpoints

Once deployed, the live API will be accessible at:
```text
https://<your-service-name>.onrender.com/api
```

### Verification Commands
```bash
# 1. Health check
curl https://<your-service-name>.onrender.com/api/health

# 2. Interactive Swagger UI
# Open in browser: https://<your-service-name>.onrender.com/docs

# 3. Doppler radar frames
curl https://<your-service-name>.onrender.com/api/radar/kolkata/frames?product=reflectivity

# 4. Cyclone telemetry
curl https://<your-service-name>.onrender.com/api/events/BOB-02/telemetry
```

### Frontend Integration
Set in your React `.env`:
```env
VITE_API_BASE_URL=https://<your-service-name>.onrender.com/api
```
