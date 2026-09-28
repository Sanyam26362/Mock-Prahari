import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import yaml
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_readme_frontmatter():
    readme_path = PROJECT_ROOT / "README.md"
    assert readme_path.is_file(), f"README.md not found at {readme_path}"

    content = readme_path.read_text(encoding="utf-8")
    assert content.startswith("---"), "README.md must start with YAML frontmatter delimiter '---'"

    # Extract frontmatter between the first two '---' markers
    parts = content.split("---", 2)
    assert len(parts) >= 3, "README.md frontmatter must be enclosed between '---' markers"
    fm_raw = parts[1].strip()

    fm_data = yaml.safe_load(fm_raw)
    assert isinstance(fm_data, dict), "Frontmatter must parse into a YAML dictionary"

    assert fm_data.get("sdk") == "docker", f"Expected sdk to be 'docker', got {fm_data.get('sdk')}"
    assert fm_data.get("app_port") == 7860, f"Expected app_port to be 7860, got {fm_data.get('app_port')}"
    assert "title" in fm_data, "Missing 'title' in frontmatter"
    assert "emoji" in fm_data, "Missing 'emoji' in frontmatter"
    print("PASS: README.md contains valid YAML frontmatter with sdk: docker and app_port: 7860")


def test_dockerfile_security_and_specs():
    dockerfile_path = PROJECT_ROOT / "Dockerfile"
    assert dockerfile_path.is_file(), f"Dockerfile not found at {dockerfile_path}"

    content = dockerfile_path.read_text(encoding="utf-8")
    assert "EXPOSE 7860" in content, "Dockerfile must expose port 7860 for Hugging Face Spaces"
    assert "useradd -m -u 1000 user" in content, "Dockerfile must create non-root user with UID 1000"
    assert "USER user" in content, "Dockerfile must switch to non-root user 'user'"
    assert "CMD [\"./start.sh\"]" in content or 'CMD ["./start.sh"]' in content, "Dockerfile must execute ./start.sh"
    assert "chown -R user:user" in content, "Dockerfile must ensure user ownership for writable directories"
    print("PASS: Dockerfile adheres strictly to HF Spaces security standards (Port 7860, UID 1000 non-root user)")


def test_start_script():
    start_sh = PROJECT_ROOT / "start.sh"
    assert start_sh.is_file(), f"start.sh not found at {start_sh}"

    raw_bytes = start_sh.read_bytes()
    assert b"\r\n" not in raw_bytes, "start.sh must have Unix LF line endings (no CRLF)"

    content = raw_bytes.decode("utf-8")
    assert "capture_radar.py" in content, "start.sh must invoke Doppler radar harvester daemon (capture_radar.py)"
    assert "--interval" in content and "--simulate" in content, "capture_radar.py must run in simulation loop"
    assert "PORT" in content or "7860" in content, "start.sh must bind uvicorn using dynamic PORT or 7860"
    print("PASS: start.sh exists, uses Unix LF endings, and properly invokes harvester daemon and uvicorn")


def test_cors_wildcard_access():
    main_py = PROJECT_ROOT / "app" / "main.py"
    assert main_py.is_file(), f"app/main.py not found at {main_py}"
    content = main_py.read_text(encoding="utf-8")
    assert 'allow_origins=["*"]' in content or "allow_origins=['*']" in content, (
        "app/main.py must configure allow_origins=['*']"
    )

    test_origins = [
        "https://my-prahari-frontend.vercel.app",
        "https://huggingface.co",
        "https://hf.space",
        "http://localhost:3000",
        "http://localhost:5173",
        "https://custom-cloud-domain.io",
    ]

    for origin in test_origins:
        res = client.get("/api/health", headers={"Origin": origin})
        assert res.status_code == 200
        assert res.headers.get("access-control-allow-origin") == origin, (
            f"Expected Access-Control-Allow-Origin header to match {origin}, got {res.headers.get('access-control-allow-origin')}"
        )
    print("PASS: app/main.py permits universal wildcard and cloud frontend origins via CORS")


def test_dockerignore():
    dockerignore_path = PROJECT_ROOT / ".dockerignore"
    assert dockerignore_path.is_file(), f".dockerignore not found at {dockerignore_path}"
    content = dockerignore_path.read_text(encoding="utf-8")
    required_ignores = ["__pycache__", "venv", ".git", "tests"]
    for req in required_ignores:
        assert req in content, f".dockerignore should ignore {req}"
    print("PASS: .dockerignore exists and excludes caches, git, and virtualenvs")


if __name__ == "__main__":
    test_readme_frontmatter()
    test_dockerfile_security_and_specs()
    test_start_script()
    test_cors_wildcard_access()
    test_dockerignore()
    print("\nALL HUGGING FACE SPACES PREPARATION TESTS PASSED CLEANLY!")
