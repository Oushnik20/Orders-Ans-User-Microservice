import requests
from fastapi.testclient import TestClient
import pytest
import os, sys, json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from users import main as users_main
from orders import main as orders_main

users_client = TestClient(users_main.app)
orders_client = TestClient(orders_main.app)

def mock_requests_get(url, timeout=3.0):

    # extract path from URL
    from urllib.parse import urlparse
    parsed = urlparse(url)
    path = parsed.path
    # forward to users_client
    resp = users_client.get(path)
    class R:
        status_code = resp.status_code
        def json(self):
            return resp.json()
    return R()

def test_create_order_happy_path(monkeypatch):
    # ensure user exists
    u = {"id": 10, "name": "Test User", "email": "test@example.com"}
    resp = users_client.post("/users/", json=u)
    assert resp.status_code == 200

    monkeypatch.setattr("orders.main.requests.get", mock_requests_get)
    order_payload = {"id": 100, "user_id": 10, "item": "Keyboard", "quantity": 1}
    r = orders_client.post("/orders/", json=order_payload)
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == 100
    assert body["user_id"] == 10
    assert body["user_email"] == "test@example.com"

def test_create_order_user_not_found(monkeypatch):
    monkeypatch.setattr("orders.main.requests.get", mock_requests_get)
    order_payload = {"id": 101, "user_id": 9999, "item": "Mouse", "quantity": 1}
    r = orders_client.post("/orders/", json=order_payload)
    assert r.status_code == 400
    assert r.json()["detail"] == "Invalid user_id: user not found"
