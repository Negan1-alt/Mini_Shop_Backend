from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from config import JWT_ALGORITHM, JWT_EXPIRE_MINUTES, JWT_SECRET
from database import get_db
from exceptions import EmailAlreadyRegistered, InvalidCredentials
from models import User
from repository import UserRepository

password_hasher = PasswordHash.recommended()


def make_token(user: User) -> str:
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


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))