from enum import Enum
from fastapi import FastAPI, Path


class usetType(str, Enum):
    ADMIN = "admin"
    CLIENT = "client"
    

app = FastAPI()


@app.get('/users/{role}/{id}')
async def get_user(role: usetType, id: int = Path(..., gt=1)) -> dict:
    return {"retrive": {
        'id': id,
        "role": role,
    }}


@app.get('/licenses/{license}')
def get_license(license: str = Path(..., 
                                    max_length=9, 
                                    min_length=9,
                                    regex=r"^\w{2}-\d{3}-\w{2}$")) -> dict:
    return {"lisence": license}