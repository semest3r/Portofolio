from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, settings, crud
from typing import List
import uuid
from datetime import datetime

router = APIRouter(
    tags=["compiler"]
)

@router.get('/compiler/', response_model=List[schemas.GetCompiler])
def get_compiler(skip: int= 0, limit: int= 100, db:Session = Depends(settings.get_db)):
    db_compiler = crud.db_get_all(models=models.Compiler, skip=skip, limit=limit, db=db)
    return db_compiler

@router.get('/compiler/{compiler_id}', response_model=schemas.GetCompiler)
def get_compiler_id(compiler_id:uuid.UUID, db:Session=Depends(settings.get_db)):
    if not compiler_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID")
    db_compiler = crud.db_get_filter(models=models.Compiler, models_filter=models.Compiler.id, filter=compiler_id, db=db)
    if not db_compiler:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compiler Not Found")
    return db_compiler

@router.post('/compiler/', status_code=status.HTTP_201_CREATED)
def create_compiler(form:schemas.CreateCompiler, db:Session=Depends(settings.get_db)):
    validasi = crud.db_get_filter(models=models.Compiler, models_filter=models.Compiler.title, filter=form.title, db=db)
    if validasi:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Compiler Already Registered")
    get_uuid = uuid.uuid4()
    db_compiler = models.Compiler(id=get_uuid, **form.dict())
    db.add(db_compiler)
    db.commit()
    db.refresh(db_compiler)
    return {}

@router.put('/compiler/{id}')
def update_compiler(id:uuid.UUID, form:schemas.UpdateCompiler, db:Session=Depends(settings.get_db)):
    db_compiler = crud.db_filter(models=models.Compiler, models_filter=models.Compiler.id, filter=id, db=db)
    get_validasi = db_compiler.first()
    if not get_validasi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compiler Not Found")
    dtime = datetime.now()
    db_compiler.update({**form.dict(), "updated_at":dtime}, synchronize_session=False)
    db.commit()
    return {}

@router.delete('/compiler/{id}')
def update_compiler(id:uuid.UUID, db:Session=Depends(settings.get_db)):
    db_compiler = crud.db_filter(models=models.Compiler, models_filter=models.Compiler.id, filter=id, db=db)
    get_validasi = db_compiler.first()
    if not get_validasi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed Delete Compiler")
    db_compiler.delete()
    db.commit()
    return {}