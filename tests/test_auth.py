from conftest import make_token


def test_auth_required_on_create(client):
    r = client.post("/wishes", json={"title": "A"})
    assert r.status_code == 401


def test_create_with_token(client):
    tok = make_token()
    r = client.post(
        "/wishes", json={"title": "Book"}, headers={"Authorization": f"Bearer {tok}"}
    )
    assert r.status_code == 201
    assert r.json()["title"] == "Book"
