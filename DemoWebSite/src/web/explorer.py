from fastapi import APIRouter
import fake.explorer as service
from model.explorer import Explorer
from typing import List



router = APIRouter(prefix= "/explorer")

@router.get("/")
def get_all() -> List[Explorer]:
    return service.get_all()

@router.get("/{name}")
def get_one(name: str) -> Explorer | None:
    return service.get(name)