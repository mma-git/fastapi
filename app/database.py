from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
'''
import psycopg2
from psycopg2.extras import RealDictCursor #turns columns and data into python dictionary when returned
from time import *

CONNECTS TO SQL DATABASE USING RAW SQL INSTEAD 
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
                            password='SQLpassword', cursor_factory=RealDictCursor)
        cursor=conn.cursor() #used to execute sql statements
        print("database connection success")
        break
    except Exception as error:
        print("ERROR: connection to database failed")
        print("ERROR:", error)
        sleep(2)
'''        
#"postgresql://<username>:<password>@<ip-address/hostname>/<database_name>"
'''

NEVER HARDCODE DATABASE URL, SECURITY ISSUES, needs to be relative connections using environment variables
postgresql://postgres:SQLpassword@localhost/fastapi
'''

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()
        
        
