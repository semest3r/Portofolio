from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, TIMESTAMP, TEXT
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from ship_web.settings import Base
from datetime import datetime

#class Ship(Base):
#    __tablename__ = "ship"
#    pk = Column(Integer, primary_key=True, unique=True)
#    id = Column(UUID(as_uuid=True), nullable=False, unique=True)
#    ship_name = Column(String(128), nullable=False, unique=True)
#    img = Column(String(255), nullable=False, unique=True, default="default.jpg")
#    created_at = Column(TIMESTAMP, default=datetime.now())
#    category_id = Column(Integer, ForeignKey("category.id"))
#    category = relationship("Category",cascade = "all, delete", back_populates="ship")

class Category(Base):
    __tablename__= "category"
    pk = Column(Integer, primary_key=True, nullable=False, unique=True)
    id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    name_category = Column(String, nullable=False, unique=True)
    #hip = relationship("Ship",cascade="all, delete", back_populates="category")

class Gallery(Base):
    __tablename__ = "gallery"
    pk = Column(Integer, primary_key=True, nullable=False, unique=True)
    id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    title = Column(String, nullable=False)
    description = Column(TEXT, nullable=True)
    img = Column(String, nullable=False, default="default.jpg")
    created_at = Column(TIMESTAMP, default=datetime.now())
    updated_at = Column(TIMESTAMP, default=datetime.now())

class User(Base):
    __tablename__="user"
    pk = Column(Integer, primary_key=True, nullable=False, unique=True)
    id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    firstname = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    email = Column(String, nullable=True)
    user_roles = relationship("User_Roles", cascade = "all, delete", back_populates="user")


class User_Roles(Base):
    __tablename__="user_roles"
    pk = Column(Integer, primary_key=True, nullable=False, unique=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    roles_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    user = relationship("User",cascade = "all, delete", back_populates="user_roles")
    roles = relationship("Roles",cascade = "all, delete", back_populates="user_roles")


class Roles(Base):
    __tablename__="roles"
    pk = Column(Integer, primary_key=True, nullable=False, unique=True)
    id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    name_roles = Column(String, nullable=False, unique=True)
    user_roles = relationship("User_Roles",cascade = "all, delete", back_populates="roles")
