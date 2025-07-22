import pytest


@pytest.mark.asyncio
async def test_register_and_login(client):
    response = await client.post(
        "/auth/register",
        json={
            "name": "Test",
            "email": "test@example.com",
            "password": "test@A123",
            "role": "user",
            "phone": "11987654321",
            "document": "12345678900",
            "address": "Rua Teste, 100",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "User registered successfully"

    response = await client.post(
        "/auth/login", json={"email": "test@example.com", "password": "test@A123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    token = response.json()["access_token"]

    response = await client.get(
        "/auth/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_admin_user_registration(client):
    response = await client.post(
        "/auth/register",
        json={
            "name": "Admin User",
            "email": "admin@example.com",
            "password": "admin@A123!",
            "role": "admin",
            "phone": "11998765432",
            "document": "00987654321",
            "address": "Av. Admin, 1",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["user"]["role"] == "admin"
