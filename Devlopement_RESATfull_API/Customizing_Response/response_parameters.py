from fastapi import FastAPI, status, Response
from pydantic import BaseModel


class Post(BaseModel):
    title: str

dummies_posts = {
    1: Post(title="Data Science"),
    2: Post(title="Data Engeneering")
}

app = FastAPI()

@app.get("/")
async def get_header(response: Response) -> dict:
    response.headers["Custome-Header"] = "Custome-Hedear-Value"
    response.set_cookie(
        "cookie-name", 
        "cookie-value", 
        max_age=86400)
    return {"hello": "Salam"}


@app.put("/posts/{id}")
async def get_posts(id: int, response: Response, post: Post) -> Post:
    if id not in dummies_posts:
        response.status_code = status.HTTP_201_CREATED
        dummies_posts[id] = post
    return dummies_posts[id]