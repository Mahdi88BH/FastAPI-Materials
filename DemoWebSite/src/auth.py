import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials


app = FastAPI()

user_secrete: str = "mahdi"
password_secrete: str = "mahdi88"


basic = HTTPBasic()

@app.get("/who")
def get_user(creds: HTTPBasicCredentials = Depends(basic)):
    if user_secrete == creds.username and password_secrete == creds.password:
        return {"username": creds.username, "password": creds.password}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not found")


if __name__ == "__main__":
    uvicorn.run("auth:app", reload=True)