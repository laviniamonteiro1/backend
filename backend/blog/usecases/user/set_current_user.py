from blog.domain.repositories.user_repository import UserRepository
from blog.domain.entities.user import User


class SetCurrentUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, user: User) -> None:
        await self.repository.set_current_user(user)
