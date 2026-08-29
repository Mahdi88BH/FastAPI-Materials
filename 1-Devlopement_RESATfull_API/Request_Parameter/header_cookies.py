from fastapi import FastAPI, Header, Cookie


app = FastAPI()


# Convert name key to lower case
@app.get("/")
async def hello(hello: str = Header(...)):
    return {"hello": hello}


# automaticlt Convert snack_case
@app.get("/user-agent")
async def get_user_agent(user_agent: str = Header(...)):
    return {"user_agent": user_agent}


@app.get("/cookies")
async def get_cookies(hello: str | None = Cookie(None)):
    return {"hello": hello}