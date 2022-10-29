from datetime import date

from pydantic import BaseModel


class ToDoBase(BaseModel):
    title: str
    description: str | None = None


class ToDoCreate(ToDoBase):
    date_due: date | None = None
    is_completed: bool = False


class ToDo(ToDoBase):
    id: int
    is_completed: bool
    date_completed: date | None
    date_due: date | None

    class Config:
        orm_mode = True
