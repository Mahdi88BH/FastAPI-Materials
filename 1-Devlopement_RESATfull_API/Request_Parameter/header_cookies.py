# 1. IMPORTING REQUIRED MODULES
# 'FastAPI' is the main application class.
# 'Header' is used to extract and validate HTTP request headers (e.g., User-Agent, Authorization).
# 'Cookie' is used to extract and validate HTTP cookie values sent by the client.
from fastapi import FastAPI, Header, Cookie


# 2. INITIALIZING THE FASTAPI APP INSTANCE
app = FastAPI()


# 3. EXTRACTING CUSTOM HTTP HEADERS
# Route: GET /
@app.get("/")
async def hello(
    # 'Header(...)': Tells FastAPI to extract this value from the HTTP Request Headers.
    # '...': Means this header is strictly REQUIRED. If missing, FastAPI returns a 422 error.
    # Automatic Header Conversion: HTTP headers are case-insensitive (e.g., "Hello: world" or "hello: world").
    # FastAPI automatically normalizes the header key name so your code receives it consistently.
    hello: str = Header(...)
):
    # Example Request:  curl -H "hello: maroc" http://127.0.0.1:8000/
    # Returns:          {"hello": "maroc"}
    return {"hello": hello}


# 4. AUTOMATIC SNAKE_CASE TO HYPHENATED HEADER CONVERSION
# Route: GET /user-agent
@app.get("/user-agent")
async def get_user_agent(
    # Automatic Hyphenation: Standard HTTP headers use hyphens (e.g., "User-Agent", "X-Auth-Token").
    # Python variables cannot contain hyphens ('user-agent' is invalid Python syntax).
    # FastAPI automatically converts snake_case parameter names ('user_agent') 
    # to hyphenated header keys ('User-Agent') under the hood!
    user_agent: str = Header(...)
):
    # Example Request:  curl -H "User-Agent: Mozilla/5.0" http://127.0.0.1:8000/user-agent
    # Returns:          {"user_agent": "Mozilla/5.0"}
    return {"user_agent": user_agent}


# 5. EXTRACTING HTTP COOKIES
# Route: GET /cookies
@app.get("/cookies")
async def get_cookies(
    # 'Cookie(None)': Tells FastAPI to look inside the HTTP 'Cookie' header for a key named 'hello'.
    # 'str | None = ...': Declares this parameter as OPTIONAL (defaults to None if no cookie is sent).
    # Utility: Allows your backend to safely read session tokens or preferences stored in client cookies.
    hello: str | None = Cookie(None)
):
    # Example Request (No Cookie):   curl http://127.0.0.1:8000/cookies
    # Returns:                      {"hello": null}
    #
    # Example Request (With Cookie): curl --cookie "hello=sweet_cookie" http://127.0.0.1:8000/cookies
    # Returns:                      {"hello": "sweet_cookie"}
    return {"hello": hello}