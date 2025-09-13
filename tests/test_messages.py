from fastapi import status


def test_send_message_success(client, auth_token):
    client.post("/users/register", json={
        "username": "receiver_user",
        "email": "receiver@example.com",
        "password": "password123"
    })

    response = client.post("/messages/",
                           headers={"Authorization": f"Bearer {auth_token}"},
                           json={
                               "receiver_id": 2,
                               "content": "Hello, interested in your item!",
                               "advertisement_id": None
                           })

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["sender_id"] == 1
    assert data["receiver_id"] == 2
    assert data["content"] == "Hello, interested in your item!"
    assert "id" in data
    assert "created_at" in data


def test_send_message_with_advertisement(client, auth_token):
    client.post("/users/register", json={
        "username": "seller",
        "email": "seller@example.com",
        "password": "password123"
    })

    ad_response = client.post("/advertisements/",
                              headers={"Authorization": f"Bearer {auth_token}"},
                              json={
                                  "title": "iPhone for sale",
                                  "description": "Good condition",
                                  "price": 500.0,
                                  "category": "electronics"
                              })
    ad_id = ad_response.json()["id"]

    response = client.post("/messages/",
                           headers={"Authorization": f"Bearer {auth_token}"},
                           json={
                               "receiver_id": 2,
                               "content": "Is this iPhone still available?",
                               "advertisement_id": ad_id
                           })

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["advertisement_id"] == ad_id


def test_send_message_receiver_not_found(client, auth_token):
    response = client.post("/messages/",
                           headers={"Authorization": f"Bearer {auth_token}"},
                           json={
                               "receiver_id": 999,
                               "content": "Hello",
                               "advertisement_id": None
                           })

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Receiver not found"


def test_send_message_unauthorized(client):
    response = client.post("/messages/", json={
        "receiver_id": 2,
        "content": "Hello",
        "advertisement_id": None
    })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_conversation_success(client, auth_token):
    client.post("/users/register", json={
        "username": "chat_partner",
        "email": "partner@example.com",
        "password": "password123"
    })

    client.post("/messages/",
                headers={"Authorization": f"Bearer {auth_token}"},
                json={
                    "receiver_id": 2,
                    "content": "First message",
                    "advertisement_id": None
                })

    client.post("/messages/",
                headers={"Authorization": f"Bearer {auth_token}"},
                json={
                    "receiver_id": 2,
                    "content": "Second message",
                    "advertisement_id": None
                })

    response = client.get("/messages/conversation/2",
                          headers={"Authorization": f"Bearer {auth_token}"})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert data[0]["content"] == "First message"
    assert data[1]["content"] == "Second message"


def test_get_conversation_unauthorized(client):
    response = client.get("/messages/conversation/2")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_empty_conversation(client, auth_token):
    client.post("/users/register", json={
        "username": "no_messages",
        "email": "nomsg@example.com",
        "password": "password123"
    })

    response = client.get("/messages/conversation/2",
                          headers={"Authorization": f"Bearer {auth_token}"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []