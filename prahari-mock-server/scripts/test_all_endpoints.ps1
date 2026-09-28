param (
    [string]$BaseUrl = "http://127.0.0.1:8000"
)

Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host "       PRAHARI MOCK SERVER - END-TO-END AUTOMATED VERIFICATION RUNBOOK    " -ForegroundColor Cyan
Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host "Target Base URL: $BaseUrl"
Write-Host ""

$endpoints = @(
    # Health & Shared Status
    @{ Path = "/api/health"; Tag = "Core Health"; ExpectFast = $true },
    @{ Path = "/api/system-status"; Tag = "Shared System" },

    # Dashboard
    @{ Path = "/api/dashboard/overview"; Tag = "Dashboard" },
    @{ Path = "/api/dashboard/kpis"; Tag = "Dashboard" },
    @{ Path = "/api/dashboard/anomaly-overview"; Tag = "Dashboard" },
    @{ Path = "/api/dashboard/active-anomalies"; Tag = "Dashboard" },
    @{ Path = "/api/dashboard/forecast-timeline"; Tag = "Dashboard" },
    @{ Path = "/api/dashboard/processing-pipeline"; Tag = "Dashboard" },

    # Model Analysis
    @{ Path = "/api/model-analysis/overview"; Tag = "Model Analysis" },
    @{ Path = "/api/model-analysis/models"; Tag = "Model Analysis" },
    @{ Path = "/api/model-analysis/pipeline"; Tag = "Model Analysis" },
    @{ Path = "/api/model-analysis/configuration"; Tag = "Model Analysis" },
    @{ Path = "/api/model-analysis/metrics"; Tag = "Model Analysis" },
    @{ Path = "/api/model-analysis/verification"; Tag = "Model Analysis" },
    @{ Path = "/api/model-analysis/track-error-chart"; Tag = "Model Analysis" },
    @{ Path = "/api/model-analysis/baseline-comparison"; Tag = "Model Analysis" },

    # Event Monitor
    @{ Path = "/api/events/"; Tag = "Event Monitor" },
    @{ Path = "/api/events/BOB-02"; Tag = "Event Monitor" },
    @{ Path = "/api/events/BOB-02/trajectory"; Tag = "Event Monitor" },
    @{ Path = "/api/events/BOB-02/timeline"; Tag = "Event Monitor" },
    @{ Path = "/api/events/BOB-02/telemetry"; Tag = "Event Monitor" },
    @{ Path = "/api/events/BOB-02/diagnostics"; Tag = "Event Monitor" },
    @{ Path = "/api/events/BOB-02/intensity-distribution"; Tag = "Event Monitor" },
    @{ Path = "/api/events/BOB-02/risk-alerts"; Tag = "Event Monitor" },

    # Historical Replay
    @{ Path = "/api/historical-events/"; Tag = "Historical Replay" },
    @{ Path = "/api/historical-events/comparison-modes"; Tag = "Historical Replay" },
    @{ Path = "/api/historical-events/amphan-2020"; Tag = "Historical Replay" },
    @{ Path = "/api/historical-events/amphan-2020/timeline"; Tag = "Historical Replay" },
    @{ Path = "/api/historical-events/amphan-2020/track"; Tag = "Historical Replay" },
    @{ Path = "/api/historical-events/amphan-2020/hazard-envelope"; Tag = "Historical Replay" },
    @{ Path = "/api/historical-events/amphan-2020/map-layers"; Tag = "Historical Replay" },
    @{ Path = "/api/historical-events/amphan-2020/metrics"; Tag = "Historical Replay" },

    # Event Detail
    @{ Path = "/api/event-detail/events"; Tag = "Event Detail" },
    @{ Path = "/api/event-detail/BOB-02"; Tag = "Event Detail" },
    @{ Path = "/api/event-detail/BOB-02/overview"; Tag = "Event Detail" },
    @{ Path = "/api/event-detail/BOB-02/map"; Tag = "Event Detail" },
    @{ Path = "/api/event-detail/BOB-02/metrics"; Tag = "Event Detail" },
    @{ Path = "/api/event-detail/BOB-02/hazard"; Tag = "Event Detail" },
    @{ Path = "/api/event-detail/BOB-02/alerts"; Tag = "Event Detail" },

    # Doppler Radar
    @{ Path = "/api/radar/stations"; Tag = "Doppler Radar" },
    @{ Path = "/api/radar/kolkata/frames?product=reflectivity"; Tag = "Doppler Radar" },
    @{ Path = "/api/radar/kolkata/latest?product=reflectivity"; Tag = "Doppler Radar" },
    @{ Path = "/static/radar/kolkata/reflectivity/kolkata_reflectivity_20260928T1300Z.png"; Tag = "Radar Static File" }
)

$passed = 0
$failed = 0

Write-Host ("{0,-20} | {1,-52} | {2,-6} | {3,8}" -f "Tag", "Endpoint", "Status", "Latency") -ForegroundColor Yellow
Write-Host ("-" * 92) -ForegroundColor Gray

foreach ($ep in $endpoints) {
    $url = "$BaseUrl$($ep.Path)"
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    try {
        $response = Invoke-WebRequest -Uri $url -Method Get -UseBasicParsing -TimeoutSec 10
        $sw.Stop()
        $code = $response.StatusCode
        $ms = [math]::Round($sw.Elapsed.TotalMilliseconds, 1)

        if ($code -eq 200) {
            Write-Host ("{0,-20} | {1,-52} | {2,-6} | {3,6}ms" -f $ep.Tag, $ep.Path, "$code OK", $ms) -ForegroundColor Green
            $passed++
        } else {
            Write-Host ("{0,-20} | {1,-52} | {2,-6} | {3,6}ms" -f $ep.Tag, $ep.Path, $code, $ms) -ForegroundColor Red
            $failed++
        }
    } catch {
        $sw.Stop()
        $ms = [math]::Round($sw.Elapsed.TotalMilliseconds, 1)
        Write-Host ("{0,-20} | {1,-52} | {2,-6} | {3,6}ms (ERR)" -f $ep.Tag, $ep.Path, "FAIL", $ms) -ForegroundColor Red
        $failed++
    }
}

Write-Host ("-" * 92) -ForegroundColor Gray
Write-Host "TEST RUN COMPLETE: $passed Passed, $failed Failed out of $($endpoints.Count) endpoints tested." -ForegroundColor Cyan
Write-Host "==========================================================================" -ForegroundColor Cyan
