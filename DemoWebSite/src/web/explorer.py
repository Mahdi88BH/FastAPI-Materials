from fastapi import APIRouter, HTTPException
from service import explorer as service
from model.explorer import Explorer
from typing import List
from error import Duplicate, Missing



router = APIRouter(prefix= "/explorer")

@router.get("")
@router.get("/")
def get_all() -> List[Explorer]:
    return service.get_all()

@router.get("/{name}")
def get_one(name: str) -> Explorer | None:
    try:
        service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.post("", status_code=201)
@router.post("/", status_code=201)
def create(explorer: Explorer) -> Explorer:

    try:
        service.create(explorer)
    except Duplicate as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.patch("")
@router.patch("/")
def modify(name: str, explorer: Explorer) -> Explorer:

    try:
        service.modify(name, explorer)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.delete("/{name}", status_code=204)
def delete(name: str):

    try:
        service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)