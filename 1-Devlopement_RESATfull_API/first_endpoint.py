# 1. IMPORTING THE FASTAPI ENGINE
# We import the core 'FastAPI' Python class from the fastapi package.
# Utility: This class provides all the underlying functionality needed to build, 
# validate, and expose your Web API routes and documentation.
from fastapi import FastAPI


# 2. CREATING THE APPLICATION INSTANCE
# We instantiate the FastAPI class into a variable named 'app'.
# Utility: This 'app' object serves as the central router and application entry point.
# It manages all incoming HTTP requests, middleware, CORS settings, and automatically 
# generates your OpenAPI/Swagger documentation at '/docs'.
app = FastAPI()


# 3. PATH OPERATION DECORATOR
# The decorator @app.get('/') tells FastAPI that the function directly below it 
# should handle incoming HTTP 'GET' requests sent to the root path ('/').
# Utility: It maps a specific URL path ('/') and HTTP method ('GET') to a dedicated Python function.
@app.get('/')
# 4. ASYNCHRONOUS PATH OPERATION FUNCTION
# 'async def' defines an asynchronous non-blocking function named 'gretting'.
# '-> dict' is a Python Type Hint indicating that this function returns a dictionary.
# Utility: Using 'async' allows the FastAPI event loop to handle thousands of concurrent 
# connections efficiently without freezing the thread while waiting for network I/O.
async def gretting() -> dict:
    
    # 5. RETURNING THE RESPONSE
    # Returns a standard Python dictionary.
    # Utility: FastAPI automatically serializes this Python dictionary into a 
    # valid JSON string response ({"Hello": "Maroc"}) and sets the HTTP response 
    # header 'Content-Type: application/json' automatically.
    return {"Hello": "Maroc"}