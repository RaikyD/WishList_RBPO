def test_rate_limit_get(client, monkeypatch):
    # Устанавливаем маленький лимит специально для этого теста
    monkeypatch.setenv("RATE_LIMIT_PER_MINUTE", "3")
    codes = [client.get("/wishes").status_code for _ in range(5)]
    assert 429 in codes
