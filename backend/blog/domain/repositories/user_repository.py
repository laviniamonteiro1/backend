from abc import ABC, abstractmethod
from blog.domain.entities.user import User
from blog.domain.value_objects.email_vo import Email
from blog.domain.value_objects.password import Password
from typing import Optional


class UserRepository(ABC):
    @abstractmethod
    async def login(self, email: Email, password: Password) -> Optional[User]: ...

    @abstractmethod
    async def register(self, user: User) -> User: ...

    @abstractmethod
    async def logout(self) -> None: ...

    @abstractmethod
    async def get_current_user(self) -> User | None: ...

    @abstractmethod
    async def set_current_user(self, user: User) -> None: ...

    @abstractmethod
    async def get_by_email(self, email: Email) -> Optional[User]: ...

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[User]: ...
