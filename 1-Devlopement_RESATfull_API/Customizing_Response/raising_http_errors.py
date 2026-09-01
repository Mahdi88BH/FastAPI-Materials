# 1. IMPORTING REQUIRED MODULES
# 'FastAPI' is the main application class.
# 'status' provides standard HTTP status code constants (e.g., status.HTTP_400_BAD_REQUEST).
# 'HTTPException' is FastAPI's custom exception class to halt request processing and return structured JSON errors.
# 'Body' is used to extract standalone keys directly from the JSON request payload.
from fastapi import FastAPI, status, HTTPException, Body


# 2. INITIALIZING THE FASTAPI APP INSTANCE
app = FastAPI()


# 3. SIGN-UP ROUTE WITH MANUAL VALIDATION & EXCEPTION HANDLING
# Route: POST /password
@app.post("/password")
def sign_up(
    # 'password': Extracts 'password' key from top-level JSON request body.
    # 'Body(...)': Indicates that this field is strictly REQUIRED.
    password: str = Body(...), 
    
    # 'confr_pass': Extracts 'confr_pass' key from top-level JSON request body.
    # 'Body(...)': Indicates that this field is strictly REQUIRED.
    confr_pass: str = Body(...)
):
    # 4. BUSINESS LOGIC & CUSTOM VALIDATION CHECK
    # Checks if the provided password string matches the confirmation password string.
    if password != confr_pass:
        # 'raise HTTPException(...)': Immediately aborts function execution!
        # Stops further processing and sends an HTTP 400 Bad Request response back to the client.
        # Utility: Ensures client receives a clean, standardized error response structure:
        # {"detail": "The Password don't match"}
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The Password don't match"
        )
    
    # 5. SUCCESSFUL RESPONSE
    # If validation passes, returns a JSON confirmation response (defaults to HTTP 200 OK).
    return {"Sign_Up": "Seccuful"}