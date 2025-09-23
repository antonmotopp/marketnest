from fastapi import status

def test_get_categories_success(client):
    response = client.get("/categories/")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert "electronics" in data
    assert "furniture" in data
    assert "other" in data
    assert len(data) == 3