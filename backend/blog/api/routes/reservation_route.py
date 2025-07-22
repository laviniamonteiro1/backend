from fastapi import APIRouter, HTTPException, Depends, status, Response
from blog.usecases.reservation.create_reservation import CreateReservation
from blog.usecases.reservation.get_user_reservation_by_id import GetUserReservationById
from blog.usecases.reservation.cancel_reservation import CancelReservation
from blog.usecases.reservation.update_reservation import UpdateReservation
from blog.usecases.reservation.delete_reservation import DeleteReservation
from blog.usecases.reservation.list_reservation import ListReservation
from blog.domain.entities.reservation import Reservation
from sqlalchemy.ext.asyncio import AsyncSession
from blog.api.deps import (
    get_db_session,
    get_reservation_repository,
    get_user_repository,
    get_current_user,
)
from blog.infra.repositories.sqlalchemy.sqlalchemy_reservation_repository import (
    SQLAlchemyReservationRepository,
)
from blog.infra.repositories.sqlalchemy.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from blog.api.schemas.reservation_schema import (
    ReservationCreateInput,
    ReservationUpdateInput,
    ReservationOutput,
    MessageReservationResponse,
)
from blog.domain.repositories.reservation_repository import ReservationRepository
from blog.domain.repositories.user_repository import UserRepository
from blog.domain.entities.user import User
import sys
import traceback

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Criar nova reserva",
)
async def create_reservation_endpoint(
    data: ReservationCreateInput,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    try:
        reservation_repo = SQLAlchemyReservationRepository(db)
        user_repo = SQLAlchemyUserRepository(db)
        usecase = CreateReservation(reservation_repo, user_repo)
        reservation = await usecase.execute(
            user_id=current_user.id,
            title=data.title,
            address=data.address,
            check_in_str=data.check_in,
            check_out_str=data.check_out,
        )
        return Response(
            content=MessageReservationResponse(
                message="Reservation created successfully",
                reservation=ReservationOutput.from_entity(reservation),
            ).model_dump_json(),
            status_code=status.HTTP_201_CREATED,
            media_type="application/json",
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/me",
    response_model=MessageReservationResponse,
    summary="Listar reservas do usuário atual",
)
async def list_my_reservations_endpoint(
    current_user: User = Depends(get_current_user),
    reservation_repo: ReservationRepository = Depends(get_reservation_repository),
):
    try:
        reservations = await reservation_repo.get_reservations_by_user_id(
            current_user.id
        )
        return MessageReservationResponse(
            message="User reservations retrieved successfully",
            reservations=[ReservationOutput.from_entity(r) for r in reservations],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{reservation_id}",
    response_model=ReservationOutput,
    summary="Obter detalhes da reserva",
)
async def get_reservation_by_id_endpoint(
    reservation_id: str,
    current_user: User = Depends(get_current_user),
    reservation_repo: ReservationRepository = Depends(get_reservation_repository),
):
    reservation = await GetUserReservationById(reservation_repo).execute(reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    if current_user.role != "admin" and reservation.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to view this reservation"
        )
    return ReservationOutput.from_entity(reservation)


@router.get(
    "/",
    response_model=MessageReservationResponse,
    summary="Listar todas as reservas",
)
async def list_all_reservations_endpoint(
    current_user: User = Depends(get_current_user),
    reservation_repo: ReservationRepository = Depends(get_reservation_repository),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Only admins can list all reservations"
        )

    reservations = await ListReservation(reservation_repo).execute()
    return MessageReservationResponse(
        message="All reservations retrieved successfully",
        reservations=[ReservationOutput.from_entity(r) for r in reservations],
    )


@router.put(
    "/{reservation_id}",
    response_model=MessageReservationResponse,
    summary="Atualizar reserva",
)
async def update_reservation_endpoint(
    reservation_id: str,
    data: ReservationUpdateInput,
    current_user: User = Depends(get_current_user),
    reservation_repo: ReservationRepository = Depends(get_reservation_repository),
):
    try:
        updated_reservation = await UpdateReservation(reservation_repo).execute(
            reservation_id=reservation_id,
            new_title=data.title,
            new_address=data.address,
            new_check_in_str=data.check_in,
            new_check_out_str=data.check_out,
            new_status=data.status,
        )
        if not updated_reservation:
            raise HTTPException(
                status_code=404, detail="Reservation not found or could not be updated"
            )
        return MessageReservationResponse(
            message="Reservation updated successfully",
            reservation=ReservationOutput.from_entity(updated_reservation),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/{reservation_id}/cancel",
    response_model=MessageReservationResponse,
    summary="Cancelar reserva",
)
async def cancel_reservation_endpoint(
    reservation_id: str,
    current_user: User = Depends(get_current_user),
    reservation_repo: ReservationRepository = Depends(get_reservation_repository),
):
    reservation = await GetUserReservationById(reservation_repo).execute(reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    if current_user.role != "admin" and reservation.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to cancel this reservation"
        )

    try:
        canceled_reservation = await CancelReservation(reservation_repo).execute(
            reservation_id
        )
        if not canceled_reservation:
            raise HTTPException(
                status_code=404,
                detail="Reservation not found or could not be cancelled",
            )
        return MessageReservationResponse(
            message="Reservation cancelled successfully",
            reservation=ReservationOutput.from_entity(canceled_reservation),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/{reservation_id}",
    response_model=MessageReservationResponse,
    summary="Deletar reserva",
    status_code=status.HTTP_200_OK,
)
async def delete_reservation_endpoint(
    reservation_id: str,
    current_user: User = Depends(get_current_user),
    reservation_repo: ReservationRepository = Depends(get_reservation_repository),
):
    reservation = await GetUserReservationById(reservation_repo).execute(reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    if current_user.role != "admin" and reservation.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this reservation"
        )

    deleted = await DeleteReservation(reservation_repo).execute(reservation_id)
    if not deleted:
        raise HTTPException(
            status_code=404, detail="Reservation not found or could not be deleted"
        )
    return MessageReservationResponse(message="Reservation deleted successfully")
