#initiate sql.. 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import psycopg2
import os

DB_URI = os.environ.get('DATABASE_URL')

#conn = psycopg2.connect(DB_URI, sslmode = True)

def start() -> scoped_session:
    engine = create_engine(DB_URI, client_encoding="utf8")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
SESSION = start()