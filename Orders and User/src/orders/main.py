from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import requests

app = FastAPI(title="Orders Service")

class OrderCreate(BaseModel):
    id: int
    user_id: int
    item: str
    quantity: int

class Order(BaseModel):
    id: int
    user_id: int
    item: str
    quantity: int
    user_name: str | None = None
    user_email: str | None = None 

orders: Dict[int, Order] = {}

# user service base URL
USER_SERVICE_BASE = "http://localhost:8001"

@app.post("/orders/", response_model=Order)
def create_order(o: OrderCreate):
    # call user service to get user info
    try:
        r = requests.get(f"{USER_SERVICE_BASE}/users/{o.user_id}", timeout=3.0)
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"User service unavailable: {e}")

    if r.status_code == 404:
        raise HTTPException(status_code=400, detail="Invalid user_id: user not found")
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="Bad response from user service")

    user = r.json()
    order = Order(
        id=o.id,
        user_id=o.user_id,
        item=o.item,
        quantity=o.quantity,
        user_name=user.get('name'),
        user_email=user.get('email')
    )
    orders[o.id] = order
    return order

@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    ord = orders.get(order_id)
    if not ord:
        raise HTTPException(status_code=404, detail="Order not found")
    return ord


#  venv\Scripts\activate
