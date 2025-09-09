from fastapi import status

def test_create_advertisement_success(client, auth_token):
    response = client.post("/advertisements/",
                           headers={"Authorization": f"Bearer {auth_token}"},
                           json={
                               "title": "iPhone 13 for sale",
                               "description": "Excellent condition, all accessories included",
                               "price": 15000.50
                           }
                           )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["title"] == "iPhone 13 for sale"
    assert data["description"] == "Excellent condition, all accessories included"
    assert float(data["price"]) == 15000.50
    assert data["user_id"] == 1
    assert "id" in data
    assert "created_at" in data


def test_create_advertisement_unauthorized(client):
    response = client.post("/advertisements/", json={
        "title": "iPhone 13",
        "description": "Phone in good condition",
        "price": 15000.50
    })

    assert response.status_code == status.HTTP_403_FORBIDDEN



def test_create_advertisement_missing_fields(client, auth_token):
    response = client.post("/advertisements/",
                           headers={"Authorization": f"Bearer {auth_token}"},
                           json={
                               "title": "iPhone 13"
                           }
                           )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY