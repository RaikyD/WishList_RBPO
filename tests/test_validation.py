from conftest import make_token


def test_invalid_url_rejected(client):
    h = {"Authorization": f"Bearer {make_token()}"}
    r = client.post(
        "/wishes",
        json={"title": "A", "link": "not-a-url"},
        headers=h,
    )
    assert r.status_code == 422


def test_long_search_q_rejected(client):
    q = "x" * 101
    r = client.get("/wishes", params={"q": q})
    assert r.status_code == 422


def test_notes_max_length(client):
    h = {"Authorization": f"Bearer {make_token()}"}
    r = client.post(
        "/wishes",
        json={"title": "A", "notes": "x" * 2000},
        headers=h,
    )
    assert r.status_code == 422
