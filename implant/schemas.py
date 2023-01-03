from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional, Union
import datetime

class Implant(BaseModel):
    id : UUID
    title : str
    price : int
    lvmax : int
    sale : bool

class Compiler(BaseModel):
    id : UUID
    title : str
    price : int
    exp : int
    lvmax : int
    sale : bool
    created_at : datetime.datetime

class CreateImplant(BaseModel):
    title : str
    price : int
    lvmax : int
    sale : bool

class UpdateImplant(BaseModel):
    title: Optional[str]=None
    price: Optional[int]=None
    lvmax: Optional[int]=None
    sale: Optional[bool]=None

class UpdateCompiler(BaseModel):
    title: Union[str, None]=None
    price: Union[int, None]=None
    lvmax: Union[int, None]=None
    exp: Union[int, None]=None
    sale: Union[bool, None]=None

class CreateCompiler(BaseModel):
    title : str
    price : int
    exp : int
    lvmax : int
    sale : bool

class GetImplant(Implant):
    pass
    class Config:
        orm_mode=True

class GetCompiler(Compiler):
    pass
    class Config:
        orm_mode=True