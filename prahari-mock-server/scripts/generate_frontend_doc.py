import json
from pathlib import Path

BASE_RENDER_URL = "https://mock-prahari.onrender.com"

with open("captured_responses.json", "r", encoding="utf-8") as f:
    responses = json.load(f)

doc_lines = []

def add(line=""):
    doc_lines.append(line)

add("# Prahari API Documentation & Frontend Integration Reference")
add()
add("> **Live Production API:** [`https://mock-prahari.onrender.com`](https://mock-prahari.onrender.com)  ")
add("> **Interactive Swagger UI:** [`https://mock-prahari.onrender.com/docs`](https://mock-prahari.onrender.com/docs)  ")
add("> **OpenAPI JSON Spec:** [`https://mock-prahari.onrender.com/openapi.json`](https://mock-prahari.onrender.com/openapi.json)  ")
add("> **Target Platform:** Smart India Hackathon (SIH 2026) | Problem Statement: PS 26078  ")
add()
add("---")
add()
add("## 1. Quick Start for Frontend Developers")
add()
add("This backend is fully deployed, operational, and publicly accessible on Render. All endpoints support **Universal CORS** (`allow_origins=[\"*\"]`), meaning you can call this API directly from `localhost:5173`, `localhost:3000`, Vercel, Netlify, or GitHub Pages without browser blocks.")
add()
add("### 1.1 Environment Variable Setup")
add("Create or update your `.env` file in your React / Next.js / Vite project:")
add("```env")
add(f"VITE_API_BASE_URL={BASE_RENDER_URL}/api")
add(f"VITE_STATIC_BASE_URL={BASE_RENDER_URL}")
add("```")
add()
add("### 1.2 Base API Client (Axios / Fetch Example)")
add("```typescript")
add("// src/api/client.ts")
add("import axios from 'axios';")
add()
add("export const apiClient = axios.create({")
add(f"  baseURL: import.meta.env.VITE_API_BASE_URL || '{BASE_RENDER_URL}/api',")
add("  timeout: 10000,")
add("  headers: {")
add("    'Content-Type': 'application/json',")
add("  },")
add("});")
add("```")
add()
add("### 1.3 Latency Emulation Note")
add("The mock server runs an **Artificial Latency Middleware** (150ms–450ms) to emulate real-world satellite ingestion and graph neural network computation times. Use this to verify loading spinners, skeleton states, and optimistic UI transitions on the frontend.")
add()
add("---")
add()
add("## 2. API Endpoint Directory")
add()
add("| # | Module | Method | Endpoint | Description |")
add("|:---:|:---|:---:|:---|:---|")

catalog = [
    # System
    ("1", "System", "GET", "/api/health", "Liveness probe for health checks"),
    ("2", "System", "GET", "/api/system-status", "Operational status of pipelines & telemetry"),
    # Dashboard
    ("3", "Dashboard", "GET", "/api/dashboard/overview", "Basin-wide weather summary & storm count"),
    ("4", "Dashboard", "GET", "/api/dashboard/kpis", "Core platform KPIs (accuracy, lead time)"),
    ("5", "Dashboard", "GET", "/api/dashboard/anomaly-overview", "High-level summary of active anomalies"),
    ("6", "Dashboard", "GET", "/api/dashboard/active-anomalies", "List of regional weather anomalies"),
    ("7", "Dashboard", "GET", "/api/dashboard/forecast-timeline", "Multi-day basin forecast timeline"),
    ("8", "Dashboard", "GET", "/api/dashboard/processing-pipeline", "AI inference stages processing status"),
    # Model Analysis
    ("9", "Model Analysis", "GET", "/api/model-analysis/overview", "GNN + Diffusion hybrid AI overview"),
    ("10", "Model Analysis", "GET", "/api/model-analysis/models", "Registry of active deep learning models"),
    ("11", "Model Analysis", "GET", "/api/model-analysis/pipeline", "Tensor dataflow & mesh downscaling pipeline"),
    ("12", "Model Analysis", "GET", "/api/model-analysis/configuration", "Hyperparameters & spatial mesh resolution"),
    ("13", "Model Analysis", "GET", "/api/model-analysis/metrics", "RMSE, MAE, CRPS, and inference latencies"),
    ("14", "Model Analysis", "GET", "/api/model-analysis/verification", "Ensemble calibration & verification curves"),
    ("15", "Model Analysis", "GET", "/api/model-analysis/track-error-chart", "Track distance error vs forecast lead hours"),
    ("16", "Model Analysis", "GET", "/api/model-analysis/baseline-comparison", "Benchmark vs ECMWF-HRES & IMD-GFS"),
    # Event Monitor
    ("17", "Event Monitor", "GET", "/api/events/", "List of all actively monitored extreme events"),
    ("18", "Event Monitor", "GET", "/api/events/{eventId}", "Base metadata for a specific live event"),
    ("19", "Event Monitor", "GET", "/api/events/{eventId}/trajectory", "Cyclone eye coordinates & forecast cone track"),
    ("20", "Event Monitor", "GET", "/api/events/{eventId}/timeline", "Historical and forecasted intensity timeline"),
    ("21", "Event Monitor", "GET", "/api/events/{eventId}/telemetry", "Real-time central pressure, wind & speed"),
    ("22", "Event Monitor", "GET", "/api/events/{eventId}/diagnostics", "Vorticity, SST & vertical wind shear stats"),
    ("23", "Event Monitor", "GET", "/api/events/{eventId}/intensity-distribution", "Probability spread across cyclone categories"),
    ("24", "Event Monitor", "GET", "/api/events/{eventId}/risk-alerts", "Downstream coastal inundation & flood risks"),
    # Historical Replay
    ("25", "Historical Replay", "GET", "/api/historical-events/", "Historical cyclone archive (Amphan, Biparjoy)"),
    ("26", "Historical Replay", "GET", "/api/historical-events/comparison-modes", "Replay modes (Model vs Ground Truth)"),
    ("27", "Historical Replay", "GET", "/api/historical-events/{eventId}", "Selected historical event summary"),
    ("28", "Historical Replay", "GET", "/api/historical-events/{eventId}/timeline", "Historical time steps for scrubber slider"),
    ("29", "Historical Replay", "GET", "/api/historical-events/{eventId}/track", "Actual observed track vs predicted track"),
    ("30", "Historical Replay", "GET", "/api/historical-events/{eventId}/hazard-envelope", "Impact polygons & storm surge zones"),
    ("31", "Historical Replay", "GET", "/api/historical-events/{eventId}/map-layers", "GeoJSON layers for Leaflet/Mapbox maps"),
    ("32", "Historical Replay", "GET", "/api/historical-events/{eventId}/metrics", "Post-event verification metrics"),
    # Event Detail
    ("33", "Event Detail", "GET", "/api/event-detail/events", "List of selectable events for deep dive"),
    ("34", "Event Detail", "GET", "/api/event-detail/{eventId}", "Deep dive event overview & status"),
    ("35", "Event Detail", "GET", "/api/event-detail/{eventId}/overview", "Synoptic analysis & meteorological overview"),
    ("36", "Event Detail", "GET", "/api/event-detail/{eventId}/map", "Event map bounding box & observation stations"),
    ("37", "Event Detail", "GET", "/api/event-detail/{eventId}/metrics", "Event impact figures & population at risk"),
    ("38", "Event Detail", "GET", "/api/event-detail/{eventId}/hazard", "Terrain-aware hazard zones & rainfall bands"),
    ("39", "Event Detail", "GET", "/api/event-detail/{eventId}/alerts", "CAP-compliant disaster alert bulletins"),
    # Radar
    ("40", "Doppler Radar", "GET", "/api/radar/stations", "Doppler radar stations & operational metadata"),
    ("41", "Doppler Radar", "GET", "/api/radar/{stationId}/frames", "Chronological radar frames with time filtering"),
    ("42", "Doppler Radar", "GET", "/api/radar/{stationId}/latest", "Latest harvested radar frame for immediate view"),
    ("43", "Static Assets", "GET", "/static/radar/{station}/{product}/{filename}", "Direct PNG Doppler radar frame stream"),
]

