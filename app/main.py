from fastapi import Depends, FastAPI, Response, status
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

boo_do = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@boo_do.post("/todos/", response_model=list[int])
def create_todos(todos: list[schemas.ToDoCreate], db: Session = Depends(get_db)):
    return crud.create_todos(db=db, todos=todos)


@boo_do.get("/todos/", response_model=list[schemas.ToDo])
def get_todos(db: Session = Depends(get_db)):
    items = crud.get_todos(db)
    return items


@boo_do.get("/todos/overdue", response_model=list[schemas.ToDo])
def get_todos_overdue(db: Session = Depends(get_db)):
    items = crud.get_todos_overdue(db)
    return items


@boo_do.put("/todos/done")
def update_todos_done(todo_ids: list[int], db: Session = Depends(get_db)):
    r = crud.update_todos_done(db=db, todo_ids=todo_ids)
    return Response(status_code=status.HTTP_200_OK)


@boo_do.get("/todos/{todo_id}", response_model=list[schemas.ToDo])
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    item = crud.get_todo_by_id(db, todo_id)
    return [item]


@boo_do.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    if not crud.delete_todo(db, todo_id):
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_200_OK)
