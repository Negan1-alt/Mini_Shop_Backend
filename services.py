from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from config import JWT_ALGORITHM, JWT_EXPIRE_MINUTES, JWT_SECRET
from database import get_db
from exceptions import EmailAlreadyRegistered, InvalidCredentials, ProductNotFound
from models import User, Product
from repository import UserRepository, ProductRepository

password_hasher = PasswordHash.recommended()


def make_token(user: User):
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)
    payload = {"sub": str(user.id), "role": user.role, "exp": expires_at}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


class AuthService:
    def __init__(self, users: UserRepository):
        self.users = users

    def register(self, email: str, password: str):
        email = email.lower()
        if self.users.get_by_email(email):
            raise EmailAlreadyRegistered("Email already registered")

        user = self.users.add(
            User(email=email, hashed_password=password_hasher.hash(password))
        )
        return {"id": user.id, "email": user.email}

    def login(self, email: str, password: str):
        user = self.users.get_by_email(email.lower())
        if user is None or not password_hasher.verify(password, user.hashed_password):
            raise InvalidCredentials("Invalid email or password")

        return {
            "access_token": make_token(user),
            "token_type": "bearer",
            "role": user.role,
        }

class ProductService:
    def __init__(self, products: ProductRepository):
        self.products = products

    def list_products(self, search, limit):
        return self.products.list(search, limit)

    def get(self, product_id):
        product = self.products.get(product_id)
        if product is None:
            raise ProductNotFound("Product not found")
        return product

    def create(self, data):
        return self.products.add(Product(**data.model_dump()))

    def update(self, product_id, data):         # 
        product = self.get(product_id)
        if product is None:
            raise ProductNotFound("Product Not Found")
        for key, value in data.model_dump(exclude_unset=True).items(): # if exclude_unset is False then will return {name:None, price:150 , category:None}
            setattr(product, key, value) # product.key = value ///// product.price = 500
        return self.products.save(product)

    def delete(self, product_id):
        self.products.delete(self.get(product_id))


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(ProductRepository(db))

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))