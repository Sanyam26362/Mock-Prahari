import argparse
import base64
import json
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# Minimal valid 1x1 transparent PNG bytes for simulation/fallback
MIN_PNG_BYTES = base64.b64decode(
    b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) PrahariRadarDaemon/1.0 (Extreme Weather Intelligence)"


def resolve_project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def capture_sweep(config_path: Path, data_dir: Path, simulate: bool = False) -> list[Path]:
    """
    Executes a single sweep across all enabled radar feeds in the config.
    Returns list of paths of newly captured frame files.
    """
    if not config_path.is_file():
        print(f"[ERROR] Config file not found: {config_path}")
        return []

    with open(config_path, "r", encoding="utf-8") as f:
        feeds = json.load(f)

    captured_files: list[Path] = []
    # Current UTC timestamp in YYYYMMDDTHHMMZ format
    utc_now = datetime.now(timezone.utc)
    ts_slug = utc_now.strftime("%Y%m%dT%H%MZ")

    for feed in feeds:
        if not feed.get("enabled", False):
            continue

        station_id = feed["stationId"].lower()
        product = feed["product"].lower()
        source_url = feed.get("sourceUrl", "")
        description = feed.get("description", f"{station_id} {product}")

        target_dir = data_dir / "radar" / station_id / product
        target_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{station_id}_{product}_{ts_slug}.png"
        target_file = target_dir / filename

        image_data = None

        if simulate:
            image_data = MIN_PNG_BYTES
            log_source = "SIMULATION"
        else:
            try:
                req = urllib.request.Request(source_url, headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(req, timeout=10) as response:
                    image_data = response.read()
                log_source = f"LIVE ({source_url})"
            except (urllib.error.URLError, TimeoutError, Exception) as e:
                print(f"[WARN] Failed to fetch live feed for {description}: {e}. Falling back to simulated frame.")
                image_data = MIN_PNG_BYTES
                log_source = "FALLBACK"

        if image_data:
            target_file.write_bytes(image_data)
            captured_files.append(target_file)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{log_source}] Saved frame: {target_file.name} -> {target_file.parent}")

    return captured_files


def main():
    parser = argparse.ArgumentParser(
        description="Prahari Doppler Radar Ingestion Daemon (SIH 2026, PS 26078)"
    )
    project_root = resolve_project_root()
    default_config = project_root / "config" / "radar_sources.json"
    default_data = project_root / "data"

    parser.add_argument(
        "--config",
        type=Path,
        default=default_config,
        help="Path to radar feeds configuration JSON (default: config/radar_sources.json)",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run a single capture sweep and exit (cron/testing mode)",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=600,
        help="Polling interval in seconds between sweeps (default: 600 seconds = 10 minutes)",
    )
    parser.add_argument(
        "--simulate",
        action="store_true",
        help="Generate synthetic PNG radar frames locally without remote network requests",
    )

    args = parser.parse_args()

    print("=" * 76)
    print("        PRAHARI DOPPLER RADAR INGESTION DAEMON (IMD RADAR HARVESTER)")
    print("=" * 76)
    print(f"Config File:  {args.config}")
    print(f"Target Dir:   {default_data / 'radar'}")
    print(f"Mode:         {'SINGLE SWEEP (--once)' if args.once else f'CONTINUOUS DAEMON (--interval {args.interval}s)'}")
    print(f"Simulation:   {'ENABLED (Local mock generation)' if args.simulate else 'DISABLED (Attempt live IMD portal fetch)'}")
    print("=" * 76 + "\n")

    if args.once:
        captured = capture_sweep(args.config, default_data, simulate=args.simulate)
        print(f"\n[DONE] Captured {len(captured)} frame(s) in single sweep.")
        sys.exit(0)

    # Continuous daemon mode
    try:
        while True:
            capture_sweep(args.config, default_data, simulate=args.simulate)
            print(f"[*] Sleeping for {args.interval} seconds until next sweep. (Press Ctrl+C to terminate)...\n")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n[STOP] Radar ingestion daemon terminated by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