for num, mod, meth, ep, desc in catalog:
    add(f"| {num} | {mod} | `{meth}` | `{ep}` | {desc} |")

add()
add("---")
add()

def render_endpoint_section(title, method, path, live_path, desc, params=None, sample_response=None, frontend_usage=None, ts_interface=None):
    add(f"### {title}")
    add(f"**Method:** `{method}`  ")
    add(f"**Path:** `{path}`  ")
    add(f"**Live Render URL:** [`{BASE_RENDER_URL}{live_path}`]({BASE_RENDER_URL}{live_path})  ")
    add()
    add(f"**Description:** {desc}")
    add()
    if params:
        add("**Parameters:**")
        add("| Name | Type | In | Required | Description |")
        add("|:---|:---|:---|:---:|:---|")
        for p in params:
            add(f"| `{p[0]}` | `{p[1]}` | {p[2]} | {'Yes' if p[3] else 'No'} | {p[4]} |")
        add()
    else:
        add("**Parameters:** None")
        add()
    
    add("**Request Body:** None (`GET` request)")
    add()
    
    if sample_response:
        add("**Sample Live Response Body (`200 OK`):**")
        add("```json")
        add(json.dumps(sample_response, indent=2))
        add("```")
        add()
    
    if frontend_usage:
        add(f"**Frontend Usage:** {frontend_usage}")
        add()
    
    if ts_interface:
        add("**TypeScript Interface:**")
        add("```typescript")
        add(ts_interface)
        add("```")
        add()
    add("---")
    add()

# Section 3: Detailed Endpoint Breakdown
add("## 3. Comprehensive Endpoint Reference & Payloads")
add()

# 1. Health
render_endpoint_section(
    title="1. Health Check",
    method="GET",
    path="/api/health",
    live_path="/api/health",
    desc="Liveness probe to verify if the server is healthy and responding. Bypasses artificial latency.",
    sample_response=responses.get("/api/health"),
    frontend_usage="Use in an application startup check or status badge (e.g. green status dot in the navbar).",
    ts_interface="""export interface HealthResponse {
  status: string;
}"""
)

# 2. System Status
render_endpoint_section(
    title="2. Operational System Status",
    method="GET",
    path="/api/system-status",
    live_path="/api/system-status",
    desc="Retrieves operational system diagnostics, active AI pipeline readiness, and cluster compute statistics.",
    sample_response=responses.get("/api/system-status"),
    frontend_usage="Use in the System Diagnostics drawer, footer health indicator, or Ops Dashboard.",
    ts_interface="""export interface SystemStatusResponse {
  system: string;
  status: 'OPERATIONAL' | 'DEGRADED' | 'MAINTENANCE';
  timestamp: string;
  cluster: {
    gpuNodesAvailable: number;
    activeInferenceThreads: number;
    memoryAllocatedGB: number;
  };
  pipelineStatus: {
    sphericalGnnStage1: string;
    diffusionDownscalingStage2: string;
    dopplerHarvesterDaemon: string;
  };
}"""
)

# 3. Dashboard Overview
render_endpoint_section(
    title="3. Dashboard Overview",
    method="GET",
    path="/api/dashboard/overview",
    live_path="/api/dashboard/overview",
    desc="Basin-wide high-level overview of monitored Indian Ocean & Bay of Bengal regions.",
    sample_response=responses.get("/api/dashboard/overview"),
    frontend_usage="Top banner and synoptic weather summary cards on the Main Executive Dashboard.",
    ts_interface="""export interface DashboardOverviewResponse {
  basin: string;
  activeExtremeEvents: number;
  monitoredBasins: string[];
  alertLevel: 'RED' | 'ORANGE' | 'YELLOW' | 'GREEN';
  synopticSummary: string;
  lastUpdated: string;
}"""
)

