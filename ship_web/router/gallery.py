from fastapi import APIRouter, Depends, status, HTTPException, Security
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from ship_web import models, schemas, settings, crud
from ..auth.oauth2 import get_current_user
from typing import List
import uuid, base64, os
from datetime import datetime

router = APIRouter(
    tags=["Gallery"]
)

@router.get("/gallery/", response_model=List[schemas.GetGallery])
def get_gallery(limit:int=100, skip:int=0, db:Session=Depends(settings.get_db)):
    db_gallery = crud.db_get_all(models=models.Gallery, limit=limit, skip=skip, db=db)
    return db_gallery

@router.get("/gallery/{id}", response_model=schemas.GetGallery)
def get_gellery_id(id:uuid.UUID, db:Session=Depends(settings.get_db)):
    db_gallery = crud.db_get_filter(models=models.Gallery, models_filter=models.Gallery.id, filter=id, db=db)
    if not db_gallery:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gallery Not Found")
    return db_gallery

@router.post("/gallery/", status_code=status.HTTP_201_CREATED)
def create_gallery(form:schemas.CreateGallery, get_current_user=Security(get_current_user, scopes=['user','superuser']), db:Session=Depends(settings.get_db)):
    validasi = crud.db_get_filter(models=models.Gallery, models_filter=models.Gallery.title, filter=form.title, db=db)
    if validasi :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Gallery Already Registered")
    filename = settings.get_time()
    get_uuid = uuid.uuid4()
    generate = uuid.uuid5(get_uuid, form.title)
    try:
        with open(f'ship_web/assets/gallery/{filename}', "wb") as fn:
            fn.write(base64.urlsafe_b64decode(form.img))
            fn.close()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image Invalid Request")
    db_gallery = models.Gallery(id=generate, img=filename, title=form.title, description=form.description)
    db.add(db_gallery)
    db.commit()
    db.refresh(db_gallery)
    return {}

@router.put("/gallery/{id}")
def update_gallery(id:uuid.UUID, form:schemas.UpdateGallery, get_current_user=Security(get_current_user, scopes=['user','superuser']), db:Session=Depends(settings.get_db)):
    db_gallery = crud.db_filter(models=models.Gallery, models_filter=models.Gallery.id, filter=id, db=db)
    get_validasi = db_gallery.first()
    if not get_validasi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Update Failed")
    filename = settings.get_time()
    try:
        with open(f'ship_web/assets/gallery/{filename}', "wb") as fn:
            fn.write(base64.urlsafe_b64decode(form.img))
            fn.close()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image Invalid Request")
    if os.path.exists(f'ship_web/assets/gallery/{get_validasi.img}'):
        os.remove(f'ship_web/assets/gallery/{get_validasi.img}')
    db_gallery.update({"title":form.title, "description":form.description, "updated_at":datetime.now(), "img":filename}, synchronize_session=False)
    db.commit()
    return {}

@router.delete("/gallery/{id}")
def delete_gallery(id:uuid.UUID,get_current_user=Security(get_current_user, scopes=['superuser']), db:Session=Depends(settings.get_db)):
    db_gallery = crud.db_filter(models=models.Gallery, models_filter=models.Gallery.id, filter=id, db=db)
    get_validasi = db_gallery.first()
    if not get_validasi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Delete Failed")
    if os.path.exists(f'ship_web/assets/gallery/{get_validasi.img}'):
        os.remove(f'ship_web/assets/gallery/{get_validasi.img}')
    db_gallery.delete()
    db.commit()
    return {}