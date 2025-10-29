from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="Users Service")

class User(BaseModel):
    id: int
    name: str
    email: str


users: Dict[int, User] = {
    1: User(id=1, name="Oushnik Banerjee", email="oushnik@example.com"),
    2: User(id=2, name="Anshu Kumari", email="anshu@example.com")
}

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    user = users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/", response_model=User)
def create_user(user: User):
    if user.id in users:
        raise HTTPException(status_code=400, detail="User already exists")
    users[user.id] = user
    return user
