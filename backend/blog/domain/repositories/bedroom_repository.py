from abc import ABC, abstractmethod
from typing import List, Optional
from blog.domain.entities.bedroom import Bedroom


class BedroomRepository(ABC):
    @abstractmethod
    async def create_bedroom(self, bedroom: Bedroom) -> Bedroom:
        pass

    @abstractmethod
    async def get_bedroom_by_id(self, bedroom_id: str) -> Optional[Bedroom]:
        pass

    @abstractmethod
    async def get_all_bedrooms(self) -> List[Bedroom]:
        pass
