def test_404_envelope(client):
    r = client.get("/wishes/999999")
    assert r.status_code == 404
    body = r.json()
    assert "error" in body
    assert set(body["error"].keys()) >= {"code", "message"}
