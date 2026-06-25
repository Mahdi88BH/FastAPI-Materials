from fastapi import FastAPI, Body, Header, Response
import uvicorn

app = FastAPI()

# Adding in URL Path a Path Parameters => who
# Adding Query Parameters => year in the end of URL
@app.get("/hi/{who}")
def greetting(who: str, year: int):
    return f"Welcome {who} to FastAPI Application in the year {year}"

@app.post('/hi')
def greet(who: str = Body(embed=True)):
    return f"Hello {who} to FastAPI Aplication using Body Parameters"

@app.post("/hii")
def greet2(who: str = Header()):
    return f"Hello {who} to FastAPI Aplication using Header Parameters"

# FastAPI converts HTTP header keys to lowercase, and converts 
# a hyphen (-) to an underscore (_)
@app.post("/agent")
def get_agent(user_agent: str = Header()):
    return user_agent

@app.get("/happy", status_code=200)
def happy(status_code= 200):
    return {"message": "Happy to see you in FastAPI Application"}

# Inject custom headers into the response header using the Response object.
@app.get("/header/{name}/{value}")
def header(name: str, value: str, response: Response):
    response.headers[name] = value
    return {"message": "Header added successfully"}



# Run The application in internal way using uvicorn.run() method. This is useful when you want to run the application directly from the script without using the command line.
if __name__ == "__main__":

    uvicorn.run("hello:app", reload=True)

# Run the application in external way using the commande line
# uvicorn hello:app --reload