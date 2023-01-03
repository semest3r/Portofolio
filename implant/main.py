from fastapi import FastAPI
from .settings import engine
from . import models
from .router import implant, compiler


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(implant.router)
app.include_router(compiler.router)