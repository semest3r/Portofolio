from fastapi import APIRouter, Depends, status, HTTPException, Security
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from ship_web import models, schemas, settings, crud
from ..auth.oauth2 import get_current_user, credentials_exception
from typing import List
import uuid, base64, os

router = APIRouter(
    tags=["Ship"]
)

@router.get("/ships/", response_model=List[schemas.Ship])
def get_ship(skip: int= 0, limit: int= 100, db: Session = Depends(settings.get_db)):
    db_ship = crud.db_get_all(models=models.Ship, limit=limit, skip=skip, db=db)
    return db_ship

@router.get("/ships/{ship_id}", response_model=schemas.Ship)
def get_ship_by_id(ship_id:int, db: Session = Depends(settings.get_db)):
    db_ship = crud.db_get_filter(models=models.Ship, models_filter=models.Ship.id, filter=ship_id, db=db)
    #db_ship = db.query(models.Ship).filter(models.Ship.id == ship_id).first()
    if not db_ship:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ship not Found")
    return db_ship

@router.post("/ships/", status_code=status.HTTP_201_CREATED)
def create_ship(form: schemas.CreateShip, get_current_user=Security(get_current_user, scopes=['user']), db: Session = Depends(settings.get_db)):
    get_ship = db.query(models.Ship).filter(models.Ship.ship_name == form.ship_name).first()
    filename = settings.get_time()
    get_uuid = uuid.uuid4()
    generate = uuid.uuid5(get_uuid, form.ship_name)
    if get_ship:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ship Already Registered")
    try:
        with open(f'ship_web/assets/img/{filename}', "wb") as fn:
            fn.write(base64.urlsafe_b64decode(form.image))
            fn.close()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image Invalid Request")
    db_ship = models.Ship(id=generate, img=settings.get_time(), ship_name=form.ship_name, category_id=form.category_id)
    db.add(db_ship)
    db.commit()
    db.refresh(db_ship)
    return {"data": db_ship}

@router.put("/ship/{ship_id}")
def update_ship(ship_id: int,
    form: schemas.CreateShip, 
    get_current_user=Security(get_current_user, 
    scopes=['user']), 
    db:Session= Depends(settings.get_db)):

    db_ship = db.query(models.Ship).filter(models.Ship.id == ship_id)
    get_ship = db_ship.first()
    filename = settings.get_time()
    if not get_ship:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ship not Found")
    try:
        with open(f'ship_web/assets/img/{filename}', "wb") as fn:
            fn.write(base64.urlsafe_b64decode(form.image))
            fn.close()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image Invalid Request")
    if os.path.exists(f'ship_web/assets/img/{get_ship.img}'):
        os.remove(f'ship_web/assets/img/{get_ship.img}')
    db_ship.update({"ship_name":form.ship_name, "img":filename}, synchronize_session=False)
    db.commit()
    return {'status': True}

@router.delete("/ship/{ship_id}")
def delete_ship(ship_id: int, get_current_user=Security(get_current_user, scopes=['user']), db: Session=Depends(settings.get_db)):
    db_ship = db.query(models.Ship).filter(models.Ship.id == ship_id)
    get_ship = db_ship.first()
    if not get_ship:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ship Not Found")
    if os.path.exists(f'ship_web/assets/img/{get_ship.img}'):
        os.remove(f'ship_web/assets/img/{get_ship.img}')
    db_ship.delete()
    db.commit()
    return {"status":True}

@router.get("/img/{filename}")
def get_image(filename:str):
    img = FileResponse(f"ship_web/assets/img/{filename}")
    return img