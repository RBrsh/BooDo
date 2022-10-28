from sqlalchemy import Boolean, Column, Integer, String, Date

from .database import Base


class ToDo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    is_completed = Column(Boolean)
    date_created = Column(Date)
    date_due = Column(Date)
    date_completed = Column(Date)
