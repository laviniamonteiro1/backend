from fastapi import FastAPI
from fastapi.security import HTTPBearer
from blog.api.routes import user_route, reservation_route, bedroom_route
from blog.api.openapi_tags import openapi_tags
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Blog API",
    description="API backend do Blog com Clean Architecture, FastAPI e PostgreSQL",
    version="1.0.0",
    contact={"name": "Lavinia", "email": "lavinia@exemplo.com"},
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    openapi_tags=openapi_tags,
)

origins = [
    "http://localhost:5173",
    "https://frontclean.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def ola():
    return {"olá": "fastapi"}


app.include_router(user_route.router, prefix="/users", tags=["Users"])
app.include_router(reservation_route.router, prefix="/reservations", tags=["Reservations"])
app.include_router(bedroom_route.router, prefix="/bedrooms", tags=["Bedrooms"])