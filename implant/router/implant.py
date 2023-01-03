from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, settings, crud
from typing import List, Union
import uuid, datetime

router = APIRouter(
    tags=["implant"]
)

@router.get('/implant/', response_model=List[schemas.GetImplant])
def get_implant(skip: int= 0, limit: int= 100, db:Session = Depends(settings.get_db)):
    db_implant = crud.db_get_all(models=models.Implant, skip=skip, limit=limit, db=db)
    return db_implant

@router.get('/implant/{implant_id}', response_model=schemas.GetImplant)
def get_implant_id(implant_id:uuid.UUID, db:Session=Depends(settings.get_db)):
    if not implant_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID")
    db_implant = crud.db_get_filter(models=models.Implant, models_filter=models.Implant.id, filter=implant_id, db=db)
    if not db_implant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Implant Not Found")
    return db_implant

@router.post('/implant/', status_code=status.HTTP_201_CREATED)
def create_implant(form:schemas.CreateImplant, db:Session=Depends(settings.get_db)):
    validasi = crud.db_get_filter(models=models.Implant, models_filter=models.Implant.title, filter=form.title, db=db)
    if validasi:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Implant Already Registered")
    get_uuid = uuid.uuid4()
    db_implant = models.Implant(id=get_uuid, **form.dict())
    db.add(db_implant)
    db.commit()
    db.refresh(db_implant)
    return {}

@router.put('/implant/{id}')
def update_implant(id:uuid.UUID, form:schemas.UpdateImplant, db:Session=Depends(settings.get_db)):
    db_implant = crud.db_filter(models=models.Implant, models_filter=models.Implant.id, filter=id, db=db)
    get_validasi = db_implant.first()
    if not get_validasi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Implant Not Found")
    dtime = datetime.datetime.now()
    db_implant.update({**form.dict(), "updated_at":dtime}, synchronize_session=False)
    db.commit()
    return {}

@router.delete('/implant/{id}')
def delete_implant(id:uuid.UUID, db:Session=Depends(settings.get_db)):
    db_implant = crud.db_filter(models=models.Implant, models_filter=models.Implant.id, filter=id, db=db)
    get_validasi = db_implant.first()
    if not get_validasi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Implant Not Found")
    db_implant.delete()
    db.commit()
    return {}

@router.get('/test/')
def get_test(form:Union[str,None]=None, db:Session=Depends(settings.get_db)):
    if form:
        form = form.replace(" ", "_")
    print(form)
    db_implant = db.query(models.Implant).filter(models.Implant.title.contains(form)).all()
    #db_implant = db.query(models.Implant).filter(models.Implant.title.match(form)).all()
    print(db_implant)
    return db_implant