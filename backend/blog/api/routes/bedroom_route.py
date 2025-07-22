from fastapi import APIRouter, HTTPException, Depends, status
from blog.usecases.bedroom.get_bedroom_by_id import GetBedroomById
from blog.usecases.bedroom.list_bedroom import ListBedroom
from blog.domain.entities.bedroom import Bedroom
from sqlalchemy.ext.asyncio import AsyncSession
from blog.api.deps import get_db_session, get_bedroom_repository, get_current_user
from blog.infra.repositories.sqlalchemy.sqlalchemy_bedroom_repository import (
    SQLAlchemyBedroomRepository,
)
from blog.api.schemas.bedroom_schema import (
    BedroomOutput,
    MessageBedroomResponse,
)
from blog.domain.repositories.bedroom_repository import BedroomRepository
from blog.domain.entities.user import User


router = APIRouter()


@router.get(
    "/",  
    response_model=MessageBedroomResponse,  
    summary="Listar todos os quartos",
)
async def list_all_bedrooms_endpoint(
    bedroom_repo: BedroomRepository = Depends(get_bedroom_repository),
):
    bedrooms = await ListBedroom(bedroom_repo).execute()
    return MessageBedroomResponse(
        message="Bedrooms retrieved successfully",
        bedrooms=[BedroomOutput.from_entity(b) for b in bedrooms],
    )


@router.get(
    "/{bedroom_id}",  # Caminho ajustado para ser relativo ao prefixo /bedrooms
    response_model=BedroomOutput,
    summary="Obter detalhes de um quarto por ID",
)
async def get_bedroom_by_id_endpoint(
    bedroom_id: str,
    bedroom_repo: BedroomRepository = Depends(get_bedroom_repository),
):
    bedroom = await GetBedroomById(bedroom_repo).execute(bedroom_id)
    if not bedroom:
        raise HTTPException(status_code=404, detail="Bedroom not found")
    return BedroomOutput.from_entity(bedroom)
