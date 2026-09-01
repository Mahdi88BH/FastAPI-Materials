# 1. IMPORTING REQUIRED MODULES
# 'FastAPI' is the main web application class.
# 'Query' is used to define default values, numeric constraints, and validation metadata 
# specifically for HTTP URL Query Parameters (the key-value pairs after '?' in a URL).
from fastapi import FastAPI, Query


# 2. INITIALIZING THE FASTAPI APP INSTANCE
# Creates the core app instance to manage routes, execution, and docs generation.
app = FastAPI()


# 3. PATH OPERATION DECORATOR
# Maps GET requests on the "/users" path (e.g., GET /users?page=2&size=20) to the function below.
@app.get("/users")
async def get_user(
    # 'page': Declares an optional query parameter mapped from '?page=...' in the URL.
    # Default value = 1: If the client sends no '?page=' parameter, 'page' defaults to 1.
    # 'gt=0': (Greater Than) Enforces that page must be strictly greater than 0 (e.g., 1, 2, 3...).
    # Utility: Prevents invalid page indices like 0 or negative numbers from causing database offset errors.
    page: int = Query(1, gt=0), 
    
    # 'size': Declares a query parameter for pagination size mapped from '?size=...' in the URL.
    # Default value = 10: If omitted by the client, it defaults to 10 items per page.
    # 'lt=100': (Less Than) Enforces that size must be strictly less than 100 (e.g., maximum 99).
    # Utility: Protects your backend/database against Denial of Service (DoS) attacks where a user 
    # requests a massive limit like '?size=1000000' and crashes server memory.
    size: int = Query(10, lt=100)
) -> dict:
    
    # Returns the validated and type-casted integers directly as a JSON response payload.
    return {"page": page, "size": size}