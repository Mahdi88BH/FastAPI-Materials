from fastapi import FastAPI, Body
from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: int


app = FastAPI()


@app.post("/users")
async def get_info_user(user: User, property: int = Body(lt=3, gt=0)):
    return {"user": user, "property": property}