from datetime import date

from pydantic import BaseModel, Field


class ToDoBase(BaseModel):
    title: str = Field(min_length=1, max_length=250)
    description: str | None = Field(max_length=2500)


class ToDoCreate(ToDoBase):
    date_due: date | None = None
    is_completed: bool = False


class ToDo(ToDoBase):
    id: int
    is_completed: bool
    date_completed: date | None
    date_due: date | None
    date_created: date

    class Config:
        orm_mode = True
