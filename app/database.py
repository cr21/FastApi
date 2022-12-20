from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHMEY_DATABASE_URL=f'postgresql://postgres:root@localhost:5432/fastapi'
SQLALCHMEY_DATABASE_URL=f'postgresql://{settings.pg_database_username}:{settings.pg_database_password}@{settings.pg_database_host}:{settings.pg_database_port}/{settings.pg_database_name}'
engine= create_engine(SQLALCHMEY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

Base = declarative_base()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()