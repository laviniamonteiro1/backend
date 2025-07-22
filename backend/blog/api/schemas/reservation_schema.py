from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime


class ReservationCreateInput(BaseModel):
    title: str = Field(
        ..., min_length=3, max_length=100, description="Título da reserva"
    )
    address: str = Field(
        ...,
        min_length=5,
        max_length=200,
        description="Endereço da propriedade reservada",
    )
    check_in: str = Field(
        ...,
        pattern=r"^\d{2}/\d{2}/\d{4} às \d{2}h\d{2}$",
        description="Data e hora de check-in (ex: 25/12/2024 às 14h00)",
    )
    check_out: str = Field(
        ...,
        pattern=r"^\d{2}/\d{2}/\d{4} às \d{2}h\d{2}$",
        description="Data e hora de check-out (ex: 30/12/2024 às 11h00)",
    )


type ReservationStatusBackendInput = Literal["confirmed", "cancelled", "completed"]


class ReservationUpdateInput(BaseModel):
    title: Optional[str] = Field(
        None, min_length=3, max_length=100, description="Novo título da reserva"
    )
    address: Optional[str] = Field(
        None, min_length=5, max_length=200, description="Novo endereço da propriedade"
    )

    check_in: Optional[str] = Field(
        None,
        pattern=r"^\d{2}/\d{2}/\d{4} às \d{2}h\d{2}$",
        description="Nova data e hora de check-in (ex: 25/12/2024 às 14h00)",
    )
    check_out: Optional[str] = Field(
        None,
        pattern=r"^\d{2}/\d{2}/\d{4} às \d{2}h\d{2}$",
        description="Nova data e hora de check-out (ex: 30/12/2024 às 11h00)",
    )

    status: Optional[ReservationStatusBackendInput] = Field(
        None, description="Novo status da reserva (ex: 'confirmed', 'cancelled')"
    )


class ReservationOutput(BaseModel):
    id: str = Field(..., description="ID da reserva")
    user_id: str = Field(..., description="ID do usuário que fez a reserva")
    title: str = Field(..., description="Título da reserva")
    address: str = Field(..., description="Endereço da propriedade reservada")
    check_in: str = Field(..., description="Data e hora de check-in")
    check_out: str = Field(..., description="Data e hora de check-out")
    status: str = Field(..., description="Status atual da reserva")

    @classmethod
    def from_entity(cls, entity):
        return cls(
            id=entity.id,
            user_id=entity.user_id,
            title=entity.title,
            address=entity.address,
            check_in=(
                entity.check_in.strftime("%d/%m/%Y às %Hh%M")
                if isinstance(entity.check_in, datetime)
                else entity.check_in
            ),
            check_out=(
                entity.check_out.strftime("%d/%m/%Y às %Hh%M")
                if isinstance(entity.check_out, datetime)
                else entity.check_out
            ),
            status=entity.status,
        )


class MessageReservationResponse(BaseModel):
    message: str
    reservation: Optional[ReservationOutput] = None
    reservations: Optional[List[ReservationOutput]] = None
