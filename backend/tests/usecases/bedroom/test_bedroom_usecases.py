import uuid
import pytest

from blog.domain.entities.bedroom import Bedroom
from blog.infra.repositories.in_memory.in_memory_bedroom_repository import (
    InMemoryBedroomRepository,
)

from blog.usecases.bedroom.get_bedroom_by_id import GetBedroomById
from blog.usecases.bedroom.list_bedroom import ListBedroom


def create_test_bedroom() -> Bedroom:
    return Bedroom(
        id=str(uuid.uuid4()),
        title="Quarto Conforto",
        description="Um quarto aconchegante com cama queen size.",
        price="R$ 200.00",
        image="conforto.jpg",
    )


@pytest.mark.asyncio
async def test_get_bedroom_by_id_use_case():
    bedroom_repo = InMemoryBedroomRepository()
    bedroom = create_test_bedroom()
    await bedroom_repo.create_bedroom(bedroom)

    usecase = GetBedroomById(bedroom_repo)
    found_bedroom = await usecase.execute(bedroom.id)

    assert found_bedroom == bedroom


@pytest.mark.asyncio
async def test_get_bedroom_by_id_not_found_use_case():
    bedroom_repo = InMemoryBedroomRepository()
    usecase = GetBedroomById(bedroom_repo)
    found_bedroom = await usecase.execute(str(uuid.uuid4()))

    assert found_bedroom is None


@pytest.mark.asyncio
async def test_list_bedroom_use_case_empty():
    bedroom_repo = InMemoryBedroomRepository()
    usecase = ListBedroom(bedroom_repo)
    bedrooms = await usecase.execute()

    assert len(bedrooms) == 0
    assert bedrooms == []


@pytest.mark.asyncio
async def test_list_bedroom_use_case_populated():
    bedroom_repo = InMemoryBedroomRepository()
    bedroom1 = create_test_bedroom()
    bedroom2 = create_test_bedroom()

    await bedroom_repo.create_bedroom(bedroom1)
    await bedroom_repo.create_bedroom(bedroom2)

    usecase = ListBedroom(bedroom_repo)
    bedrooms = await usecase.execute()

    assert len(bedrooms) == 2
    assert bedroom1 in bedrooms
    assert bedroom2 in bedrooms
