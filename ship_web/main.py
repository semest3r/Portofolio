from fastapi import FastAPI, UploadFile, File
from ship_web.settings import engine
from ship_web import models
from ship_web.router import ship, category, user, roles, gallery
import pandas as pd
from pydantic import BaseModel
from typing import List
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

#app.include_router(ship.router)
app.include_router(category.router)
app.include_router(user.router)
app.include_router(roles.router)
app.include_router(gallery.router)


class BaseCSV(BaseModel):
    username:str
    password:str
    class Config:
        orm_mode:True

df = pd.read_csv("ship_web/myfile.csv", sep=";")

@app.get("/csv", response_model=List[BaseCSV])
def load_csv():
    return df.to_dict(orient="records")

@app.post("/csv/", response_model=List[BaseCSV])
def post_csv(fileb: UploadFile = File()):
    df = pd.read_csv(fileb.file, sep=";")

    return df.to_dict(orient="records")