# 4. Dashboard KPIs
render_endpoint_section(
    title="4. Dashboard KPIs",
    method="GET",
    path="/api/dashboard/kpis",
    live_path="/api/dashboard/kpis",
    desc="Key statistical metrics measuring forecast lead time, resolution, and model skill scores.",
    sample_response=responses.get("/api/dashboard/kpis"),
    frontend_usage="Top KPI grid cards (4-card metric row on the dashboard).",
    ts_interface="""export interface DashboardKPIsResponse {
  forecastResolutionKm: number;
  leadTimeHours: number;
  trackError24hKm: number;
  intensityRmseKnots: number;
  activeAlertCount: number;
  radarCoveragePercentage: number;
}"""
)

# 5. Dashboard Anomaly Overview
render_endpoint_section(
    title="5. Dashboard Anomaly Overview",
    method="GET",
    path="/api/dashboard/anomaly-overview",
    live_path="/api/dashboard/anomaly-overview",
    desc="High-level breakdown of severe meteorological anomalies segmented by hazard type.",
    sample_response=responses.get("/api/dashboard/anomaly-overview"),
    frontend_usage="Distribution doughnut / pie chart or summary pills on the dashboard.",
    ts_interface="""export interface AnomalyOverviewResponse {
  totalAnomalies: number;
  cyclonicDepressions: number;
  extremePrecipitationZones: number;
  heatwavePockets: number;
  marineGales: number;
}"""
)

# 6. Dashboard Active Anomalies
render_endpoint_section(
    title="6. Dashboard Active Anomalies",
    method="GET",
    path="/api/dashboard/active-anomalies",
    live_path="/api/dashboard/active-anomalies",
    desc="Detailed list of currently tracked anomalies across India and neighboring oceanic basins.",
    sample_response=responses.get("/api/dashboard/active-anomalies"),
    frontend_usage="Active Anomalies table or scrollable alert cards on the dashboard overview.",
    ts_interface="""export interface AnomalyItem {
  id: string;
  type: string;
  region: string;
  severity: 'CRITICAL' | 'HIGH' | 'MODERATE' | 'LOW';
  coordinates: [number, number];
  efiValue: number;
}

export type ActiveAnomaliesResponse = AnomalyItem[];"""
)

# 7. Dashboard Forecast Timeline
render_endpoint_section(
    title="7. Dashboard Forecast Timeline",
    method="GET",
    path="/api/dashboard/forecast-timeline",
    live_path="/api/dashboard/forecast-timeline",
    desc="Multi-step chronological forecast sequence outlining storm path milestones.",
    sample_response=responses.get("/api/dashboard/forecast-timeline"),
    frontend_usage="Interactive horizontal timeline or slider on the dashboard.",
    ts_interface="""export interface TimelineStep {
  step: string;
  timestamp: string;
  expectedIntensity: string;
  windSpeedKmph: number;
  primaryRiskZone: string;
}

export type ForecastTimelineResponse = TimelineStep[];"""
)

# 8. Dashboard Processing Pipeline
render_endpoint_section(
    title="8. Dashboard Processing Pipeline",
    method="GET",
    path="/api/dashboard/processing-pipeline",
    live_path="/api/dashboard/processing-pipeline",
    desc="Status of real-time multi-stage inference workflows (Radar -> GNN -> Diffusion -> Alerting).",
    sample_response=responses.get("/api/dashboard/processing-pipeline"),
    frontend_usage="Dataflow architecture diagram or live operational pipeline indicator.",
    ts_interface="""export interface PipelineStage {
  stageId: string;
  name: string;
  latencyMs: number;
  status: 'ACTIVE' | 'IDLE' | 'COMPLETED';
}

export interface ProcessingPipelineResponse {
  pipelineId: string;
  totalLatencyMs: number;
  stages: PipelineStage[];
}"""
)

# 9. Model Analysis Overview
render_endpoint_section(
    title="9. Model Analysis Overview",
    method="GET",
    path="/api/model-analysis/overview",
    live_path="/api/model-analysis/overview",
    desc="Architectural overview of the two-stage hybrid Spherical GNN and Conditional Diffusion platform.",
    sample_response=responses.get("/api/model-analysis/overview"),
    frontend_usage="Model Analysis introductory panel and model metadata drawer.",
    ts_interface="""export interface ModelAnalysisOverviewResponse {
  architecture: string;
  stage1: string;
  stage2: string;
  inputVariables: string[];
  outputResolutionKm: number;
}"""
)

# 10. Model Analysis Models
render_endpoint_section(
    title="10. Model Registry List",
    method="GET",
    path="/api/model-analysis/models",
    live_path="/api/model-analysis/models",
    desc="Comprehensive list of active neural network checkpoints, parameter counts, and quantization states.",
    sample_response=responses.get("/api/model-analysis/models"),
    frontend_usage="Model switcher dropdown and neural network architecture specifications table.",
    ts_interface="""export interface ModelRecord {
  modelId: string;
  name: string;
  version: string;
  parameters: string;
  quantization: string;
  hardwareTarget: string;
}

export type ModelsResponse = ModelRecord[];"""
)

# 11. Model Analysis Pipeline
render_endpoint_section(
    title="11. Model Tensor Pipeline",
    method="GET",
    path="/api/model-analysis/pipeline",
    live_path="/api/model-analysis/pipeline",
    desc="Detailed tensor dimensions, mesh resolutions, and intermediate feature transformations.",
    sample_response=responses.get("/api/model-analysis/pipeline"),
    frontend_usage="Interactive tensor flow graph visualization.",
    ts_interface="""export interface PipelineStepDetail {
  stepOrder: number;
  component: string;
  inputShape: string;
  outputShape: string;
  computeType: string;
}

export interface ModelPipelineResponse {
  pipelineName: string;
  steps: PipelineStepDetail[];
}"""
)

# 12. Model Analysis Configuration
render_endpoint_section(
    title="12. Model Configuration & Hyperparameters",
    method="GET",
    path="/api/model-analysis/configuration",
    live_path="/api/model-analysis/configuration",
    desc="Runtime configuration parameters, diffusion timesteps, and spherical mesh subdivision levels.",
    sample_response=responses.get("/api/model-analysis/configuration"),
    frontend_usage="Configuration inspector card and model tuning readouts.",
    ts_interface="""export interface ModelConfigurationResponse {
  meshSubdivisionLevel: number;
  diffusionSteps: number;
  samplingMethod: string;
  temperature: number;
  ensembleMembers: number;
}"""
)

