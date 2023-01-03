from fastapi import FastAPI
from ship_web.settings import engine
from ship_web import models
from ship_web.router import ship, category, user, roles, gallery
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#app.include_router(ship.router)
app.include_router(category.router)
app.include_router(user.router)
app.include_router(roles.router)
app.include_router(gallery.router)