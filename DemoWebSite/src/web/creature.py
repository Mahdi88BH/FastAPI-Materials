from fastapi import APIRouter, status, HTTPException
import service.creature as service
from model.creature import Creature
from typing import List
from error import Duplicate, Missing


router = APIRouter(prefix= "/creature")

@router.get("", status_code=status.HTTP_200_OK)
@router.get("/", status_code=status.HTTP_200_OK)
def get_all() -> List[Creature]:
    return service.get_all()


@router.get("/{name}", status_code=status.HTTP_200_OK)
def get_one(name: str) -> Creature | None:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.msg)


@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create(creature: Creature) -> Creature:
    try:
        return service.create(creature)
    except Duplicate as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.msg)
    

@router.patch("")
@router.patch("/")
def modify(name: str, creature: Creature) -> Creature:
    try:
        service.modify(name, creature)
    except Missing as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.msg)


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
def delete(name: str):
    try:
        service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.msg)