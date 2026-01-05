from pydantic import BaseModel, EmailStr, constr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=128)

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class UserInDB(UserOut):
    hashed_password: str
