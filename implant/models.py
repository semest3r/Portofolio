from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .settings import Base
from datetime import datetime

class Implant(Base):
    __tablename__ = "implant"
    pk = Column(Integer, primary_key=True, nullable=False, unique=True)
    id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    title = Column(String, nullable=False, unique=True)
    price = Column(Integer, nullable=False)
    lvmax = Column(Integer, nullable=False) #lvl maksimal implant
    sale = Column(Boolean, default=False, nullable=False) #boolean dapat dijual atau tidak
    created_at = Column(TIMESTAMP, default=datetime.now())
    updated_at = Column(TIMESTAMP, default=datetime.now())
    #detail_id = Column(UUID(as_uuid=True), ForeignKey(), nullable=False)

class Compiler(Base):
    __tablename__ = "compiler"
    pk = Column(Integer, primary_key=True, nullable=False, unique=True)
    id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    title = Column(String, nullable=False, unique=True)
    price = Column(Integer, nullable=False)
    exp = Column(Integer, nullable=False, unique=True) #jumlah exp yang didapat per compiler
    lvmax = Column(Integer, nullable=False) #lvl maksimal penggunaan exp
    sale = Column(Boolean, default=False, nullable=False) #boolean dapat dijual atau tidak
    created_at = Column(TIMESTAMP, default=datetime.now())
    updated_at = Column(TIMESTAMP, default=datetime.now())

