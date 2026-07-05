from fastapi import FastAPI


app = FastAPI()

@app.get('/')
def gretting() -> dict:
    return {"Hello": "Maroc"}

