from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models 
from database import Base, engine
from routes import router

Base.metadata.create_all(engine)

app = FastAPI(title="Simple Store API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)