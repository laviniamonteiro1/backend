from typing import List

from blog.domain.entities.bedroom import Bedroom
from blog.domain.repositories.bedroom_repository import BedroomRepository


class ListBedroom:
    def __init__(self, bedroom_repo: BedroomRepository):
        self._bedroom_repo = bedroom_repo

    async def execute(self) -> List[Bedroom]:
        return await self._bedroom_repo.get_all_bedrooms()
