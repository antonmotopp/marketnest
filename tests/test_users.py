from fastapi import status

def test_register_success(client):
    response = client.post("/users/register", json={
        "username": "testuser1",
        "email": "test1@example.com",
        "password": "testpassword"
    })
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "username" in data
    assert "email" in data
    assert "password" not in data

def test_register_existing_username(client):
    response = client.post("/users/register", json={
        "username": "testuser",
        "email": "test1@example.com",
        "password": "secretpassword"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Username or email already exists" in response.json()["detail"]

def test_register_existing_email(client):
    response = client.post("/users/register", json={
        "username": "testuser1",
        "email": "test@example.com",
        "password": "secretpassword"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Username or email already exists" in response.json()["detail"]

def test_register_missing_username(client):
    response = client.post("/users/register", json={
        "email": "test@example.com",
        "password": "secretpassword"
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, "Missing fields: Username"

def test_register_missing_email(client):
    response = client.post("/users/register", json={
        "username": "testuser1",
        "password": "secretpassword"
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, "Missing fields: Email"

def test_register_missing_password(client):
    response = client.post("/users/register", json={
        "username": "testuser1",
        "password": "strongpassword"
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, "Missing fields: Password"

def test_register_invalid_email_type(client):
    response = client.post("/users/register", json={
        "username": "testuser1",
        "email": "emailwithouth(at)symbol",
        "password": "strongpassword"
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, "Wrong style of Email"