# 13. Model Analysis Metrics
render_endpoint_section(
    title="13. Model Skill Scores & Error Metrics",
    method="GET",
    path="/api/model-analysis/metrics",
    live_path="/api/model-analysis/metrics",
    desc="Quantitative statistical metrics measuring geopotential height RMSE, wind speed MAE, and CRPS.",
    sample_response=responses.get("/api/model-analysis/metrics"),
    frontend_usage="Radar charts, bar graphs, and model accuracy comparison tables.",
    ts_interface="""export interface ModelMetricsResponse {
  geopotentialHeightRmseZ500: number;
  windSpeedMaeU10: number;
  crpsPrecipitation: number;
  meanInferenceTimeMs: number;
}"""
)

# 14. Model Analysis Verification
render_endpoint_section(
    title="14. Model Ensemble Verification",
    method="GET",
    path="/api/model-analysis/verification",
    live_path="/api/model-analysis/verification",
    desc="Ensemble calibration curve data, spread-error ratios, and probability reliability metrics.",
    sample_response=responses.get("/api/model-analysis/verification"),
    frontend_usage="Calibration curve and reliability diagram plots (Chart.js / Recharts).",
    ts_interface="""export interface VerificationPoint {
  forecastProbability: number;
  observedFrequency: number;
}

export interface ModelVerificationResponse {
  metricName: string;
  spreadSkillRatio: number;
  curve: VerificationPoint[];
}"""
)

# 15. Model Analysis Track Error Chart
render_endpoint_section(
    title="15. Track Error Chart Data",
    method="GET",
    path="/api/model-analysis/track-error-chart",
    live_path="/api/model-analysis/track-error-chart",
    desc="Cyclone center position displacement error (km) across 12h, 24h, 48h, and 72h lead times.",
    sample_response=responses.get("/api/model-analysis/track-error-chart"),
    frontend_usage="Forecast lead time track error line chart (Prahari vs NWP baselines).",
    ts_interface="""export interface TrackErrorPoint {
  leadHours: number;
  prahariErrorKm: number;
  baselineErrorKm: number;
}

export type TrackErrorChartResponse = TrackErrorPoint[];"""
)

# 16. Model Analysis Baseline Comparison
render_endpoint_section(
    title="16. Baseline Model Benchmarks",
    method="GET",
    path="/api/model-analysis/baseline-comparison",
    live_path="/api/model-analysis/baseline-comparison",
    desc="Direct side-by-side benchmark comparison: Prahari vs ECMWF-HRES and IMD-GFS.",
    sample_response=responses.get("/api/model-analysis/baseline-comparison"),
    frontend_usage="Model comparison table and radar comparison benchmark.",
    ts_interface="""export interface BaselineModelStat {
  model: string;
  resolutionKm: number;
  inferenceLatencyMinutes: number;
  trackError24hKm: number;
  computeCostUsdPerRun: number;
}

export type BaselineComparisonResponse = BaselineModelStat[];"""
)

# 17. Event Monitor - List Events
render_endpoint_section(
    title="17. List Active Monitored Events",
    method="GET",
    path="/api/events/",
    live_path="/api/events/",
    desc="Retrieves the list of active cyclone and severe weather events currently under live monitoring.",
    sample_response=responses.get("/api/events/"),
    frontend_usage="Event selector dropdown at the top of the Live Cyclone Monitor page.",
    ts_interface="""export interface MonitoredEventSummary {
  eventId: string;
  name: string;
  category: string;
  basin: string;
  status: 'ACTIVE' | 'WATCH' | 'DISSIPATING';
  currentWindSpeedKmph: number;
}

export type EventListResponse = MonitoredEventSummary[];"""
)

# 18. Event Monitor - Event Base Info
render_endpoint_section(
    title="18. Live Event Base Details",
    method="GET",
    path="/api/events/{eventId}",
    live_path="/api/events/BOB-02",
    desc="Detailed current status, classification, and geographical position of the specified event.",
    params=[("eventId", "string", "path", True, "Identifier of the event (e.g. `BOB-02`, case-insensitive)")],
    sample_response=responses.get("/api/events/BOB-02"),
    frontend_usage="Header card and title display on the Live Event Monitor page.",
    ts_interface="""export interface LiveEventDetailsResponse {
  eventId: string;
  name: string;
  classification: string;
  formationDate: string;
  currentCoordinates: {
    lat: number;
    lng: number;
  };
  centralPressureHpa: number;
  sustainedWindKmph: number;
  gustsKmph: number;
}"""
)

# 19. Event Monitor - Trajectory
render_endpoint_section(
    title="19. Event Trajectory & Forecast Cone",
    method="GET",
    path="/api/events/{eventId}/trajectory",
    live_path="/api/events/BOB-02/trajectory",
    desc="Observed coordinates, past track points, and probabilistic forecast cone coordinates with timestamps.",
    params=[("eventId", "string", "path", True, "Event ID (e.g. `BOB-02`)")],
    sample_response=responses.get("/api/events/BOB-02/trajectory"),
    frontend_usage="Primary Leaflet / Mapbox track polyline and uncertainty cone layer on the monitor map.",
    ts_interface="""export interface TrackPoint {
  timestamp: string;
  lat: number;
  lng: number;
  windSpeedKts: number;
  pressureHpa: number;
  pointType: 'OBSERVED' | 'FORECAST';
}

export interface TrajectoryResponse {
  eventId: string;
  track: TrackPoint[];
  forecastConePolygon?: [number, number][];
}"""
)

# 20. Event Monitor - Timeline
render_endpoint_section(
    title="20. Event Intensity Timeline",
    method="GET",
    path="/api/events/{eventId}/timeline",
    live_path="/api/events/BOB-02/timeline",
    desc="Time series of central pressure (hPa) and sustained wind speed (knots) through landfall.",
    params=[("eventId", "string", "path", True, "Event ID (e.g. `BOB-02`)")],
    sample_response=responses.get("/api/events/BOB-02/timeline"),
    frontend_usage="Dual-axis pressure vs wind speed line chart.",
    ts_interface="""export interface IntensityPoint {
  timestamp: string;
  windKnots: number;
  pressureHpa: number;
  stage: string;
}

export type EventTimelineResponse = IntensityPoint[];"""
)

