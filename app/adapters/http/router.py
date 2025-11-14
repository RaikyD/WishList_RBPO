from fastapi import APIRouter

from .wishes_router import router as wishes

api = APIRouter()
api.include_router(wishes)
