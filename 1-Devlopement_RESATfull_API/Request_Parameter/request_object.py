# 1. IMPORTING REQUIRED MODULES
# 'FastAPI' is the core application framework.
# 'Request' from fastapi (re-exported from Starlette) gives access to the raw incoming HTTP request object.
from fastapi import FastAPI, Request


# 2. INITIALIZING THE FASTAPI APP
app = FastAPI()


# 3. ACCESSING THE RAW REQUEST OBJECT
# Route: GET /request
@app.get("/request")
async def get_request_data(
    # 'request: Request': Declaring a parameter of type 'Request' tells FastAPI to inject 
    # the underlying raw HTTP request object directly into your function.
    # Utility: Gives you low-level access to request metadata that FastAPI high-level 
    # abstractions might abstract away—such as client IP address, URL components, raw body bytes, 
    # query params, request scheme (http/https), and connection headers.
    request: Request
):
    # 'request.url.path': Extracts the path component of the requested URL (e.g., "/request").
    # Returns the path string inside a JSON object response.
    return {"path": request.url.path}



@app.get("/request-debug")
async def debug_request(request: Request):
    return {
        "client_ip": request.client.host,        # e.g., "127.0.0.1"
        "method": request.method,               # e.g., "GET"
        "full_url": str(request.url),           # e.g., "http://127.0.0.1:8000/request-debug?key=val"
        "headers": dict(request.headers),       # All headers as a standard Python dict
        "query_params": dict(request.query_params) # e.g., {"key": "val"}
    }