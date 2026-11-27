from sqlalchemy import Column, Integer, String, Numeric

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, server_default="user")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    price = Column(Numeric(10,2), nullable = False, server_default="0")
    stock = Column(Integer, nullable = False, server_default="0")