# 21. Event Monitor - Telemetry
render_endpoint_section(
    title="21. Live Event Telemetry",
    method="GET",
    path="/api/events/{eventId}/telemetry",
    live_path="/api/events/BOB-02/telemetry",
    desc="High-frequency telemetry: forward speed, bearing direction, eye radius, and quadrant wind radii.",
    params=[("eventId", "string", "path", True, "Event ID (e.g. `BOB-02`)")],
    sample_response=responses.get("/api/events/BOB-02/telemetry"),
    frontend_usage="Live storm telemetry dashboard gauges (Speedometer, Compass, Radius dials).",
    ts_interface="""export interface TelemetryResponse {
  eventId: string;
  forwardSpeedKmph: number;
  headingDegrees: number;
  eyeRadiusKm: number;
  quadrantRadiiKm: {
    ne: number;
    se: number;
    sw: number;
    nw: number;
  };
}"""
)

# 22. Event Monitor - Diagnostics
render_endpoint_section(
    title="22. Meteorological Diagnostics",
    method="GET",
    path="/api/events/{eventId}/diagnostics",
    live_path="/api/events/BOB-02/diagnostics",
    desc="Atmospheric diagnostics: relative vorticity, Sea Surface Temperature (SST), and 850-200hPa wind shear.",
    params=[("eventId", "string", "path", True, "Event ID (e.g. `BOB-02`)")],
    sample_response=responses.get("/api/events/BOB-02/diagnostics"),
    frontend_usage="Environmental conditions cards and cyclogenesis potential bar meters.",
    ts_interface="""export interface DiagnosticsResponse {
  seaSurfaceTemperatureCelsius: number;
  verticalWindShearKnots: number;
  relativeVorticity850: number;
  upperLevelDivergence: number;
  environmentalFavorability: 'EXTREME' | 'HIGH' | 'MODERATE' | 'UNFAVORABLE';
}"""
)

# 23. Event Monitor - Intensity Distribution
render_endpoint_section(
    title="23. Intensity Category Probability Distribution",
    method="GET",
    path="/api/events/{eventId}/intensity-distribution",
    live_path="/api/events/BOB-02/intensity-distribution",
    desc="Probabilistic distribution across IMD cyclone classifications (CS, SCS, VSCS, ESCS, SuCS).",
    params=[("eventId", "string", "path", True, "Event ID (e.g. `BOB-02`)")],
    sample_response=responses.get("/api/events/BOB-02/intensity-distribution"),
    frontend_usage="Intensity likelihood probability bar chart or stacked probability meter.",
    ts_interface="""export interface IntensityProbability {
  category: string;
  description: string;
  probabilityPercentage: number;
}

export type IntensityDistributionResponse = IntensityProbability[];"""
)

# 24. Event Monitor - Risk Alerts
render_endpoint_section(
    title="24. Downstream Risk Alerts",
    method="GET",
    path="/api/events/{eventId}/risk-alerts",
    live_path="/api/events/BOB-02/risk-alerts",
    desc="Downstream coastal surge, storm tide inundation, and flash flood impact alerts by district.",
    params=[("eventId", "string", "path", True, "Event ID (e.g. `BOB-02`)")],
    sample_response=responses.get("/api/events/BOB-02/risk-alerts"),
    frontend_usage="District-level warning cards and alert badge feed.",
    ts_interface="""export interface RiskAlert {
  alertId: string;
  district: string;
  state: string;
  riskType: string;
  riskLevel: 'RED' | 'ORANGE' | 'YELLOW';
  peakImpactTime: string;
  estimatedSurgeHeightMeters?: number;
}

export type RiskAlertsResponse = RiskAlert[];"""
)

# 25. Historical Replay - Catalog
render_endpoint_section(
    title="25. Historical Events Archive",
    method="GET",
    path="/api/historical-events/",
    live_path="/api/historical-events/",
    desc="Retrieves the catalog of landmark historical events available for historical replay analysis.",
    sample_response=responses.get("/api/historical-events/"),
    frontend_usage="Historical event picker / carousel (Amphan 2020, Biparjoy 2023, Mumbai Deluge 2005).",
    ts_interface="""export interface HistoricalEventSummary {
  eventId: string;
  name: string;
  year: number;
  peakIntensity: string;
  landfallLocation: string;
  fatalitiesReported: number;
}

export type HistoricalEventsResponse = HistoricalEventSummary[];"""
)

# 26. Historical Replay - Comparison Modes
render_endpoint_section(
    title="26. Replay Comparison Modes",
    method="GET",
    path="/api/historical-events/comparison-modes",
    live_path="/api/historical-events/comparison-modes",
    desc="List of supported side-by-side comparison modes (Ground Truth vs Model, Diffusion vs Coarse NWP).",
    sample_response=responses.get("/api/historical-events/comparison-modes"),
    frontend_usage="Comparison mode toggle button group on the Replay player.",
    ts_interface="""export interface ComparisonMode {
  id: string;
  label: string;
  description: string;
  leftLayer: string;
  rightLayer: string;
}

export type ComparisonModesResponse = ComparisonMode[];"""
)

# 27. Historical Replay - Event Summary
render_endpoint_section(
    title="27. Selected Historical Event Overview",
    method="GET",
    path="/api/historical-events/{eventId}",
    live_path="/api/historical-events/amphan-2020",
    desc="Metadata, track span, and summary statistics of the chosen historical case study.",
    params=[("eventId", "string", "path", True, "Historical event slug (e.g. `amphan-2020`, case-insensitive)")],
    sample_response=responses.get("/api/historical-events/amphan-2020"),
    frontend_usage="Historical Case Study summary header and impact recap.",
    ts_interface="""export interface HistoricalEventDetailResponse {
  eventId: string;
  name: string;
  period: string;
  maxWindKnots: number;
  minPressureHpa: number;
  totalDamageUsdBillions: number;
  synopsis: string;
}"""
)

