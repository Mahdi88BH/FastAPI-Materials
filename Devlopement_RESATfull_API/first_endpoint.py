from fastapi import FastAPI


app = FastAPI()

@app.get('/')
async def gretting() -> dict:
    return {"Hello": "Maroc"}

