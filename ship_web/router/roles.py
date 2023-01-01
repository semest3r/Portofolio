from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException, Security
from ..auth.oauth2 import get_current_user, credentials_exception
from ship_web import models, schemas, settings
from typing import List
import uuid


router = APIRouter(
    tags=["Roles"]
)

@router.get("/roles/", response_model=List[schemas.Roles])
def get_roles(db:Session=Depends(settings.get_db)):
    db_roles = db.query(models.Roles).all()
    return db_roles

@router.get("/user_roles/", response_model=List[schemas.UserRoles])
def get_user_roles(db:Session=Depends(settings.get_db)):
    query = db.query(models.User_Roles).all()
    return query

@router.get("/user_roles/{id}", response_model=schemas.UserRoles)
def get_user_roles_by_id(id:int, db:Session=Depends(settings.get_db)):
    query = db.query(models.User_Roles).filter(models.User_Roles.id == id).first()
    return query

@router.post("/roles/", status_code=status.HTTP_201_CREATED)
def create_roles(form:schemas.CreateRoles, db:Session=Depends(settings.get_db)):
    get_uuid = uuid.uuid4()
    generate = uuid.uuid5(get_uuid, form.name_roles)
    db_roles = models.Roles(id=generate, name_roles=form.name_roles)
    db.add(db_roles)
    db.commit()
    db.refresh(db_roles)