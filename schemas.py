from pydantic import BaseModel, EmailStr, Field

class RegisterData(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class LoginData(BaseModel):
    email: EmailStr
    password: str

class ProductCreate(BaseModel):
    name:str = Field(min_length = 1)
    price:float = Field(ge = 0)
    category:str | None = None
    stock:int = Field(default =0,ge= 0)

class ProductUpdate(BaseModel):
    name:str | None = Field(default = None, min_length = 1)
    price:float | None = Field(default = None, ge = 0)
    stock:int | None = Field(default =None,ge= 0)

class ProductRead(ProductCreate):
    id:int
    model_config = {"from_attributes": True}


