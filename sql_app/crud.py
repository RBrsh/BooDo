from datetime import date

from sqlalchemy.orm import Session

from . import models, schemas


def create_todos(db: Session, todos: list[schemas.ToDoCreate]):
    todos_in_models = [models.ToDo(**todo.dict(), date_created=date.today())
                       for todo in todos]
    db.add_all(todos_in_models)
    db.commit()

    todos_ids = []
    for i in todos_in_models:
        db.refresh(i)
        todos_ids.append(i.id)

    return todos_ids


def get_todos(db: Session, limit: int = 100):
    return db.query(models.ToDo).limit(limit).all()


def get_todos_overdue(db: Session, limit: int = 100):
    return db.query(models.ToDo).\
        filter(models.ToDo.date_due <= date.today(),
               models.ToDo.is_completed is False
               ).limit(limit).all()


def update_todos_done(db: Session, todo_ids: list[int]):
    updated_todo_ids = []
    for i in todo_ids:
        item = db.query(models.ToDo).filter(models.ToDo.id == i).one()
        item.is_completed = True
        item.date_completed = date.today()
        updated_todo_ids.append(item.id)
    db.commit()
    return updated_todo_ids
