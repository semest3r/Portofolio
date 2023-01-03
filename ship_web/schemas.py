from pydantic import BaseModel
from typing import List, Optional, Union
from email_validator import validate_email
from uuid import UUID
from datetime import datetime


class BaseUser(BaseModel):
    username: str

class CreateUser(BaseUser):
    password: str
    firstname: Optional[str]
    lastname: Optional[str]
    email: Optional[str]

class UpdateUser(BaseUser):
    firstname: Optional[str]
    lastname: Optional[str]
    email: Optional[str]

class getUser(BaseUser):
    id: UUID
    firstname: Optional[str]
    lastname: Optional[str]
    email: Optional[str]
    
    class Config:
        orm_mode=True

class CreateShip(BaseModel):
    ship_name: str
    image: str
    category_id: int
    
class Category(BaseModel):
    name_category : str
    
class getCategory(BaseModel):
    category_uuid:str
    name_category:str
    
    class Config:
        orm_mode = True
        
class Ship(BaseModel):
    ship_name: str
    img: str
    category: getCategory

    class Config:
        orm_mode = True

class Token(BaseModel):
    acces_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None]=None
    scopes: List[str] = []

class Roles(BaseModel):
    id: UUID
    name_roles: str

    class Config:
        orm_mode=True

class UserRoles(BaseModel):
    user: getUser
    roles: Roles

    class Config:
        orm_mode=True

class CreateRoles(BaseModel):
    name_roles:str

#Gallery
class Gallery(BaseModel):
    id: UUID
    title: str
    description: str
    img:str
    created_at: datetime

class CreateGallery(BaseModel):
    title: str
    description: str
    img: str

class UpdateGallery(CreateGallery):
    pass

class GetGallery(Gallery):
    pass
    class Config:
        orm_mode=True