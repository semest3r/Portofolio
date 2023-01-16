from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import calendar
from pydantic import BaseSettings

class Set_Database(BaseSettings):
    DATABASE_HOSTNAME:str
    DATABASE_PORT:str
    DATABASE_PASSWORD:str
    DATABASE_NAME:str
    DATABASE_USERNAME:str
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    
    class Config:
        env_file=".env"

set_db = Set_Database()

engine = create_engine(f'postgresql://{set_db.DATABASE_USERNAME}:{set_db.DATABASE_PASSWORD}@{set_db.DATABASE_HOSTNAME}:{set_db.DATABASE_PORT}/{set_db.DATABASE_NAME}')

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_time():
    time = datetime.utcnow()
    utc_time = calendar.timegm(time.utctimetuple())
    name_img = f'img{utc_time}.jpg'
    return name_img

