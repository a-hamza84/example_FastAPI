from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    String
)
from sqlalchemy.ext.declarative import declarative_base
from models.base import SESSION
from models.users import User

Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)
    created_by = Column(Integer, ForeignKey(User.id))
    created_at = Column(Date)

    def __init__(
        self, title, description, start_date, end_date, created_by, created_at
    ):
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.created_at = created_at
        self.created_by = created_by

    def save_task(self):
        SESSION.add(self)
        SESSION.commit()
