Microservice Design

Services include

* Users Service (port 8001) – stores user info (id, name, email)
* Orders Service (port 8002) – creates orders and gets user info from Users Service

Goal: Orders Service checks if user exists and adds their info to the order.

Schema:
User: { id, name, email }
Order: { id, user_id, item, quantity, user_name, user_email }

API Endpoints:
* Users Service: GET `/users/{user_id}, POST /users/`
* Orders Service: POST `/orders/, GET /orders/{order_id}`

Flow how it is working

Client sends `POST /orders/` with order info
Orders Service calls Users Service to get user info
If user exists, add user info to order and return
Errors: user not found → 400, service down → 503, other → 502

Locally running

1. Create virtualenv, install requirements
2. Run Users Service: `uvicorn src.users.main:app --port 8001 --reload`
3. Run Orders Service: `uvicorn src.orders.main:app --port 8002 --reload`
4. Create users, then create orders
5. Docs: `http://127.0.0.1:8001/docs`, `http://127.0.0.1:8002/docs`
