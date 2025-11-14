from conftest import make_token


def test_crud_happy_path(client):
    h = {"Authorization": f"Bearer {make_token()}"}
    # create
    r1 = client.post("/wishes", json={"title": "Game"}, headers=h)
    assert r1.status_code == 201
    wid = r1.json()["id"]

    # read
    r2 = client.get(f"/wishes/{wid}")
    assert r2.status_code == 200
    assert r2.json()["title"] == "Game"

    # update
    r3 = client.patch(f"/wishes/{wid}", json={"notes": "ok"}, headers=h)
    assert r3.status_code == 200
    assert r3.json()["notes"] == "ok"

    # purchase
    r4 = client.post(f"/wishes/{wid}/purchase", headers=h)
    assert r4.status_code == 200
    assert r4.json()["is_purchased"] is True

    # delete
    r5 = client.delete(f"/wishes/{wid}", headers=h)
    assert r5.status_code == 204
