import json
from datetime import datetime, date

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .database import Base
from .main import boo_do, get_db
from . import models

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
    date_format = "%Y-%m-%d"
    test_date = date.today()
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
            "date_due": test_date.strftime(date_format),
        },
        {
            "title": "Test Task 2",
            "description": "Desc3",
            "is_completed": False
        }
    ]
    # Defaults for empty or absent keys in payload that must be
    # filled in when creating the record in dB:
    defaults = {
        "description": None,
        "date_created": test_date,
        "is_completed": False,
        "date_due": None,
    }

    response = client.post("/todos/", data=json.dumps(payload),
                           headers=json_headers)

    assert response.status_code == 200, response.text

    data = response.json()
    assert len(data) == len(payload)

    # Check stored data in the DB directly:
    local_db = TestingSessionLocal()
    for i, v in enumerate(data):
        # Create dict filled with values from payload and defaults:
        filled = defaults.copy()
        filled.update(payload[i])

        t = local_db.query(models.ToDo).filter(models.ToDo.id == v).one()

        if "date_due" in filled.keys() and filled["date_due"]:
            filled["date_due"] = datetime.strptime(filled["date_due"],
                                                   date_format).date()

        for k in filled.keys():
            assert filled[k] == getattr(t, k)


def test_create_todos_invalid():
    pass


def test_read_todos():
    json_headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    test_date = date.today().strftime("%Y-%m-%d")
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
