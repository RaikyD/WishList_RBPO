# def test_internal_error_is_sanitized(client, monkeypatch):
#     from app.adapters.db.repository import WishRepository

#     def boom(*args, **kwargs):
#         raise RuntimeError("boom: sensitive details")

#     monkeypatch.setattr(WishRepository, "list", boom)

#     r = client.get("/wishes")
#     assert r.status_code == 500
#     body = r.json()
#     assert body.get("error", {}).get("code") == "internal_error"
#     assert "boom" not in body.get("error", {}).get("message", "")
