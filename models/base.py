from sqlalchemy import ForeignKey, MetaData, Table, Column, Integer, String, Date, create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from utils.helpers import read_config

psql_conf = read_config()['Postgres Configs']
url = URL.create(
    drivername=psql_conf["drivername"],
    username=psql_conf["username"],
    password=psql_conf["password"],
    host=psql_conf["host"],
    database=psql_conf["database"]
)
Base = declarative_base()

engine = create_engine(url)

_SessionFactory = sessionmaker(bind=engine)

def create_tables():
    meta = MetaData()
    users_sso = Table(
    'users_sso', meta, 
    Column('id', Integer, primary_key=True),
    Column('username',String),
    Column('password',String),
    Column('email',String),
    Column('created_at', Date)
    )
    tasks = Table(
    'tasks', meta, 
    Column('id', Integer, primary_key=True),
    Column('title',String),
    Column('description',String),
    Column('start_date',Date),
    Column('end_date', Date),
    Column('created_by', Integer, ForeignKey('users_sso.id')),
    Column('created_at', Date)
    )
    meta.create_all(engine) # create tables

def session_factory():
    Base.metadata.create_all(engine)
    return _SessionFactory()

create_tables()
SESSION = session_factory()