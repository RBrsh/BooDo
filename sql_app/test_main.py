from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .database import Base
from .main import boo_do, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


boo_do.dependency_overrides[get_db] = override_get_db

client = TestClient(boo_do)


def test_create_todos():
    pass


def test_create_todos_invalid():
    pass


def test_read_todos():
    pass


def test_read_todos_overdue():
    # done items should not be included
    pass


def test_update_todos():
    pass


def test_update_done():
    pass
