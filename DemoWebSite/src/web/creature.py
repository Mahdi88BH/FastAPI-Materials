from fastapi import APIRouter
import fake.creature as service
from model.creature import Creature
from typing import List


router = APIRouter(prefix= "/creature")

@router.get("/")
def get_all() -> List[Creature]:
    return service.get_all()


@router.get("/{name}")
def get_one(name: str) -> Creature | None:
    return service.get(name)