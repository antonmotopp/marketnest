import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.core.security import Hash
from main import app
from app.db.database import get_db, Base
from app.models.user import User


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
    test_user = User(
        username="testuser",
        email="test@example.com",
        password=Hash.hash_password("testpassword"),
    )
    db.add(test_user)
    db.commit()
    db.close()

    with TestClient(app) as c:
        yield c

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def auth_token(client):
    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "testpassword"
    })
    return response.json()["access_token"]


@pytest.fixture
def auth_tokens(client):
    user2_data = {
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "testpassword"
    }
    client.post("/users/register", json=user2_data)

    response1 = client.post("/auth/login", data={
        "username": "testuser",
        "password": "testpassword"
    })
    token1 = response1.json()["access_token"]

    response2 = client.post("/auth/login", data={
        "username": "testuser2",
        "password": "testpassword"
    })
    token2 = response2.json()["access_token"]

    return [token1, token2]