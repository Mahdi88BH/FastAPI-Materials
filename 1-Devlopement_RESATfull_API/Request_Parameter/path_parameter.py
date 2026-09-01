# 1. IMPORTING REQUIRED MODULES
# 'Enum' allows creating enumerated constants (fixed set of valid choices).
# 'FastAPI' is the main application class.
# 'Path' is used to declare validation constraints and metadata specifically for URL path parameters.
from enum import Enum
from fastapi import FastAPI, Path


# 2. DEFINING AN ENUM FOR ENFORCED URL CHOICES
# Inheriting from (str, Enum) ensures the values are strings and can be directly serialized to JSON.
# Utility: Restricts the URL path parameter to only a fixed set of predefined choices ("admin" or "client").
# If a user passes anything else (e.g., /users/guest/5), FastAPI automatically rejects it with a 422 error.
# It also provides auto-completion in the generated Swagger UI documentation.
class usetType(str, Enum):
    ADMIN = "admin"
    CLIENT = "client"


# 3. INITIALIZING THE FASTAPI APP
# Creates the core application instance to register routes and handle HTTP traffic.
app = FastAPI()


# 4. ROUTE WITH ENUM AND NUMERIC PATH PARAMETER VALIDATION
# Defines a GET endpoint expecting two dynamic URL parameters: {role} and {id}.
@app.get('/users/{role}/{id}')
async def get_user(
    # 'role': Automatically validates that the URL string matches one of the usetType Enum choices.
    role: usetType, 
    
    # 'id': Uses Path(...) to apply numeric constraints.
    # '...': Indicates that this path parameter is strictly REQUIRED.
    # 'gt=1': (Greater Than) Enforces that the ID must be an integer strictly greater than 1 (e.g., 2, 3, 4...).
    # Utility: Prevents invalid IDs (like 0, negative numbers, or non-integers) from ever reaching your inner code.
    id: int = Path(..., gt=1)
) -> dict:
    
    # Returns the validated inputs as a JSON payload.
    # Note: 'role' (Enum) automatically serializes to its string value in the output.
    return {
        "retrive": {
            'id': id,
            "role": role,
        }
    }


# 5. ROUTE WITH STRING PATTERN (REGEX) PATH PARAMETER VALIDATION
# Defines a GET endpoint taking a license string from the URL path.
@app.get('/licenses/{license}')
# Note: This function uses standard 'def' (synchronous) instead of 'async def'.
# Utility: FastAPI automatically runs standard synchronous functions in an external thread pool 
# so they don't block the main asyncio event loop.
def get_license(
    license: str = Path(
        ..., 
        # 'min_length=9' & 'max_length=9': Enforces that the string must be EXACTLY 9 characters long.
        max_length=9, 
        min_length=9,
        
        # 'regex=r"..."' (or 'pattern' in newer FastAPI versions): 
        # Validates the string against a Regular Expression pattern.
        # Break down of r"^\w{2}-\d{3}-\w{2}$":
        #   ^           : Start of string
        #   \w{2}       : Exactly 2 word characters (letters/numbers/underscore)
        #   -           : A literal hyphen
        #   \d{3}       : Exactly 3 digits (numbers)
        #   -           : A literal hyphen
        #   \w{2}       : Exactly 2 word characters
        #   $           : End of string
        # Example valid input: "AB-123-CD" or "MA-888-BH"
        regex=r"^\w{2}-\d{3}-\w{2}$"
    )
) -> dict:
    
    # Returns the validated license string as a JSON response.
    return {"lisence": license}