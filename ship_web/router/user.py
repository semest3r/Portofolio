from fastapi import APIRouter, Depends, status, HTTPException, Security, Request, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ship_web import models, schemas, settings
from ..auth.oauth2 import hash_password, create_access_token, verify_password, get_current_user, credentials_exception
import uuid
import pandas as pd
import time
router = APIRouter(
    tags=["User"]
)

@router.get('/user/{user_id}')
def get_user(user_id:str, get_current_user=Security(get_current_user, scopes=['user']), db: Session=Depends(settings.get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    return db_user

@router.post('/user/', status_code=status.HTTP_201_CREATED)
def create_user(form:schemas.CreateUser, db: Session=Depends(settings.get_db)):
    get_user = db.query(models.User).filter(models.User.username == form.username).first()
    get_uuid = uuid.uuid4()
    generate = uuid.uuid5(get_uuid, form.username)
    if get_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Already Registered")
    get_password = hash_password(form.password)
    db_user = models.User(id=generate, username=form.username, password=get_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

@router.put('/user/{user_id}')
def update_user(user_id: int, form:schemas.UpdateUser, db:Session=Depends(settings.get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id)
    get_user = db_user.first()
    print(form.username)
    if not get_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    db_user.update({**form.dict()}, synchronize_session=False)
    db.commit()
    return {"status":True}

@router.delete('/user/{user_id}')
def delete_user(user_id: int, get_current_user=Security(get_current_user, scopes=['superuser']), db:Session=Depends(settings.get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id)
    get_user = db_user.first()
    if not get_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    db_user.delete()
    db.commit()
    return {"status":True}

@router.post('/login/')
def login_user(user_credentials: OAuth2PasswordRequestForm = Depends(), db:Session=Depends(settings.get_db)):
    data_roles = []
    db_user = db.query(models.User).filter(models.User.username == user_credentials.username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    verify_pwd = verify_password(user_credentials.password, db_user.password)
    if verify_pwd is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    get_roles = db.query(models.User_Roles).filter(models.User_Roles.user_id == db_user.id).all()
    for x in get_roles:
        data_roles.append(x.roles.name_roles)
    access_token = create_access_token(data={"username":str(db_user.id), "scopes":data_roles})
    return{"access_token":access_token, "token_type":"bearer"}

@router.get('/current_user/', response_model=schemas.getUser)
def current_user(get_current_user=Security(get_current_user, scopes=['superuser'])):
    return get_current_user

@router.post('/user_batch/', status_code=status.HTTP_201_CREATED)
async def create_user(fileb: UploadFile = File(), db: Session=Depends(settings.get_db)):
    df = pd.read_csv(fileb.file, sep=";")
    read = df.to_dict(orient="records")
    startTime = time.time()
    data = []
    for x in read:
        get_user = db.query(models.User).filter(models.User.username == x["username"]).first()
        if get_user:
            print("user sudah registrasi")
        get_uuid = uuid.uuid4()
        generate = uuid.uuid5(get_uuid, x["username"])
        get_password = hash_password(x["password"])
        data.append(models.User(id=generate, username=x["username"], password=get_password))
    print(data)
    db.bulk_save_objects(data)
    db.commit()
    executionTime = (time.time() - startTime)
    print('Execution time in seconds: ' + str(executionTime))
    return {"status":True}