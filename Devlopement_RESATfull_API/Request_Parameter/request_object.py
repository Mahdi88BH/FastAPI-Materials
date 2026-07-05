from fastapi import FastAPI, Request


app = FastAPI()


@app.get("/request")
async def get_request_data(request: Request):
    return {"path": request.url.path}