# 28. Historical Replay - Timeline
render_endpoint_section(
    title="28. Historical Replay Time Slices",
    method="GET",
    path="/api/historical-events/{eventId}/timeline",
    live_path="/api/historical-events/amphan-2020/timeline",
    desc="Chronological list of timestamp steps used to drive the replay scrubber and step-by-step playback.",
    params=[("eventId", "string", "path", True, "Historical event slug (e.g. `amphan-2020`)")],
    sample_response=responses.get("/api/historical-events/amphan-2020/timeline"),
    frontend_usage="Playback timeline scrubber slider and play/pause frame sequence.",
    ts_interface="""export interface ReplayTimeStep {
  stepIndex: number;
  timestamp: string;
  category: string;
  forwardSpeedKmph: number;
}

export type HistoricalTimelineResponse = ReplayTimeStep[];"""
)

# 29. Historical Replay - Track Comparison
render_endpoint_section(
    title="29. Observed vs Forecasted Track Comparison",
    method="GET",
    path="/api/historical-events/{eventId}/track",
    live_path="/api/historical-events/amphan-2020/track",
    desc="Synchronized coordinates of the actual observed path alongside the Prahari deep learning prediction.",
    params=[("eventId", "string", "path", True, "Historical event slug (e.g. `amphan-2020`)")],
    sample_response=responses.get("/api/historical-events/amphan-2020/track"),
    frontend_usage="Dual-polyline map overlay comparing ground truth vs prediction track accuracy.",
    ts_interface="""export interface TrackComparisonPoint {
  timestamp: string;
  observedLat: number;
  observedLng: number;
  predictedLat: number;
  predictedLng: number;
  trackErrorKm: number;
}

export type HistoricalTrackResponse = TrackComparisonPoint[];"""
)

# 30. Historical Replay - Hazard Envelope
render_endpoint_section(
    title="30. Historical Hazard Envelope Polygons",
    method="GET",
    path="/api/historical-events/{eventId}/hazard-envelope",
    live_path="/api/historical-events/amphan-2020/hazard-envelope",
    desc="Multi-polygon boundaries defining historical inundation zones, gale wind swaths, and tidal surges.",
    params=[("eventId", "string", "path", True, "Historical event slug (e.g. `amphan-2020`)")],
    sample_response=responses.get("/api/historical-events/amphan-2020/hazard-envelope"),
    frontend_usage="GeoJSON polygon overlay highlighting damaged land and surge reach on the map.",
    ts_interface="""export interface HazardPolygon {
  zoneName: string;
  hazardType: string;
  severityLevel: string;
  polygonCoordinates: [number, number][];
}

export type HazardEnvelopeResponse = HazardPolygon[];"""
)

# 31. Historical Replay - Map Layers
render_endpoint_section(
    title="31. Historical Map Layers & Rasters",
    method="GET",
    path="/api/historical-events/{eventId}/map-layers",
    live_path="/api/historical-events/amphan-2020/map-layers",
    desc="List of available raster overlays (wind field heatmaps, rain accumulation, satellite imagery) for replay.",
    params=[("eventId", "string", "path", True, "Historical event slug (e.g. `amphan-2020`)")],
    sample_response=responses.get("/api/historical-events/amphan-2020/map-layers"),
    frontend_usage="Map layer control toggles (Satellite, Wind Heatmap, Precipitation Overlay).",
    ts_interface="""export interface ReplayMapLayer {
  layerId: string;
  name: string;
  type: 'raster' | 'geojson' | 'vector';
  sourceUrl: string;
  opacity: number;
  defaultVisible: boolean;
}

export type ReplayMapLayersResponse = ReplayMapLayer[];"""
)

# 32. Historical Replay - Post-Event Metrics
render_endpoint_section(
    title="32. Historical Replay Accuracy Metrics",
    method="GET",
    path="/api/historical-events/{eventId}/metrics",
    live_path="/api/historical-events/amphan-2020/metrics",
    desc="Post-landfall verification statistics (Landfall point accuracy in km, timing error in hours).",
    params=[("eventId", "string", "path", True, "Historical event slug (e.g. `amphan-2020`)")],
    sample_response=responses.get("/api/historical-events/amphan-2020/metrics"),
    frontend_usage="Historical Case Study scorecard metrics.",
    ts_interface="""export interface HistoricalMetricsResponse {
  landfallLocationErrorKm: number;
  landfallTimingErrorHours: number;
  maxWindSpeedErrorKnots: number;
  centralPressureRmseHpa: number;
}"""
)

# 33. Event Detail - Events List
render_endpoint_section(
    title="33. Event Detail Selectable Events",
    method="GET",
    path="/api/event-detail/events",
    live_path="/api/event-detail/events",
    desc="Returns list of events selectable for full deep-dive operational investigation.",
    sample_response=responses.get("/api/event-detail/events"),
    frontend_usage="Event picker on the Detailed Event Investigation page.",
    ts_interface="""export interface EventDetailListItem {
  eventId: string;
  name: string;
  status: string;
  basin: string;
  alertLevel: string;
}

export type EventDetailEventsResponse = EventDetailListItem[];"""
)

# 34. Event Detail - Base
render_endpoint_section(
    title="34. Event Deep Dive Container",
    method="GET",
    path="/api/event-detail/{eventId}",
    live_path="/api/event-detail/BOB-02",
    desc="Full comprehensive container metadata for the selected investigation event.",
    params=[("eventId", "string", "path", True, "Event ID (e.g. `BOB-02`)")],
    sample_response=responses.get("/api/event-detail/BOB-02"),
    frontend_usage="Initial fetch when loading the Event Detail investigation view.",
    ts_interface="""export interface EventDetailContainerResponse {
  eventId: string;
  name: string;
  phase: string;
  coastalSectorsAtRisk: string[];
  bulletinNumber: number;
  issuedAt: string;
}"""
)

