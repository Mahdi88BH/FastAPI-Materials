from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/hi")
def greetting():
    return "Welcome there"


# Run The application in internal way using uvicorn.run() method. This is useful when you want to run the application directly from the script without using the command line.
if __name__ == "__main__":

    import uvicorn
    uvicorn.run("hello:app", reload=True)

# Run the application in external way using the commande line
# uvicorn hello:app --reload