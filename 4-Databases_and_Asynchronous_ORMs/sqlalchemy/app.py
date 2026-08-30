import contextlib

from fastapi import FastAPI, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

import schemas
from models import Post
from database import create_all_tables


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all_tables()
    yield


app = FastAPI(lifespan=lifespan)



@app.post('/posts', response_model=schemas.PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_create: schemas.PostCreate, session: AsyncSession = Depends
) -> Post:

    post = Post(**post_create.model_dump())
    session.add(post)
    await session.commit()

    return post
