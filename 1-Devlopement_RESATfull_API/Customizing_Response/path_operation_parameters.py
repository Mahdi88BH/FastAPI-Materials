from fastapi import FastAPI, status
from pydantic import BaseModel


class Post(BaseModel):
    titel: str
    nb_views: int

dummies_post = {
    1: Post(titel="Data Science", nb_views=100),
    2: Post(titel="Data Engeneering", nb_views=88)
}

class PublicPost(BaseModel):
    titel: str

app = FastAPI()


# Response Model
@app.get("/posts/{id}", response_model=PublicPost)
async def get_post(id: int) -> PublicPost:
    return dummies_post[id]



# Status Code
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post) -> Post:
    return post



# Status Code
@app.delete("/posts", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int) -> None:
    dummies_post.pop(id)
    return None