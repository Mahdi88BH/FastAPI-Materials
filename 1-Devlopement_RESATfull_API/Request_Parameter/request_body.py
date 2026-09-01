# 1. IMPORTING REQUIRED MODULES
# 'FastAPI' is the core application class.
# 'Body' is used to extract, validate, and apply constraints to standalone fields 
# sent inside the HTTP JSON request body alongside or outside of Pydantic models.
# 'BaseModel' from Pydantic is used to define structured schemas for request/response payloads.
from fastapi import FastAPI, Body
from pydantic import BaseModel


# 2. DEFINING A PYDANTIC DATA MODEL
# Pydantic models define the expected structure, field types, and validation rules for JSON bodies.
# Utility: FastAPI uses this model to automatically parse, validate, and convert the incoming 
# JSON payload into a clean Python object with type safety (`user.name`, `user.age`).
class User(BaseModel):
    name: str  # Must be a string
    age: int   # Must be an integer


# 3. INITIALIZING THE FASTAPI APP INSTANCE
app = FastAPI()


# 4. POST PATH OPERATION WITH A COMPOSITE JSON REQUEST BODY
# Registers a POST endpoint at "/users" (typically used for creating resources or submitting forms).
@app.post("/users")
async def get_info_user(
    # 'user': Because 'User' inherits from BaseModel, FastAPI automatically expects 
    # a JSON object matching this schema inside the incoming request body.
    user: User, 
    
    # 'property': Uses 'Body()' to declare a singular, primitive value directly inside the JSON body.
    # 'lt=3': (Less Than) Must be strictly less than 3 (i.e., 1 or 2 for integers).
    # 'gt=0': (Greater Than) Must be strictly greater than 0.
    # Utility: Instructs FastAPI to expect a top-level key named "property" in the same JSON payload 
    # alongside the "user" object key, enforcing numeric constraints on it.
    property: int = Body(lt=3, gt=0)
):
    
    # Expected JSON Payload Structure for this route:
    # {
    #   "user": {
    #     "name": "Mahdi",
    #     "age": 22
    #   },
    #   "property": 2
    # }
    
    # Returns the parsed user Pydantic model and the validated property back as a JSON response.
    return {"user": user, "property": property}