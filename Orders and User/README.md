# ProductDevProject - Users + Orders (FastAPI)

## What you get
- Two FastAPI microservices (Users and Orders)
- Orders service validates/enriches orders by calling Users service
- Pytest tests that simulate inter-service calls
- DesignDoc.md explaining flow and failure handling

## Quick start
1. python -m venv venv
2. source venv/bin/activate (or venv\Scripts\activate on Windows)
3. pip install -r requirements.txt
4. Run users: uvicorn src.users.main:app --port 8001
5. Run orders: uvicorn src.orders.main:app --port 8002
6. Use curl or Postman to create users and orders.

## Sample curl:
- Create user:
  curl -X POST http://localhost:8001/users/ -H 'Content-Type: application/json' -d '{"id":3,"name":"A","email":"a@example.com"}'
- Create order:
  curl -X POST http://localhost:8002/orders/ -H 'Content-Type: application/json' -d '{"id":1,"user_id":3,"item":"Pen","quantity":2}'
