from fastapi import APIRouter
import service.creature as service
from model.creature import Creature
from typing import List


router = APIRouter(prefix= "/creature")

@router.get("/")
def get_all() -> List[Creature]:
    return service.get_all()


@router.get("/{name}")
def get_one(name: str) -> Creature | None:
    return service.get_one(name)


@router.post("/")
def create(creature: Creature):
    return service.create(creature)