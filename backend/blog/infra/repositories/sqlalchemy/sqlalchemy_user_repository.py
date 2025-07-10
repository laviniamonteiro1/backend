from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from blog.domain.entities.user import User
from blog.domain.repositories.user_repository import UserRepository
from blog.domain.value_objects.email_vo import Email
from blog.domain.value_objects.password import Password
from blog.infra.models.user_model import UserModel

from blog.infra.database import async_session


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self._current_user: Optional[User] = None

    async def register(self, user: User) -> User:
        model = UserModel.from_entity(user)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        user.id = model.id
        return model.to_entity()

    async def login(self, email: Email, password: Password) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.email == str(email))
        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()

        if user and password.verify(user.password):
            self._current_user = user.to_entity()
            return self._current_user
        return None

    async def get_current_user(self) -> Optional[User]:
        if self._current_user is None:
            raise ValueError("Current user is not set. Please log in first.")
        stmt = select(UserModel).where(UserModel.id == str(self._current_user.id))
        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()
        if user:
            self._current_user = user.to_entity()
        else:
            self._current_user = None
        return self._current_user

    async def set_current_user(self, user: User) -> None:
        self._current_user = user

    async def logout(self) -> None:
        self._current_user = None

    async def get_by_email(self, email: Email) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.email == str(email))
        result = await self._session.execute(stmt)
        user_model = result.scalar_one_or_none()
        return user_model.to_entity() if user_model else None

    async def get_by_id(self, id: str) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.id == str(id))
        result = await self._session.execute(stmt)
        user_model = result.scalar_one_or_none()
        return user_model.to_entity() if user_model else None
