from blog.domain.repositories.user_repository import UserRepository


class LogoutUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self) -> None:
        return await self.repository.logout()
