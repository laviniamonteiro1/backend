from blog.domain.repositories.bedroom_repository import BedroomRepository
from blog.domain.entities.bedroom import Bedroom
from typing import Optional, List
import pytest


class InMemoryBedroomRepository(BedroomRepository):
    def __init__(self):
        self._bedrooms = {}

    @pytest.mark.asyncio
    async def create_bedroom(self, bedroom: "Bedroom") -> "Bedroom":
        self._bedrooms[bedroom.id] = bedroom
        return bedroom

    @pytest.mark.asyncio
    async def get_bedroom_by_id(self, bedroom_id: str) -> Optional["Bedroom"]:
        return self._bedrooms.get(bedroom_id)

    @pytest.mark.asyncio
    async def get_all_bedrooms(self) -> List["Bedroom"]:
        return list(self._bedrooms.values())

    @pytest.mark.asyncio
    async def update_bedroom(self, bedroom: "Bedroom") -> Optional["Bedroom"]:
        if bedroom.id in self._bedrooms:
            self._bedrooms[bedroom.id] = bedroom
            return bedroom
        return None

    @pytest.mark.asyncio
    async def delete_bedroom(self, bedroom_id: str) -> bool:
        if bedroom_id in self._bedrooms:
            del self._bedrooms[bedroom_id]
            return True
        return False
