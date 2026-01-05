from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserOut
from app.services.user import UserService
from app.repositories.user import UserRepository
from app.core.db import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    service = UserService(UserRepository())
    return await service.register_user(db, user_in)
