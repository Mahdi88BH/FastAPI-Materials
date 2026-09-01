# 1. IMPORTING REQUIRED MODULES
# 'FastAPI' is the main application class.
# 'status' provides standard HTTP status constants (e.g., status.HTTP_201_CREATED).
# 'Response' gives low-level programmatic control over headers, cookies, and status codes for the current response.
# 'BaseModel' defines Pydantic data validation structures.
from fastapi import FastAPI, status, Response
from pydantic import BaseModel


# 2. DEFINING SCHEMAS AND MOCK DATABASE
class Post(BaseModel):
    title: str

dummies_posts = {
    1: Post(title="Data Science"),
    2: Post(title="Data Engeneering")
}

# 3. INITIALIZING THE FASTAPI APP INSTANCE
app = FastAPI()


# 4. CUSTOM HEADERS & COOKIES VIA RESPONSE PARAMETER
# Route: GET /
@app.get("/")
async def get_header(
    # 'response: Response': Injecting the Response object allows dynamically modifying response metadata 
    # without breaking the convenience of returning a standard Python dictionary.
    response: Response
) -> dict:
    
    # Setting a custom HTTP response header
    # Utility: Useful for sending metadata like request tracing IDs, cache controls, or custom server signatures.
    response.headers["Custome-Header"] = "Custome-Hedear-Value"
    
    # Setting a client-side HTTP Cookie
    # 'max_age=86400': Sets cookie lifespan in seconds (86400 seconds = 24 hours).
    # Utility: Stores session tokens, auth keys, or user preferences in client browsers/HTTP engines.
    response.set_cookie(
        "cookie-name", 
        "cookie-value", 
        max_age=86400
    )
    
    # Returns the main JSON body payload while attached headers and cookies are sent along automatically.
    return {"hello": "Salam"}


# 5. DYNAMIC STATUS CODES (UPSERT PATTERN)
# Route: PUT /posts/{id}
@app.put("/posts/{id}")
async def get_posts(
    id: int, 
    response: Response, 
    post: Post
) -> Post:
    
    # Checks if the target resource ID already exists in the dictionary.
    if id not in dummies_posts:
        # UPSERT Behavior: If the ID does NOT exist, create the new record 
        # and dynamically change the HTTP status code from default 200 OK to 201 Created!
        # Utility: Enables RESTful update-or-create logic where creation yields 201 and update yields 200.
        response.status_code = status.HTTP_201_CREATED
        dummies_posts[id] = post
        
    # If the ID exists, it updates or returns the existing resource with default status 200 OK.
    return dummies_posts[id]