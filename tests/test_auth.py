import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from main import app
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

    assert response.status_code == 200
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
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_wrong_username(client):
    response = client.post("/auth/login", json={
        "username": "nonexistent",
        "password": "testpassword"
    })
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_missing_fields(client):
    response = client.post("/auth/login", json={
        "username": "testuser"
    })
    assert response.status_code == 422
    response = client.post("/auth/login", json={
        "password": "testpassword"
    })
    assert response.status_code == 422


def test_login_empty_fields(client):
    response = client.post("/auth/login", json={
        "username": "",
        "password": ""
    })
    assert response.status_code == 401


def test_logout_success(client):
    response = client.post("/auth/logout")
    assert response.status_code == 200
    assert "Successfully logged out" in response.json()["message"]