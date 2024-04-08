from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import psycopg2
from psycopg2.extras import RealDictCursor

from time import time

# This file is to connect the database
# This is the connection string format
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>:@<ip-address/hostname>/<database_name>' 
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# # This is to connect a database and raw sql.
# # I don't use this. instead we use sqlalchmy connection
# while True:
#     try:
#         conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', 
#                                 password='N@v131981', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("DB successfully connected")
#         break
#     except Exception as error:
#         print("not connected")
#         print(error)
#         time.sleep(2)

