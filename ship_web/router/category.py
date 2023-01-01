from fastapi import APIRouter, Depends, status, HTTPException, Security
from sqlalchemy.orm import Session
from ship_web import models, schemas, settings, crud
from typing import List
from ..auth.oauth2 import get_current_user
import uuid

router = APIRouter(
    tags=["Category"]
)

@router.put('/category/{category_id}')
def update_category(category_id:int, form:schemas.Category, get_current_user=Security(get_current_user, scopes=['user']), db: Session=Depends(settings.get_db)):
    db_category = db.query(models.Category).filter(models.Category.id == category_id)
    get_category = db_category.first()
    if not get_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category Not Found")
    db_category.update({"name_category":form.name_category}, synchronize_session=False)
    db.commit()
    return {"status":True}

@router.get('/category/', response_model=List[schemas.getCategory])
def get_category(skip:int=0, limit:int=100, db: Session=Depends(settings.get_db)):
    get_category = crud.db_get_all(models=models.Category, limit=limit, skip=skip, db=db)
    return get_category

@router.get('/category/{category_id}', response_model=schemas.getCategory)
def get_category_id(category_id:int, db: Session=Depends(settings.get_db)):
    get_category = crud.db_get_filter(models=models.Category, models_filter=models.Category.id, filter=category_id, db=db)
    if not get_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category Not Found")
    return get_category

@router.post('/category/', status_code=status.HTTP_201_CREATED)
def create_category(form:schemas.Category, get_current_user=Security(get_current_user, scopes=['user']), db: Session=Depends(settings.get_db)):
    get_category = db.query(models.Category).filter(models.Category.name_category == form.name_category).first()
    if get_category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category Already Exist")
    get_uuid = uuid.uuid4()
    generate = uuid.uuid5(get_uuid, form.name_category)
    db_category = models.Category(name_category=form.name_category,id=generate)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)


@router.delete('/category/{category_id}')
def delete_category(category_id:int, get_current_user=Security(get_current_user, scopes=['superuser']), db: Session=Depends(settings.get_db)):
    db_category = crud.db_get_filter(models=models.Category, models_filter=models.Category.id, filter=category_id, db=db)
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category Not Found")
    db.delete(db_category)
    db.commit()
    return {"status":True} 