# 35. Event Detail - Overview
render_endpoint_section(
    title="35. Event Synoptic Overview",
    method="GET",
    path="/api/event-detail/{eventId}/overview",
    live_path="/api/event-detail/BOB-02/overview",
    desc="Synoptic weather analysis, atmospheric steering currents, and expected landfall progression.",
    params=[("eventId", "string", "path", True, "Event ID (e.g. `BOB-02`)")],
    sample_response=responses.get("/api/event-detail/BOB-02/overview"),
    frontend_usage="Executive briefing summary card on the Event Detail page.",
    ts_interface="""export interface EventDetailOverviewResponse {
  eventId: string;
  synopticSituation: string;
  steeringCurrentDescription: string;
  expectedLandfallWindow: string;
  estimatedWaveHeightMeters: number;
}"""
)

# 36. Event Detail - Map Layers
render_endpoint_section(
    title="36. Event Interactive Map Setup",
    method="GET",
    path="/api/event-detail/{eventId}/map",
    live_path="/api/event-detail/BOB-02/map",
    desc="Map viewport bounds, radar station coordinates, coastal telemetry buoys, and weather stations.",
    params=[("eventId", "string", "path", True, "Event ID (e.g. `BOB-02`)")],
    sample_response=responses.get("/api/event-detail/BOB-02/map"),
    frontend_usage="Map bounds initialization (`fitBounds`) and observation markers.",
    ts_interface="""export interface ObservationStation {
  id: string;
  name: string;
  type: 'radar' | 'buoy' | 'coastal_station';
  lat: number;
  lng: number;
}

export interface EventDetailMapResponse {
  defaultBounds: {
    north: number;
    south: number;
    east: number;
    west: number;
  };
  observationStations: ObservationStation[];
}"""
)

# 37. Event Detail - Metrics
render_endpoint_section(
    title="37. Event Impact Figures & Metrics",
    method="GET",
    path="/api/event-detail/{eventId}/metrics",
    live_path="/api/event-detail/BOB-02/metrics",
    desc="Socio-economic and physical vulnerability metrics: population at risk, port closures, expected rainfall.",
    params=[("eventId", "string", "path", True, "Event ID (e.g. `BOB-02`)")],
    sample_response=responses.get("/api/event-detail/BOB-02/metrics"),
    frontend_usage="Disaster impact stats row (Evacuations needed, Ports impacted, 24h peak rain).",
    ts_interface="""export interface EventDetailMetricsResponse {
  estimatedPopulationAtRisk: number;
  peak24hRainfallMm: number;
  stormSurgeHeightMeters: number;
  majorPortsInWarningZone: string[];
}"""
)

# 38. Event Detail - Hazard Polygons
render_endpoint_section(
    title="38. High-Resolution Hazard Zones",
    method="GET",
    path="/api/event-detail/{eventId}/hazard",
    live_path="/api/event-detail/BOB-02/hazard",
    desc="Multi-level hazard zones: extreme wind swath (>120 km/h), storm surge danger, and urban deluge sectors.",
    params=[("eventId", "string", "path", True, "Event ID (e.g. `BOB-02`)")],
    sample_response=responses.get("/api/event-detail/BOB-02/hazard"),
    frontend_usage="Leaflet / Mapbox color-coded hazard polygon overlays with click popups.",
    ts_interface="""export interface HazardZone {
  zoneId: string;
  name: string;
  hazardType: string;
  severityColor: string;
  coordinates: [number, number][];
}

export type EventHazardResponse = HazardZone[];"""
)

# 39. Event Detail - CAP Alerts
render_endpoint_section(
    title="39. CAP-Compliant Emergency Alerts",
    method="GET",
    path="/api/event-detail/{eventId}/alerts",
    live_path="/api/event-detail/BOB-02/alerts",
    desc="Formal Common Alerting Protocol (CAP) compliant emergency bulletins for disaster management authorities.",
    params=[("eventId", "string", "path", True, "Event ID (e.g. `BOB-02`)")],
    sample_response=responses.get("/api/event-detail/BOB-02/alerts"),
    frontend_usage="Official emergency warning alerts drawer and printable evacuation bulletins.",
    ts_interface="""export interface CapAlertItem {
  identifier: string;
  sender: string;
  sent: string;
  status: string;
  msgType: string;
  scope: string;
  info: {
    event: string;
    urgency: string;
    severity: string;
    certainty: string;
    headline: string;
    description: string;
    instruction: string;
    area: {
      areaDesc: string;
    };
  };
}

export type EventAlertsResponse = CapAlertItem[];"""
)

# 40. Radar Stations
render_endpoint_section(
    title="40. Doppler Radar Stations Registry",
    method="GET",
    path="/api/radar/stations",
    live_path="/api/radar/stations",
    desc="List of IMD Doppler radar stations available in the network with coordinates, ranges, and products.",
    sample_response=responses.get("/api/radar/stations"),
    frontend_usage="Station selector pills on the Doppler Radar Viewer page.",
    ts_interface="""export interface RadarStation {
  id: string;
  name: string;
  state: string;
  latitude: number;
  longitude: number;
  rangeKm: number;
  supportedProducts: ('reflectivity' | 'velocity')[];
}

export type RadarStationsResponse = RadarStation[];"""
)

# 41. Radar Frames
render_endpoint_section(
    title="41. Doppler Radar Frames Scanner",
    method="GET",
    path="/api/radar/{stationId}/frames",
    live_path="/api/radar/kolkata/frames?product=reflectivity&limit=2",
    desc="Returns chronologically sorted Doppler radar image frames. Frames are updated dynamically by the background harvester daemon every 10 minutes.",
    params=[
        ("stationId", "string", "path", True, "Radar station identifier (e.g. `kolkata`, `paradip`)"),
        ("product", "string", "query", False, "Radar product type: `reflectivity` (default) or `velocity`"),
        ("from", "string", "query", False, "ISO-8601 start timestamp filter (e.g. `2026-09-28T12:00:00Z`)"),
        ("to", "string", "query", False, "ISO-8601 end timestamp filter (e.g. `2026-09-28T18:00:00Z`)"),
        ("limit", "integer", "query", False, "Maximum number of most recent frames to return")
    ],
    sample_response=responses.get("/api/radar/kolkata/frames?product=reflectivity&limit=2"),
    frontend_usage="Doppler Radar animation player (frame-by-frame scrubbing and looping radar loop).",
    ts_interface="""export interface RadarFrame {
  timestamp: string;
  filename: string;
  url: string; // e.g. "/static/radar/kolkata/reflectivity/kolkata_reflectivity_20260928T1704Z.png"
}

export interface RadarFramesResponse {
  station: string;
  product: 'reflectivity' | 'velocity';
  count: number;
  frames: RadarFrame[];
}"""
)

