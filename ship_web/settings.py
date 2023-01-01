from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import calendar

engine = create_engine("postgresql://postgres:pgadmin@127.0.0.1:5432/nkrielites")
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