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
    assert data["content"] == "Hello, interested in your item!"
    assert "id" in data
    assert "chat_id" in data
    assert "created_at" in data


def test_send_message_with_advertisement(client, auth_token):
    client.post("/users/register", json={
        "username": "seller",
        "email": "seller@example.com",
        "password": "password123"
    })

    form_data = {
        'title': 'iPhone for sale',
        'description': 'Good condition',
        'price': '500.0',
        'category': 'electronics'
    }

    ad_response = client.post("/advertisements/",
                              headers={"Authorization": f"Bearer {auth_token}"},
                              data=form_data)
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
    assert data["content"] == "Is this iPhone still available?"


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
    assert data[0]["sender_id"] == 1
    assert data[1]["sender_id"] == 1
    assert "chat_id" in data[0]
    assert "chat_id" in data[1]
    assert data[0]["chat_id"] == data[1]["chat_id"]


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


def test_get_conversations_list(client, auth_token):
    client.post("/users/register", json={
        "username": "user1",
        "email": "user1@example.com",
        "password": "password123"
    })

    client.post("/users/register", json={
        "username": "user2",
        "email": "user2@example.com",
        "password": "password123"
    })

    client.post("/messages/",
                headers={"Authorization": f"Bearer {auth_token}"},
                json={
                    "receiver_id": 2,
                    "content": "Hello user1!",
                    "advertisement_id": None
                })

    client.post("/messages/",
                headers={"Authorization": f"Bearer {auth_token}"},
                json={
                    "receiver_id": 3,
                    "content": "Hello user2!",
                    "advertisement_id": None
                })

    response = client.get("/messages/conversations",
                          headers={"Authorization": f"Bearer {auth_token}"})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2

    for conversation in data:
        assert "chat_id" in conversation
        assert "other_user_id" in conversation
        assert "other_username" in conversation
        assert "last_message" in conversation
        assert "last_message_time" in conversation
        assert "unread_count" in conversation


def test_delete_chat_success(client, auth_token):
    client.post("/users/register", json={
        "username": "to_delete",
        "email": "delete@example.com",
        "password": "password123"
    })

    response = client.post("/messages/",
                           headers={"Authorization": f"Bearer {auth_token}"},
                           json={
                               "receiver_id": 2,
                               "content": "Message to be deleted",
                               "advertisement_id": None
                           })

    chat_id = response.json()["chat_id"]

    delete_response = client.delete(f"/messages/chat/{chat_id}",
                                    headers={"Authorization": f"Bearer {auth_token}"})

    assert delete_response.status_code == status.HTTP_200_OK
    assert delete_response.json()["message"] == "Chat deleted successfully"

    conversation_response = client.get("/messages/conversations",
                                       headers={"Authorization": f"Bearer {auth_token}"})
    assert len(conversation_response.json()) == 0


def test_delete_chat_forbidden(client, auth_token):
    client.post("/users/register", json={
        "username": "receiver",
        "email": "receiver@example.com",
        "password": "password123"
    })

    response = client.post("/messages/",
                           headers={"Authorization": f"Bearer {auth_token}"},
                           json={
                               "receiver_id": 2,
                               "content": "Hello receiver!",
                               "advertisement_id": None
                           })

    chat_id = response.json()["chat_id"]

    client.post("/users/register", json={
        "username": "hacker",
        "email": "hacker@example.com",
        "password": "password123"
    })

    hacker_login = client.post("/auth/login", data={
        "username": "hacker",
        "password": "password123"
    })
    hacker_token = hacker_login.json()["access_token"]

    delete_response = client.delete(f"/messages/chat/{chat_id}",
                                    headers={"Authorization": f"Bearer {hacker_token}"})

    assert delete_response.status_code == status.HTTP_403_FORBIDDEN
    assert "You can only delete chats you participate in" in delete_response.json()["detail"]


def test_delete_chat_by_participant(client, auth_token):
    client.post("/users/register", json={
        "username": "participant",
        "email": "participant@example.com",
        "password": "password123"
    })

    response = client.post("/messages/",
                           headers={"Authorization": f"Bearer {auth_token}"},
                           json={
                               "receiver_id": 2,
                               "content": "Hello participant!",
                               "advertisement_id": None
                           })

    chat_id = response.json()["chat_id"]

    participant_login = client.post("/auth/login", data={
        "username": "participant",
        "password": "password123"
    })
    participant_token = participant_login.json()["access_token"]

    delete_response = client.delete(f"/messages/chat/{chat_id}",
                                    headers={"Authorization": f"Bearer {participant_token}"})

    assert delete_response.status_code == status.HTTP_200_OK
    assert delete_response.json()["message"] == "Chat deleted successfully"


def test_chat_auto_creation(client, auth_token):
    client.post("/users/register", json={
        "username": "receiver",
        "email": "receiver@example.com",
        "password": "password123"
    })

    response1 = client.post("/messages/",
                            headers={"Authorization": f"Bearer {auth_token}"},
                            json={
                                "receiver_id": 2,
                                "content": "First message",
                                "advertisement_id": None
                            })

    chat_id_1 = response1.json()["chat_id"]

    response2 = client.post("/messages/",
                            headers={"Authorization": f"Bearer {auth_token}"},
                            json={
                                "receiver_id": 2,
                                "content": "Second message",
                                "advertisement_id": None
                            })

    chat_id_2 = response2.json()["chat_id"]

    assert chat_id_1 == chat_id_2