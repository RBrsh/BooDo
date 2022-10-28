from datetime import date

from pydantic import BaseModel


class ToDoBase(BaseModel):
    title: str
    description: str | None = None


class ToDoCreate(ToDoBase):
    date_due: date | None = None


class ToDo(ToDoBase):
    id: int

    class Config:
        orm_mode = True
