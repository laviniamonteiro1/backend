from typing import Optional

from blog.domain.entities.bedroom import Bedroom
from blog.domain.repositories.bedroom_repository import BedroomRepository


class GetBedroomById:
    def __init__(self, bedroom_repo: BedroomRepository):
        self._bedroom_repo = bedroom_repo

    async def execute(self, bedroom_id: str) -> Optional[Bedroom]:
        return await self._bedroom_repo.get_bedroom_by_id(bedroom_id)