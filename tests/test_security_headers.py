from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_security_headers_present_on_health():
    r = client.get("/health")
    assert r.status_code == 200
    h = r.headers
    assert h.get("X-Content-Type-Options") == "nosniff"
    assert h.get("X-Frame-Options") == "DENY"
    assert h.get("Referrer-Policy") == "no-referrer"
    assert "camera=()" in h.get("Permissions-Policy", "")
    assert "default-src 'none'" in h.get("Content-Security-Policy", "")


def test_security_headers_present_on_api_response():
    r = client.get("/wishes")
    assert r.status_code in (200, 422)  # list works without token; params may validate
    h = r.headers
    for name in [
        "X-Content-Type-Options",
        "X-Frame-Options",
        "Referrer-Policy",
        "Permissions-Policy",
        "Content-Security-Policy",
        "Strict-Transport-Security",
    ]:
        assert name in h
