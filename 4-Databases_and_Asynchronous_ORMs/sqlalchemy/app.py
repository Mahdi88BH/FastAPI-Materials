import contextlib

from fastapi import FastAPI

from database import create_all_tables


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all_tables()
    yield


app = FastAPI(lifespan=lifespan)


