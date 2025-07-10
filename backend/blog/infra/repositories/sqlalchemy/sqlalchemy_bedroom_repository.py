# blog/infra/repositories/sqlalchemy/sqlalchemy_bedroom_repository.py

from typing import Optional, List, TYPE_CHECKING
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import (
    delete,
)  # delete pode ser removido se não houver outras operações de delete

from blog.domain.repositories.bedroom_repository import BedroomRepository
from blog.infra.models.bedroom_model import BedroomModel

if TYPE_CHECKING:
    from blog.domain.entities.bedroom import Bedroom


class SQLAlchemyBedroomRepository(BedroomRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_bedroom(self, bedroom: "Bedroom") -> "Bedroom":
        model = BedroomModel.from_entity(bedroom)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        bedroom.id = model.id
        return model.to_entity()

    async def get_bedroom_by_id(self, bedroom_id: str) -> Optional["Bedroom"]:
        stmt = select(BedroomModel).where(BedroomModel.id == bedroom_id)
        result = await self._session.execute(stmt)
        bedroom_model = result.scalar_one_or_none()
        return bedroom_model.to_entity() if bedroom_model else None

    async def get_all_bedrooms(self) -> List["Bedroom"]:
        stmt = select(BedroomModel)
        result = await self._session.execute(stmt)
        bedroom_models = result.scalars().all()
        return [model.to_entity() for model in bedroom_models]
