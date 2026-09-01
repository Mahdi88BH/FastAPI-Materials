# 1. IMPORTING REQUIRED MODULES
# 'FastAPI' is the core application class.
# 'status' provides human-readable HTTP status code constants (e.g., status.HTTP_201_CREATED instead of raw magic numbers like 201).
# 'BaseModel' from Pydantic defines data models for validation and serialization.
from fastapi import FastAPI, status
from pydantic import BaseModel


# 2. INTERNAL DOMAIN MODEL
# Defines the complete schema for a Post within the application database/memory.
class Post(BaseModel):
    title: str
    nb_views: int


# 3. MOCK DATABASE INSTANCE
# Simulates a persistent key-value datastore mapping integer IDs to Post instances.
dummies_post = {
    1: Post(title="Data Science", nb_views=100),
    2: Post(title="Data Engeneering", nb_views=88)
}


# 4. PUBLIC RESPONSE MODEL (DATA FILTERING SCHEMA)
# Defines a restricted public view model containing ONLY fields intended for client exposure.
# Utility: Acts as a security firewall—hides internal/sensitive attributes (like 'nb_views', internal flags, or hashes) 
# before sending JSON back to the user.
class PublicPost(BaseModel):
    title: str


# 5. INITIALIZING THE FASTAPI APP INSTANCE
app = FastAPI()


# 6. RESPONSE MODEL FILTERING & ROUTE MATCHER
# Route: GET /posts/{id}
# 'response_model=PublicPost': Forces FastAPI to filter the returned object through the PublicPost schema.
# Even though 'dummies_post[id]' returns a full Post object with 'nb_views', FastAPI automatically strips 'nb_views' 
# and returns ONLY {"titel": "..."} to the client.
@app.get("/posts/{id}", response_model=PublicPost)
async def get_post(id: int) -> PublicPost:
    return dummies_post[id]


# 7. CREATION ENDPOINT WITH HTTP STATUS 201 CREATED
# Route: POST /posts
# 'status_code=status.HTTP_201_CREATED': Overrides the default HTTP 200 OK success code with 201 Created.
# Utility: Adheres strictly to REST API standards for resource creation.
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post) -> Post:
    return post


# 8. DELETION ENDPOINT WITH HTTP STATUS 204 NO CONTENT
# Route: DELETE /posts (via query parameter ?id=...)
# 'status_code=status.HTTP_204_NO_CONTENT': Sets response status to 204 No Content.
# Utility: Standard REST behavior for successful deletion operations where no response body is returned.
# Returning 'None' ensures the HTTP response payload body remains completely empty.
@app.delete("/posts", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int) -> None:
    dummies_post.pop(id)
    return None