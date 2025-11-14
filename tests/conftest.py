import os
import time

import jwt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.shared.db import Base, get_db

TEST_DB_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
SessionTest = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture(scope="session", autouse=True)
def _db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(monkeypatch):
    def override():
        db = SessionTest()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override
    # делаем лимит большим для обычных тестов, маленьким только для теста rate-limit
    monkeypatch.setenv("RATE_LIMIT_PER_MINUTE", "1000")
    return TestClient(app)


def make_token(secret=os.getenv("JWT_SECRET", "dev")):
    payload = {"sub": "u1", "iat": int(time.time())}
    return jwt.encode(payload, secret, algorithm="HS256")
