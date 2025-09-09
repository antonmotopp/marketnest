from fastapi import status

def test_login_success(client):
    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpassword"
    })

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "access_token" in data
    assert "token_type" in data
    assert "user" in data
    assert data["token_type"] == "bearer"

    user_data = data["user"]
    assert user_data["username"] == "testuser"
    assert user_data["email"] == "test@example.com"
    assert "id" in user_data


def test_login_wrong_password(client):
    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "wrongpassword"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_wrong_username(client):
    response = client.post("/auth/login", json={
        "username": "nonexistent",
        "password": "testpassword"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_missing_fields(client):
    response = client.post("/auth/login", json={
        "username": "testuser"
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response = client.post("/auth/login", json={
        "password": "testpassword"
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_login_empty_fields(client):
    response = client.post("/auth/login", json={
        "username": "",
        "password": ""
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_logout_success(client):
    login_response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpassword"
    })
    token = login_response.json()["access_token"]
    response = client.post("/auth/logout", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == status.HTTP_200_OK
    assert "successfully logged out" in response.json()["message"]


def test_logout_without_token(client):
    response = client.post("/auth/logout")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_logout_invalid_token(client):
    response = client.post("/auth/logout", headers={
        "Authorization": "Bearer invalid-token"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED