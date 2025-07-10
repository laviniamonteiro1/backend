import pytest
import datetime


@pytest.mark.asyncio
async def test_get_bedroom_by_id(client):
    dummy_bedroom_id = "f0e0d0c0-b1a1-9c8c-7b6b-5a4a3a2a1a0a"
    
    # Tenta listar para pegar um ID real, se existir
    list_response = await client.get("/bedrooms")
    if list_response.status_code == 200 and list_response.json()["bedrooms"]:
        test_id = list_response.json()["bedrooms"][0]["id"]
    else:
        # Se a lista estiver vazia ou retornar 404, usa o ID dummy
        test_id = dummy_bedroom_id

    response = await client.get(f"/bedrooms/{test_id}")
    
    if test_id == dummy_bedroom_id: # Se usamos um ID dummy, esperamos 404
        assert response.status_code == 404
        assert response.json()["detail"] == "Bedroom not found" # A rota agora deve retornar este detalhe específico
    else: # Se obtivemos um ID real da lista, esperamos 200
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_id
        assert "title" in data
        assert "description" in data
        assert "price" in data
        assert "image" in data


@pytest.mark.asyncio
async def test_list_bedrooms(client):
    response = await client.get("/bedrooms")
    assert response.status_code == 200 # Esperamos 200 OK para listagem
    data = response.json()
    assert "message" in data
    assert "bedrooms" in data
    assert isinstance(data["bedrooms"], list)