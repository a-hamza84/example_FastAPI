from sqlalchemy import Column, Date, Integer, String, select
from sqlalchemy.ext.declarative import declarative_base
from models.base import SESSION
from utils.helpers import password_context
import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users_sso"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(Integer)
    email = Column(String)
    created_at = Column(Date)

    def __init__(self, username, password, email):
        self.username = username
        self.email = email
        self.created_at = datetime.date.today()
        self.password = self.hash_pass(password)

    def hash_pass(self, password):
        return password_context.hash(password)

    def save_user(self):
        SESSION.add(self)
        SESSION.commit()
