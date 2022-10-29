import json
import datetime

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .database import Base
from .main import boo_do, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                   bind=engine)


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
    json_headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    payload = [
        {
            "title": "Test Task 1",
            "description": "Desc1",
        },
        {
            "title": "Test Task 2",
        },
        {
            "title": "Test Task 3",
            "description": "Desc3",
            "date_due": datetime.date.today().strftime("%Y-%m-%d"),
        },
        {
            "title": "Test Task 2",
            "description": "Desc3",
            "is_completed": False
        }
    ]
    response = client.post("/todos/", data=json.dumps(payload),
                           headers=json_headers)

    assert response.status_code == 200, response.text

    data = response.json()
    assert len(data) == len(payload)


def test_create_todos_invalid():
    pass


def test_read_todos():
    json_headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    test_date = datetime.date.today().strftime("%Y-%m-%d")
    payload = [
        {
            "title": "Test Task 1",
            "description": "Desc1",
        },
        {
            "title": "Test Task 2",
        },
        {
            "title": "Test Task 3",
            "description": "Desc3",
            "date_due": test_date,
        },
        {
            "title": "Test Task 2",
            "description": "Desc3",
            "is_completed": False
        }
    ]

    response = client.post("/todos/", data=json.dumps(payload),
                           headers=json_headers)

    assert response.status_code == 200, response.text
    pay_ld = response.json()

    assert len(pay_ld) == len(payload)

    for i, todo_id in enumerate(pay_ld):
        r = client.get(f"/todos/{todo_id}")
        assert r.status_code == 200, r.text

        for k in payload[i].keys():
            assert payload[i][k] == r.json()[0][k]


def test_read_todos_overdue():
    # done items should not be included
    pass


def test_update_todos():
    pass


def test_update_done():
    pass
