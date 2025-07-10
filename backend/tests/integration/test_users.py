# tests/test_users.py (ou tests/integration/test_users.py)
import pytest


@pytest.mark.asyncio
async def test_register_and_login(client):
    # Registro
    response = await client.post(
        "/users/register",
        json={
            "name": "Test",
            "email": "test@example.com",
            "password": "test@A123", # A senha deve ser forte o suficiente se houver validação no Password VO
            "role": "user",
        },
    )
    # Voltou a esperar 201, pois a API agora retorna 201 para registro
    assert response.status_code == 201 
    data = response.json()
    assert data["message"] == "User registered successfully"

    # Login
    response = await client.post(
        "/users/login", json={"email": "test@example.com", "password": "test@A123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    token = response.json()["access_token"]

    # GET /users/me
    response = await client.get(
        "/users/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_admin_user_registration(client):
    # Registro de usuário admin
    response = await client.post(
        "/users/register",
        json={
            "name": "Admin User",
            "email": "admin@example.com",
            "password": "admin@A123!", # Senha ajustada para robusta
            "role": "admin",
        },
    )
    # Voltou a esperar 201, pois a API agora retorna 201 para registro
    assert response.status_code == 201 
    data = response.json()
    assert data["user"]["role"] == "admin"