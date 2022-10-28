from datetime import date

from sqlalchemy.orm import Session

from . import models, schemas


def get_items(db: Session, limit: int = 100):
    return db.query(models.ToDo).limit(limit).all()


def create_user_item(db: Session, item: schemas.ToDoCreate):
    db_item = models.ToDo(**item.dict(), date_created=date.today())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