# 42. Radar Latest Frame
render_endpoint_section(
    title="42. Latest Doppler Radar Frame",
    method="GET",
    path="/api/radar/{stationId}/latest",
    live_path="/api/radar/kolkata/latest?product=reflectivity",
    desc="Retrieves the single newest available Doppler radar frame for the station, ideal for quick real-time checks.",
    params=[
        ("stationId", "string", "path", True, "Radar station identifier (e.g. `kolkata`, `paradip`)"),
        ("product", "string", "query", False, "Product type: `reflectivity` or `velocity` (default: `reflectivity`)")
    ],
    sample_response=responses.get("/api/radar/kolkata/latest?product=reflectivity"),
    frontend_usage="Live radar snapshot thumbnail on dashboard or initial image for the radar viewer.",
    ts_interface="""export interface LatestRadarFrameResponse {
  station: string;
  product: 'reflectivity' | 'velocity';
  timestamp: string;
  filename: string;
  url: string;
}"""
)

# 43. Static Imagery Asset URL
render_endpoint_section(
    title="43. Static Radar Image Stream",
    method="GET",
    path="/static/radar/{stationId}/{product}/{filename}",
    live_path="/static/radar/kolkata/reflectivity/kolkata_reflectivity_20260928T1704Z.png",
    desc="Serves raw Doppler radar image files with proper `image/png` Content-Type headers for rendering in `<img>` tags or Mapbox/Leaflet ImageOverlays.",
    params=[
        ("stationId", "string", "path", True, "Station slug (e.g. `kolkata`)"),
        ("product", "string", "path", True, "Product (`reflectivity` or `velocity`)"),
        ("filename", "string", "path", True, "Full frame filename (e.g. `kolkata_reflectivity_20260928T1704Z.png`)")
    ],
    sample_response={"binary": "<Raw PNG Image Data - Content-Type: image/png>"},
    frontend_usage="Use directly in `<img>` or Leaflet `L.imageOverlay(url, bounds)`.",
    ts_interface="// Use directly as an image src:\n// <img src={`${VITE_STATIC_BASE_URL}${frame.url}`} alt=\"Doppler Radar Frame\" />"
)

# Section 4: React / TypeScript Hook Examples
add("## 4. Frontend Integration Snippets (React & TypeScript)")
add()
add("### 4.1 React Custom Hook for Doppler Radar Player")
add("```tsx")
add("""import { useState, useEffect } from 'react';
import axios from 'axios';

interface RadarFrame {
  timestamp: string;
  filename: string;
  url: string;
}

export function useRadarFrames(station: string = 'kolkata', product: string = 'reflectivity') {
  const [frames, setFrames] = useState<RadarFrame[]>([]);
  const [currentIndex, setCurrentIndex] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(true);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);

  const baseUrl = import.meta.env.VITE_API_BASE_URL || 'https://mock-prahari.onrender.com/api';
  const staticUrl = import.meta.env.VITE_STATIC_BASE_URL || 'https://mock-prahari.onrender.com';

  useEffect(() => {
    setLoading(true);
    axios.get(`${baseUrl}/radar/${station}/frames?product=${product}`)
      .then(res => {
        setFrames(res.data.frames);
        setCurrentIndex(res.data.frames.length - 1);
      })
      .finally(() => setLoading(false));
  }, [station, product]);

  useEffect(() => {
    if (!isPlaying || frames.length === 0) return;
    const interval = setInterval(() => {
      setCurrentIndex(prev => (prev + 1) % frames.length);
    }, 700);
    return () => clearInterval(interval);
  }, [isPlaying, frames]);

  return {
    frames,
    currentFrame: frames[currentIndex],
    currentImageUrl: frames[currentIndex] ? `${staticUrl}${frames[currentIndex].url}` : null,
    currentIndex,
    setCurrentIndex,
    isPlaying,
    setIsPlaying,
    loading
  };
}""")
add("```")
add()

add("### 4.2 React Hook for Monitored Cyclone Telemetry")
add("```tsx")
add("""import { useState, useEffect } from 'react';
import axios from 'axios';

export function useCycloneTelemetry(eventId: string = 'BOB-02') {
  const [telemetry, setTelemetry] = useState<any>(null);
  const [trajectory, setTrajectory] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const baseUrl = import.meta.env.VITE_API_BASE_URL || 'https://mock-prahari.onrender.com/api';

  useEffect(() => {
    Promise.all([
      axios.get(`${baseUrl}/events/${eventId}/telemetry`),
      axios.get(`${baseUrl}/events/${eventId}/trajectory`)
    ]).then(([telRes, trajRes]) => {
      setTelemetry(telRes.data);
      setTrajectory(trajRes.data);
    }).finally(() => setLoading(false));
  }, [eventId]);

  return { telemetry, trajectory, loading };
}""")
add("```")
add()

add("---")
add()
add("## 5. Summary & Support")
add()
add("- **Live Base URL:** [`https://mock-prahari.onrender.com`](https://mock-prahari.onrender.com)")
add("- **CORS:** Enabled with wildcard `*` for seamless frontend development.")
add("- **Interactive API Explorer:** Visit [`https://mock-prahari.onrender.com/docs`](https://mock-prahari.onrender.com/docs) for the live Swagger UI where you can execute queries directly in your browser.")
add("- **All 42 API Endpoints:** Tested and verified operational with 200 OK responses.")

full_content = "\n".join(doc_lines)

with open("FRONTEND_API_REFERENCE.md", "w", encoding="utf-8") as f:
    f.write(full_content)

print(f"Generated FRONTEND_API_REFERENCE.md ({len(full_content)} chars)")
