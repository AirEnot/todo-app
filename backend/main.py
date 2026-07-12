from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import *

from models.base import Base
from db.sessoin import engine

from core.config import get_settings
from api.routers.task import router as task_router
from api.routers.category import router as category_router

settings = get_settings()

@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=task_router)
app.include_router(router=category_router)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=settings.allow_origins,
    allow_methods=["*"]
)

