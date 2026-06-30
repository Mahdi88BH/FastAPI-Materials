import os
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from model.user import User
from datetime import timedelta
from typing import List

if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import user as service
else:
    from service import user as service

from error import Missing, Duplicate

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix= "/user")

oauth2_dep = OAuth2PasswordBearer(tokenUrl="token")


def unauthed():
    raise HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail= "Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"}
    )


@router.post("/token")
async def create_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()):
    user = service.auth_user(form_data.username, form_data.password)

    if not user:
        unauthed()
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(
        data={"sub": user.username}, expires=expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/token")
def get_access_token(token: str = Depends(oauth2_dep)) -> dict:
    return {"token": token}


@router.get("/")
def get_all() -> List[User]:
    return service.get_all()


@router.get("/{name}")
def get_one(name: str):
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=exc.msg)
    

@router.post("/", status_code=status.HTTP_201_CREATED)
def create(user: User) -> User:
    try:
        return service.create(user)
    except Duplicate as exc:
        HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.msg)


@router.patch("/")
def modify(name: str, user: User) -> User:
    try:
        service.modify(name, user)
    except Missing as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.msg
        )


@router.delete("/{name}")
def delete(name: str) -> None:
    try:
        service.delete(name)
    except Missing as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.msg
        )