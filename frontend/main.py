from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

products = [
    {"id": 1, "name": "Book One", "price": 150, "category": "Books", "description": "Test book", "image_url": ""},
    {"id": 2, "name": "Mouse", "price": 300, "category": "Tech", "description": "Wireless mouse", "image_url": ""},
]

@app.get("/products")
def get_products():
    return products

@app.get("/products/search/by-name")
def search_products(name: str = ""):
    return [p for p in products if name.lower() in p["name"].lower()]