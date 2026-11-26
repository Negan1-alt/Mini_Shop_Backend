from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field

from exceptions import EmailAlreadyRegistered, InvalidCredentials
from services import AuthService, get_auth_service

router = APIRouter()


class RegisterData(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class LoginData(BaseModel):
    email: EmailStr
    password: str


@router.post("/register", status_code=201, tags=["Auth"])
def register(data: RegisterData, service: AuthService = Depends(get_auth_service)):
    try:
        return service.register(str(data.email), data.password)
    except EmailAlreadyRegistered as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@router.post("/login", tags=["Auth"])
def login(data: LoginData, service: AuthService = Depends(get_auth_service)):
    try:
        return service.login(str(data.email), data.password)
    except InvalidCredentials as error:
        raise HTTPException(status_code=401, detail=str(error)) from error