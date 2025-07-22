from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import sqlalchemy as sa
from typing import Union, Sequence
from datetime import datetime
import uuid


from fastapi.staticfiles import StaticFiles

from blog.api.routes import (
    reservation_route,
    user_route,
    bedroom_route,
)

from blog.api.openapi_tags import openapi_tags
from blog.api.bedrooms_mock import BedroomMock
from blog.infra.models.bedroom_model import BedroomModel
from blog.infra.database import async_session, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Database tables checked/created on startup.")

    async with async_session() as db:
        try:
            total_bedrooms_result = await db.execute(
                sa.select(sa.func.count()).select_from(BedroomModel)
            )
            qtd_quartos = total_bedrooms_result.scalar_one()

            if qtd_quartos == 0:
                print(
                    "Banco de dados vazio. Populando com dados iniciais de quartos..."
                )

                for bedroom_data in BedroomMock:
                    bedroom_id = uuid.uuid4()

                    await db.execute(
                        sa.text(
                            """
                            INSERT INTO bedrooms (id, title, description, price, image)
                            VALUES (:id, :title, :description, :price, :image)
                            """
                        ),
                        {
                            "id": str(bedroom_id),
                            "title": bedroom_data["title"],
                            "description": bedroom_data["description"],
                            "price": bedroom_data["price"],
                            "image": bedroom_data["image"],
                        },
                    )

                await db.commit()
                print("Quartos mockados adicionados com sucesso.")
            else:
                print(
                    f"Banco de dados já contém {qtd_quartos} quartos. Nenhuma população necessária."
                )

        except Exception as e:
            print(f"Erro ao inserir dados iniciais de quartos: {e}")
            await db.rollback()
        finally:
            pass

    yield

    await engine.dispose()
    print("Database engine disposed on shutdown.")


app = FastAPI(
    title="RoyalStay API",
    description="API backend de quartos com Clean Architecture, FastAPI e PostgreSQL",
    version="1.0.0",
    contact={
        "name": "Lavínia",
        "email": "laviniamonteiro10@gmail.com",
    },
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    openapi_tags=openapi_tags,
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="blog/api/static"), name="static")


origins = ["http://localhost:5173", "https://web-front-omega.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        field = ".".join(str(loc) for loc in err["loc"] if isinstance(loc, str))
        errors.append({"field": field, "message": err["msg"]})

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Erro de validação nos campos enviados.", "errors": errors},
    )


@app.get("/")
def root():
    return {"message": "RoyalStay API rodando com sucesso!"}


# Inclusão das rotas
app.include_router(
    user_route.router, prefix="/auth", tags=["Users"]
)  # <--- LINHA CORRIGIDA AQUI!
app.include_router(bedroom_route.router, prefix="/bedrooms", tags=["Bedrooms"])
app.include_router(
    reservation_route.router, prefix="/reservations", tags=["Reservation"]
)
