from operator import indexOf

from app import db
from app.db import database

import pytest
from main import app
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.db.database import get_db, Base
from app.models.user import DBUser
from app.core.security import hash_password

TEST_DB_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False, "isolation_level": None},
    poolclass=StaticPool,
    echo=False
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    test_user = DBUser(
        username="testuser",
        email="test@example.com",
        password=hash_password("testpassword"),
    )
    db.add(test_user)
    db.commit()
    db.close()

    with TestClient(app) as c:
        yield c

    Base.metadata.drop_all(bind=engine)

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

def test_register_success(client):
    response = client.post("/auth/register", json={
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

    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "test1@example.com",
        "password": "secretpassword"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "*Username or email already exists*" in response.json()["detail"]

def test_register_existing_email(client):

    response = client.post("/auth/register", json={
        "username": "testuser1",
        "email": "test@example.com",
        "password": "secretpassword"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "*Username or email already exists*" in response.json()["detail"]

def test_register_missing_username(client):

    response = client.post("/auth/register", json={

        "email": "test@example.com",
        "password": "secretpassword"
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, "Missing fields: Username"

def test_register_missing_email(client):

    response = client.post("/auth/register", json={

        "username": "testuser1",
        "password": "secretpassword"
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, "Missing fields: Email"

def test_register_missing_password(client):
    response = client.post("/auth/register", json={
        "username": "testuser1",
        "password": "strongpassword"
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, "Missing fields: Password"

def test_register_invalid_email_type(client):
    response = client.post("/auth/register", json={
        "username": "testuser1",
        "email": "emailwithouth(at)symbol",
        "password": "strongpassword"
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, "Wrong style of Email"