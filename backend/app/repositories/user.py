from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate
from sqlalchemy.exc import IntegrityError

class UserRepository:
    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create_user(self, db: AsyncSession, user_in: UserCreate, hashed_password: str) -> User:
        user = User(email=user_in.email, hashed_password=hashed_password)
        db.add(user)
        try:
            await db.commit()
            await db.refresh(user)
            return user
        except IntegrityError:
            await db.rollback()
            raise
