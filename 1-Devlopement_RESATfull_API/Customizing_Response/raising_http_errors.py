from fastapi import FastAPI, status, HTTPException, Body


app = FastAPI()


@app.post("/password")
def sign_up(
    password: str = Body(...), 
    confr_pass: str = Body(...)):

    if password != confr_pass:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="The Password don't match"
        )
    return {"Sign_Up": "Seccuful"}