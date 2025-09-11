from fastapi import status

def test_create_advertisement_success(client, auth_token):
    response = client.post("/advertisements/",
                           headers={"Authorization": f"Bearer {auth_token}"},
                           json={
                               "title": "iPhone 13 for sale",
                               "description": "Excellent condition, all accessories included",
                               "price": 15000.50,
                               "category": "electronics"
                           }
                           )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["title"] == "iPhone 13 for sale"
    assert data["description"] == "Excellent condition, all accessories included"
    assert data["price"] == 15000.50
    assert data["user_id"] == 1
    assert data["category"] == "electronics"
    assert "id" in data
    assert "created_at" in data


def test_create_advertisement_unauthorized(client):
    response = client.post("/advertisements/", json={
        "title": "iPhone 13",
        "description": "Phone in good condition",
        "price": 15000.50,
        "category": "electronics"
    })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_advertisement_missing_fields(client, auth_token):
    response = client.post("/advertisements/",
                           headers={"Authorization": f"Bearer {auth_token}"},
                           json={
                               "title": "iPhone 13"
                           }
                           )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_get_advertisements_empty(client):
    response = client.get("/advertisements/all")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_advertisements_with_data(client, auth_token):
    client.post("/advertisements",
                headers={"Authorization": f"Bearer {auth_token}"},
                json={
                    "title": "iPhone 13 for sale",
                    "description": "Excellent condition, all accessories included",
                    "price": 15000.50,
                    "category": "electronics"
                }
                )

    response = client.get("/advertisements/all")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "iPhone 13 for sale"


def test_get_advertisement_by_id_success(client, auth_token):
    create_response = client.post("/advertisements/",
                                  headers={"Authorization": f"Bearer {auth_token}"},
                                  json={
                                      "title": "MacBook Pro for sale",
                                      "description": "Latest model with warranty",
                                      "price": 25000.00,
                                      "category": "electronics"
                                  }
                                  )
    created_id = create_response.json()["id"]

    response = client.get(f"/advertisements/{created_id}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == created_id
    assert data["title"] == "MacBook Pro for sale"
    assert data["description"] == "Latest model with warranty"


def test_get_advertisement_by_id_not_found(client):
    response = client.get("/advertisements/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Advertisement not found"


def test_get_advertisement_by_id_invalid_id(client):
    response = client.get("/advertisements/invalid")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_advertisement_success(client, auth_token):
    create_response = client.post("/advertisements/",
                                  headers={"Authorization": f"Bearer {auth_token}"},
                                  json={
                                      "title": "Old Title",
                                      "description": "Old description",
                                      "price": 1000.00,
                                      "category": "electronics"
                                  })
    created_id = create_response.json()["id"]

    response = client.put(f"/advertisements/{created_id}",
                          headers={"Authorization": f"Bearer {auth_token}"},
                          json={
                              "title": "Updated Title",
                              "price": 1500.00
                          })

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["price"] == 1500.00
    assert data["description"] == "Old description"
    assert data["category"] == "electronics"


def test_update_advertisement_unauthorized(client):
    response = client.put("/advertisements/1", json={
        "title": "Updated Title"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_advertisement_not_found(client, auth_token):
    response = client.put("/advertisements/999",
                          headers={"Authorization": f"Bearer {auth_token}"},
                          json={"title": "Updated Title"})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Advertisement not found"


def test_delete_advertisement_success(client, auth_token):
    create_response = client.post("/advertisements/",
                                  headers={"Authorization": f"Bearer {auth_token}"},
                                  json={
                                      "title": "To Delete",
                                      "description": "This will be deleted",
                                      "price": 1000.00,
                                      "category": "electronics"
                                  })
    created_id = create_response.json()["id"]

    response = client.delete(f"/advertisements/{created_id}",
                             headers={"Authorization": f"Bearer {auth_token}"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Advertisement deleted successfully"

    get_response = client.get(f"/advertisements/{created_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_advertisement_unauthorized(client):
    response = client.delete("/advertisements/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_advertisement_not_found(client, auth_token):
    response = client.delete("/advertisements/999",
                             headers={"Authorization": f"Bearer {auth_token}"})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Advertisement not found"


def test_create_advertisement_invalid_category(client, auth_token):
    response = client.post("/advertisements/",
                          headers={"Authorization": f"Bearer {auth_token}"},
                          json={
                              "title": "Test",
                              "description": "Test",
                              "price": 100.00,
                              "category": "invalid_category"
                          })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_filter_advertisements_by_category(client, auth_token):
    client.post("/advertisements/",
                headers={"Authorization": f"Bearer {auth_token}"},
                json={
                    "title": "Phone",
                    "description": "Test",
                    "price": 100.00,
                    "category": "electronics"
                })

    client.post("/advertisements/",
                headers={"Authorization": f"Bearer {auth_token}"},
                json={
                    "title": "Chair",
                    "description": "Test",
                    "price": 50.00,
                    "category": "furniture"
                })

    response = client.get("/advertisements/all?category=electronics")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["category"] == "electronics"