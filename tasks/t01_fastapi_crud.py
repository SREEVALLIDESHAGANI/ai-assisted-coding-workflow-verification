# Task 1: FastAPI User CRUD Models and Service
from typing import Dict, Optional, List
from pydantic import BaseModel, Field, field_validator
import re

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    is_active: bool = True

    @field_validator('email')
    def validate_email_format(cls, v):
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', v):
            raise ValueError('Invalid email format')
        return v

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

class UserService:
    def __init__(self):
        self.db: Dict[int, dict] = {}
        self.counter = 1

    def create_user(self, user: UserCreate) -> UserResponse:
        user_id = self.counter
        self.counter += 1
        record = {'id': user_id, 'username': user.username, 'email': user.email, 'is_active': user.is_active}
        self.db[user_id] = record
        return UserResponse(**record)

    def get_user(self, user_id: int) -> Optional[UserResponse]:
        record = self.db.get(user_id)
        return UserResponse(**record) if record else None
