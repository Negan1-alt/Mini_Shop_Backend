from fastapi import APIRouter, Depends, HTTPException, Query, Path
from schemas import LoginData, RegisterData, ProductRead, ProductCreate, ProductUpdate
from exceptions import EmailAlreadyRegistered, InvalidCredentials, ProductNotFound
from services import AuthService,ProductService, get_auth_service, get_product_service
from auth import require_admin

router = APIRouter()

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

@router.get("/products", response_model=list[ProductRead], tags=["Products"])
def list_products(
    search: str | None = Query(default=None, min_length=1, max_length=50),
    limit: int = Query(default=50, ge=1, le=100),
    service: ProductService = Depends(get_product_service),
):
    return service.list_products(search, limit)


@router.get("/products/{product_id}", response_model=ProductRead, tags=["Products"])
def get_product(product_id: int = Path(ge=1), service: ProductService = Depends(get_product_service)):
    try:
        return service.get(product_id)
    except ProductNotFound as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.post("/products", status_code=201, response_model=ProductRead, tags=["Products"],
             dependencies=[Depends(require_admin)])
def create_product(data: ProductCreate, service: ProductService = Depends(get_product_service)):
    return service.create(data)


@router.put("/products/{product_id}", response_model=ProductRead, tags=["Products"],
            dependencies=[Depends(require_admin)])
def replace_product(data: ProductCreate, product_id: int = Path(ge=1),
                    service: ProductService = Depends(get_product_service)):
    try:
        return service.replace(product_id, data)
    except ProductNotFound as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.patch("/products/{product_id}", response_model=ProductRead, tags=["Products"],
              dependencies=[Depends(require_admin)])
def update_product(data: ProductUpdate, product_id: int = Path(ge=1),
                   service: ProductService = Depends(get_product_service)):
    try:
        return service.update(product_id, data)
    except ProductNotFound as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.delete("/products/{product_id}", tags=["Products"], dependencies=[Depends(require_admin)])
def delete_product(product_id: int = Path(ge=1), service: ProductService = Depends(get_product_service)):
    try:
        service.delete(product_id)
    except ProductNotFound as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    return {"message": "Product deleted"}