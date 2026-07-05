from fastapi import FastAPI, Query


app = FastAPI()


@app.get("/users")
def get_user(page: int = Query(1, gt=0), 
            size: int = Query(10, lt=100)) -> dict:
    return {"page": page, "size": size}