def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_create_and_get_wish(client):
    from conftest import make_token

    token = make_token()
    headers = {"Authorization": f"Bearer {token}"}

    payload = {"title": "Nintendo Switch", "price_estimate": 30000, "notes": "OLED"}
    r = client.post("/wishes", json=payload, headers=headers)
    assert r.status_code == 201, r.text
    created = r.json()
    assert created["id"] > 0
    assert created["title"] == "Nintendo Switch"
    assert created["is_purchased"] is False

    wid = created["id"]
    r = client.get(f"/wishes/{wid}")
    assert r.status_code == 200
    got = r.json()
    assert got["id"] == wid
    assert got["title"] == "Nintendo Switch"


def test_list_filters_and_purchase(client):
    from conftest import make_token

    token = make_token()
    headers = {"Authorization": f"Bearer {token}"}

    # seed
    client.post(
        "/wishes", json={"title": "Book", "price_estimate": 1500}, headers=headers
    )
    client.post(
        "/wishes",
        json={
            "title": "Running shoes",
            "price_estimate": 8000,
            "notes": "for marathon",
        },
        headers=headers,
    )
    client.post("/wishes", json={"title": "Headphones"}, headers=headers)

    # list all
    r = client.get("/wishes")
    assert r.status_code == 200
    all_items = r.json()
    assert len(all_items) >= 3

    # search q
    r = client.get("/wishes", params={"q": "run"})
    assert r.status_code == 200
    res = r.json()
    assert any("Running shoes" == x["title"] for x in res)

    # price_lte
    r = client.get("/wishes", params={"price_lte": 2000})
    assert r.status_code == 200
    res = r.json()
    assert all((x["price_estimate"] or 0) <= 2000 for x in res)

    # purchase flow
    wid = all_items[0]["id"]
    r = client.post(f"/wishes/{wid}/purchase", headers=headers)
    assert r.status_code == 200
    assert r.json()["is_purchased"] is True

    # filter purchased
    r = client.get("/wishes", params={"purchased": True})
    assert r.status_code == 200
    res = r.json()
    assert any(x["is_purchased"] for x in res)


def test_patch_and_delete(client):
    from conftest import make_token

    token = make_token()
    headers = {"Authorization": f"Bearer {token}"}

    r = client.post(
        "/wishes", json={"title": "Laptop", "price_estimate": 100000}, headers=headers
    )
    assert r.status_code == 201
    wid = r.json()["id"]

    # patch
    r = client.patch(
        f"/wishes/{wid}",
        json={"notes": "16GB RAM", "price_estimate": 90000},
        headers=headers,
    )
    assert r.status_code == 200
    body = r.json()
    assert body["notes"] == "16GB RAM"
    assert body["price_estimate"] == 90000

    # delete
    r = client.delete(f"/wishes/{wid}", headers=headers)
    assert r.status_code == 204

    # not found after delete
    r = client.get(f"/wishes/{wid}")
    assert r.status_code == 404


def test_not_found_and_validation(client):
    from conftest import make_token

    token = make_token()
    headers = {"Authorization": f"Bearer {token}"}

    # not found
    r = client.get("/wishes/999999")
    assert r.status_code == 404

    # validation: пустой title
    r = client.post("/wishes", json={"title": ""}, headers=headers)
    assert r.status_code == 422
