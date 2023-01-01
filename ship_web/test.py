from datetime import datetime, timedelta
import base64
import uuid
from passlib.context import CryptContext
import secrets
from jose import JWTError, jwt
expire = datetime.utcnow()+timedelta(minutes=5)
print(expire)
SECRET_KEY = "1b09d17ac7e0b84d4de7be808e86878ab47c63eda404bab89a8178f144059a5f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
test_jwt  = create_access_token(data={"username":"154df638-992b-567a-bff4-b67f38e6a667","scopes":["user"]})
print(test_jwt)
"""time = datetime.datetime.utcnow()
utc_time = calendar.timegm(time.utctimetuple())
name_img = f'img{utc_time}.jpg'
db_ship = db.query(models.Ship).filter(models.Ship.ship_name == ship_name).first()
if db_ship is None:
    db_ship = models.Ship(ship_name=ship_name, img=name_img)
    db.add(db_ship)
    db.commit()
    db.refresh(db_ship)
    try:
        contents = file.file.read()
        with open(f'assets/img/{name_img}', "wb") as image:
            image.write(contents)
    except Exception:
        return {"message": "error uploading the file"}
    finally:
        file.file.close()
else:
    raise HTTPException(status_code=400, detail="Ship Already Exist")


###########33    
file = "nkri.png"
with open(file, "rb") as image:
   my_string= base64.urlsafe_b64encode(image.read())

bs64 = my_string

with open(f'assets/img/test.png', "wb") as image:
    image.write(base64.urlsafe_b64decode(bs64))
    image.close()

a= datetime.datetime.now()

print(a)

get_uuid = uuid.uuid4()
generate = uuid.uuid5(get_uuid, "name")
print(generate)



#######################
class passHandler():
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    def get_pwd_hash(self, password):
        return self.pwd_context.hash(password)
    def verify_pwd(self, plain_pwd, hashed_pwd):
        return self.pwd_context.verify(plain_pwd, hashed_pwd)    

pwd = "password"

get_pass = passHandler()
pwd_hash = get_pass.get_pwd_hash(pwd)
print(pwd_hash)

#############
print(secrets.token_hex(32))
#############
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

hash_pwd = hash_password("admin")

verify_pwd = verify_password("admin", hash_pwd)
print(verify_pwd)
##################
#TESTING JWT TOKEN
SECRET_KEY = "asdasd"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
test_jwt  = create_access_token(data={"username":"154df638-992b-567a-bff4-b67f38e6a667"})
print(test_jwt)
    """

