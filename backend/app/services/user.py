from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from backend.app.repositories.user import UserRepository
from backend.app.schemas.user import UserCreate, UserOut
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    async def register_user(self, db: AsyncSession, user_in: UserCreate) -> UserOut:
        existing = await self.repo.get_by_email(db, user_in.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
        hashed_password = self.hash_password(user_in.password)
        try:
            user = await self.repo.create_user(db, user_in, hashed_password)
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
        return UserOut(id=user.id, email=user.email, created_at=user.created_at)
