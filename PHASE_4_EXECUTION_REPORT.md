# PHASE 4 EXECUTION REPORT: Doppler Radar Image Scanning & Static Serving

### 1. File Inventory & Modifications
| Path | Action | Purpose |
|---|---|---|
| `data/radar/stations.json` | Created | Doppler radar station metadata (Kolkata, Paradip, Agartala) |
| `app/radar_scanner.py` | Created | Scanner utility with regex timestamp parsing, sorting, and time filtering |
| `app/routers/radar.py` | Created | API router for `/api/radar/stations`, `/{stationId}/frames`, and `/{stationId}/latest` |
| `app/main.py` | Modified | Mounted static files under `/static/radar` and included radar router |
| `data/radar/kolkata/reflectivity/*.png` | Created | 3 sample timestamped reflectivity Doppler frames |
| `data/radar/kolkata/velocity/*.png` | Created | 1 sample timestamped velocity Doppler frame |
| `data/radar/agartala/reflectivity/` | Created | Empty directory to test zero-frame responses |
| `tests/test_phase4.py` | Created | Automated test suite verifying sorting, parsing, filters, and static file serving |

---

### 2. Directory Structure of `data/radar/`
```text
data/radar/
├── stations.json
├── agartala/
│   └── reflectivity/
├── kolkata/
│   ├── reflectivity/
│   │   ├── kolkata_reflectivity_20260928T1200Z.png
│   │   ├── kolkata_reflectivity_20260928T1230Z.png
│   │   └── kolkata_reflectivity_20260928T1300Z.png
│   └── velocity/
│       └── kolkata_velocity_20260928T1300Z.png
└── paradip/
```

---

### 3. Doppler Radar Endpoints & Sample Responses

#### `GET /api/radar/stations`
Returns list of registered IMD radar stations.
```json
[
  {
    "id": "kolkata",
    "name": "Kolkata (Subhash Chandra Bose AP)",
    "latitude": 22.65,
    "longitude": 88.45,
    "rangeKm": 250,
    "products": ["reflectivity", "velocity"]
  },
  {
    "id": "paradip",
    "name": "Paradip Port",
    "latitude": 20.31,
    "longitude": 86.61,
    "rangeKm": 250,
    "products": ["reflectivity", "velocity"]
  },
  {
    "id": "agartala",
    "name": "Agartala",
    "latitude": 23.88,
    "longitude": 91.24,
    "rangeKm": 250,
    "products": ["reflectivity"]
  }
]
```

#### `GET /api/radar/kolkata/frames?product=reflectivity`
Returns chronologically sorted frames (oldest to newest) with web-safe forward-slash URLs:
```json
{
  "stationId": "kolkata",
  "product": "reflectivity",
  "source": "IMD Doppler Weather Radar",
  "frames": [
    {
      "id": "kolkata_reflectivity_20260928T1200Z",
      "timestamp": "2026-09-28T12:00:00Z",
      "imageUrl": "/static/radar/kolkata/reflectivity/kolkata_reflectivity_20260928T1200Z.png"
    },
    {
      "id": "kolkata_reflectivity_20260928T1230Z",
      "timestamp": "2026-09-28T12:30:00Z",
      "imageUrl": "/static/radar/kolkata/reflectivity/kolkata_reflectivity_20260928T1230Z.png"
    },
    {
      "id": "kolkata_reflectivity_20260928T1300Z",
      "timestamp": "2026-09-28T13:00:00Z",
      "imageUrl": "/static/radar/kolkata/reflectivity/kolkata_reflectivity_20260928T1300Z.png"
    }
  ]
}
```

#### `GET /api/radar/kolkata/latest?product=reflectivity`
Returns the single most recent frame:
```json
{
  "id": "kolkata_reflectivity_20260928T1300Z",
  "timestamp": "2026-09-28T13:00:00Z",
  "imageUrl": "/static/radar/kolkata/reflectivity/kolkata_reflectivity_20260928T1300Z.png"
}
```

---

### 4. Filename Parsing, Sorting & Filtering Verification
- **Regex Pattern:** `^(?P<station>[a-zA-Z0-9_-]+)_(?P<product>[a-zA-Z0-9_-]+)_(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})T(?P<hour>\d{2})(?P<minute>\d{2})Z\.(?:png|jpg|jpeg)$`
- **ISO Conversion:** Converted `20260928T1300Z` to ISO 8601 string `2026-09-28T13:00:00Z`.
- **Chronological Sorting:** Verified frames are returned in ascending order (`12:00` -> `12:30` -> `13:00`).
- **Time Filtering:**
  - `from=2026-09-28T12:30:00Z` returns 2 frames (`12:30` and `13:00`).
  - `to=2026-09-28T12:30:00Z` returns 2 frames (`12:00` and `12:30`).
- **Limit Slicing:** `limit=1` returns the single newest frame.
- **Empty Frames Handling:** Stations with no images (such as `agartala`) return `200 OK` with `frames: []`. Calling `/latest` on an empty station returns `404 Not Found`.

---

### 5. Static File Serving Verification
Static files are mounted at `/static/radar` mapped directly to `data/radar/`:
- **URL Tested:** `GET /static/radar/kolkata/reflectivity/kolkata_reflectivity_20260928T1300Z.png`
- **Response Status:** `200 OK`
- **Content-Type Header:** `image/png`
- **Forward Slash Consistency:** All generated image URLs strictly use forward slashes (`/`) across Windows and Unix platforms.

---

### 6. Automated Test Suite Results (`tests/test_phase4.py`)
```text
PASS: /api/radar/stations lists valid stations
PASS: /api/radar/kolkata/frames sorted chronologically with forward-slash URLs
PASS: from filter works correctly
PASS: to filter works correctly
PASS: limit parameter returns newest slice
PASS: /api/radar/kolkata/latest returns newest frame
PASS: Static PNG file served with image/png MIME type
PASS: Unknown station cleanly returns 404
PASS: Unsupported product cleanly returns 404
PASS: Station with no images returns 200 with empty frames array
PASS: /latest on station with no images returns 404

ALL PHASE 4 TESTS PASSED SUCCESSFULLY!
```

---

### 7. PowerShell Verification Runbook

Run these commands in PowerShell against the active Uvicorn server (`http://127.0.0.1:8000`):

```powershell
# 1. Fetch radar stations
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/radar/stations" -Method Get

# 2. Fetch frames for Kolkata (reflectivity)
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/radar/kolkata/frames?product=reflectivity" -Method Get

# 3. Fetch latest single frame
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/radar/kolkata/latest?product=reflectivity" -Method Get

# 4. Fetch frames with time filtering and limit
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/radar/kolkata/frames?product=reflectivity&from=2026-09-28T12:30:00Z&limit=1" -Method Get

# 5. Verify static PNG download with HTTP headers
curl.exe -I "http://127.0.0.1:8000/static/radar/kolkata/reflectivity/kolkata_reflectivity_20260928T1300Z.png"
```
