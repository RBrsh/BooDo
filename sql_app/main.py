from fastapi import Depends, FastAPI
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


@boo_do.post("/todos/", response_model=schemas.ToDo)
def create_todo(item: schemas.ToDoCreate, db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=item)


@boo_do.get("/todos/", response_model=list[schemas.ToDo])
def get_todos(db: Session = Depends(get_db)):
    items = crud.get_items(db)
    return items
