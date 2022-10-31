import json
from datetime import datetime, date, timedelta

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
    # Defaults for empty or absent keys in payload that will be
    # filled in when creating the record in DB:
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


def test_read_todos():
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
            "date_due": date.today(),
            "is_completed": False
        },
        {
            "title": "Test Task 2",
            "description": "Desc3",
            "is_completed": False
        }
    ]

    # Store data for testing directly to the DB:
    local_db = TestingSessionLocal()
    todos_in_models = [models.ToDo(**todo, date_created=date.today())
                       for todo in payload]
    local_db.add_all(todos_in_models)
    local_db.commit()

    for todo in todos_in_models:
        local_db.refresh(todo)
        r = client.get(f"/todos/{todo.id}")
        assert r.status_code == 200, r.text

        response_payload = r.json()
        assert response_payload
        assert type(response_payload) is list, len(response_payload) == 1
        assert type(response_payload[0]) is dict

        for k in response_payload[0].keys():
            value = getattr(todo, k)
            if type(value) is date:
                value = value.strftime("%Y-%m-%d")
            assert response_payload[0][k] == value


def test_read_todos_overdue():
    date_format = "%Y-%m-%d"
    test_date = date.today()
    payload = [
        {
            "title": "Standing task 1 no due date",
            "description": "Desc1",
        },
        {
            "title": "Standing task 2 due date in future",
            "description": "Desc",
            "date_due": (
                    date.today() + timedelta(days=15)
            ),
        },
        {
            "title": "Not completed overdue task",
            "description": "Desc3",
            "date_due": (
                    date.today() - timedelta(days=2)
             ),
        },
        {
            "title": "Completed overdue task",
            "description": "Desc",
            "date_due": (
                    date.today() - timedelta(days=4)
             ),
            "is_completed": True,
        },
        {
            "title": "Standing task due today",
            "description": "Desc",
            "date_due": date.today(),
        },
        {
            "title": "Completed task due today",
            "description": "Desc",
            "date_due": date.today(),
            "is_completed": True,
        },
        {
            "title": "Completed not overdue task",
            "description": "Desc",
            "date_due": (
                    date.today() + timedelta(days=30)
            ),
            "is_completed": True,
        },
    ]

    # Store data for testing directly to the DB:
    local_db = TestingSessionLocal()
    todos_in_models = [models.ToDo(**todo, date_created=date.today())
                       for todo in payload]
    local_db.add_all(todos_in_models)
    local_db.commit()

    response = client.get("/todos/overdue")
    assert response.status_code == 200, response.text

    data = response.json()
    for todo_received in data:
        assert todo_received["date_due"], \
            datetime.strptime(todo_received["date_due"], date_format)\
            .date() < test_date
        assert todo_received["is_completed"] is False


def test_update_done():
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
            "date_due": date.today(),
        },
        {
            "title": "Test Task 4",
            "description": "Desc3",
            "is_completed": False
        }
    ]

    # Store data for testing directly to the DB:
    local_db = TestingSessionLocal()
    todos_in_models = [models.ToDo(**todo, date_created=date.today())
                       for todo in payload]
    local_db.add_all(todos_in_models)
    local_db.commit()

    created_todos_ids = []
    for todo in todos_in_models:
        local_db.refresh(todo)
        created_todos_ids.append(todo.id)

    response = client.put("/todos/done", data=json.dumps(created_todos_ids),
                          headers=json_headers)
    assert response.status_code == 200

    for todo in todos_in_models:
        local_db.refresh(todo)
        assert todo.is_completed is True
