from fastapi import APIRouter, HTTPException, Depends, status
from blog.usecases.user.register_user import RegisterUserUseCase
from blog.usecases.user.login_user import LoginUserUseCase
from blog.usecases.user.logout_user import LogoutUserUseCase
from blog.usecases.user.get_current_user import GetCurrentUserUseCase
from blog.domain.entities.user import User
from blog.domain.value_objects.email_vo import Email
from blog.domain.value_objects.password import Password, PasswordValidationError
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from blog.api.deps import get_db_session, get_user_repository, get_current_user
from blog.infra.repositories.sqlalchemy.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from blog.api.schemas.user_schema import (
    RegisterUserInput,
    UserOutput,
    MessageUserResponse,
)
from blog.api.schemas.token_schema import TokenResponse
from blog.api.security import create_access_token
from blog.domain.repositories.user_repository import UserRepository
from blog.api.schemas.user_schema import LoginUserInput
from blog.api.security import verify_token

security = HTTPBearer()
router = APIRouter()


@router.post(
    "/register",
    response_model=MessageUserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar novo usuário",
    description="Cria um novo usuário com nome, email e senha forte.",
)
async def register_user(
    data: RegisterUserInput, db: AsyncSession = Depends(get_db_session)
):
    try:
        user_repo = SQLAlchemyUserRepository(db)
        usecase = RegisterUserUseCase(user_repo)
        user = User(
            id=str(uuid.uuid4()),
            name=data.name,
            email=Email(data.email),
            password=Password(data.password),
            role=data.role,
            phone=data.phone,    # Adicionado phone
            document=data.document, # Adicionado document
            address=data.address, # Adicionado address (corrigido o typo)
        )
        result = await usecase.execute(user)
        return MessageUserResponse(
            message="User registered successfully", user=UserOutput.from_entity(result)
        )
    except PasswordValidationError as p:
        raise HTTPException(status_code=400, detail=str(p))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Fazer o Login do usuário",
    description="Autentica um usuário com email e senha forte.",
)
async def login_user(
    data: LoginUserInput,
    user_repo: UserRepository = Depends(get_user_repository),
):
    try:
        usecase = LoginUserUseCase(user_repo)
        user = await usecase.execute(Email(data.email), Password(data.password))
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_access_token(data={"sub": user.id})
        return TokenResponse(access_token=token, token_type="bearer")
    except PasswordValidationError as p:
        raise HTTPException(status_code=400, detail=str(p))
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get(
    "/me",
    response_model=UserOutput,
    summary="Informar os dados do usuário atual",
    description="Retorna os dados do usuário atual.",
)
async def get_me_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user: User = Depends(get_current_user),
):
    try:
        return {
            "id": user.id,
            "name": user.name,
            "email": str(user.email),
            "role": user.role,
            "phone": user.phone,
            "document": user.document,
            "address": user.address, # Typo 'adress' corrigido para 'address'
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post(
    "/logout",
    response_model=MessageUserResponse,
    summary="Fazer Logout do usuário",
    description="Realiza o logout do usuário, invalidando a sessão.",
    status_code=status.HTTP_200_OK
)
async def logout_user_route(
    user_repo: UserRepository = Depends(get_user_repository),
):
    try:
        usecase = LogoutUserUseCase(user_repo)
        await usecase.execute()
        return MessageUserResponse(message="Logout realizado com sucesso!")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao fazer logout: {e}")