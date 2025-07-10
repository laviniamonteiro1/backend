from blog.domain.repositories.user_repository import UserRepository
from blog.domain.entities.user import User
from blog.domain.value_objects.email_vo import Email
from blog.domain.value_objects.password import Password
from typing import Optional
import pytest


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._users = {}
        self._current_user_id = None

    @pytest.mark.asyncio
    async def register(self, user: User) -> User:
        self._users[user.id] = user
        self._current_user_id = user.id
        return user

    @pytest.mark.asyncio
    async def login(self, email: Email, password: Password) -> Optional[User]:
        for user in self._users.values():
            if user.email == email and user.password == password:
                self._current_user_id = user.id
                return user
        return None

    @pytest.mark.asyncio
    async def logout(self) -> None:
        self._current_user_id = None

    @pytest.mark.asyncio
    async def get_current_user(self) -> Optional[User]:
        if self._current_user_id is None:
            return None
        return self._users.get(self._current_user_id)

    @pytest.mark.asyncio
    async def set_current_user(self, user: User) -> None:
        self._users[user.id] = user
        self._current_user_id = user.id

    @pytest.mark.asyncio
    async def get_by_email(self, email: Email) -> None:
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    @pytest.mark.asyncio
    async def get_by_id(self, id: str) -> None:
        for user in self._users.values():
            if user.id == id:
                return user
        return None
