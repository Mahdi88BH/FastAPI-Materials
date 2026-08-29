from fastapi import FastAPI, Depends, Query

# In FastAPI, a dependency can be defined either as a function or as a callable class.

# async def pagination(skip: int = 0, limit: int = 10) -> tuple[int, int]:
#     return (skip, limit)


async def pagination(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=0),
        ) -> tuple[int, int]:
    capped_limit = min(100, limit)

    return (skip, capped_limit)


# async def get_post_or_404(id: int) -> Post:
#     try:
#         return db.posts[id]
#     except KeyError:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


app = FastAPI()



@app.get("/items")
async def list_items(p: tuple[int, int] = Depends(pagination)):
    skip, limit = p

    return {"skip": skip, "limit": limit}


@app.get("/things")
async def list_things(p: tuple[int, int] = Depends(pagination)):
    skip, limit = p

    return {"skip": skip, "limit": limit}


# @app.get("/posts/{id}")
# async def get(post: Post = Depends(get_post_or_404)):
#     return post

# @app.patch("/posts/{id}")
# async def update(post_update: PostUpdate, post: Post = Depends(get_post_or_404)):
#     updated_post = post.copy(update=post_update.dict())
#     db.posts[post.id] = updated_post
#     return updated_post

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete(post: Post = Depends(get_post_or_404)):
#     db.posts.pop(post.id)