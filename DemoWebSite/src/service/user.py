from datetime import timedelta, datetime
import os
from jose import jwt
from model.user import User
from typing import Optional, List

# --- CONDITIONAL DATABASE/DATA LAYER INJECTION ---
# This checks if an environment variable is flagged for testing.
# It swaps out your actual production data layer for an in-memory mock/fake layer cleanly.
if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import user as data
else:
    from data import user as data

from passlib.context import CryptContext

# --- CRYPTOGRAPHIC CONFIGURATION ---
# CRITICAL SECURITY WARNING: This key must be moved to a hidden environment variable (.env) in production.
SECRET_KEY = "keep-it-secret-keep-it-safe"
ALGORITHM = "HS256" # Symmetric cryptographic algorithm (HMAC with SHA-256)

# Initializes Passlib's hashing configuration engine.
# By choosing "bcrypt", it ensures passwords are salted and hashed with a slow algorithm to prevent brute-force attacks.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# =====================================================================
# 1. PASSWORD CRYPTOGRAPHY LAYER
# =====================================================================

def verify_password(plain: str, hash: str) -> bool:
    """Compares a plain text password against an encrypted database hash string.

    Returns True if they match, preventing timing attacks.
    """
    return pwd_context.verify(plain, hash)


def get_hash(plain: str) -> str:
    """Transforms a plain text password into an irreversible, salted cryptographic hash

    string to store safely in the database.
    """
    return pwd_context.hash(plain)


# =====================================================================
# 2. JWT DECODING & IDENTITY PARSING
# =====================================================================

def get_jwt_username(token: str) -> Optional[str]:
    """Intercepts an incoming token string, decrypts/verifies its signature,

    and extracts the subject identification name.
    """
    try:
        # Decode the token using our local hidden key. 
        # If any character was altered by a hacker, this line throws a JWTError instantly.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # 'sub' (Subject) is the standard JWT open-spec claim key containing the username/identity identifier.
        # This uses Python's walrus operator (:=) to assign and check presence simultaneously.
        if not (username := payload.get("sub")):
            return None
    except jwt.JWTError:
        # Captures invalid signatures, tampered payloads, or expired tokens safely.
        return None
    return username


def get_current_user(token: str) -> Optional[User]:
    """The core identity resolver function.

    Takes a string token, finds the username, and fetches the full User data object.
    """
    if not (username := get_jwt_username(token)):
        return None
    if (user := lookup_user(username)):
        return user
    return None


def lookup_user(username: str) -> Optional[User]:
    """Direct database abstraction query wrapper to look up a record by username."""
    if (user := data.get_one(username)):
        return user
    return None


# =====================================================================
# 3. AUTHENTICATION (LOGIN FLOW ENTRY POINT)
# =====================================================================

def auth_user(name: str, plain: str) -> Optional[User]:
    """Verifies a user's initial login attempt credentials.

    Checks existence first, then mathematically checks the password accuracy.
    """
    # Guard clause: If the username doesn't exist in the system, exit immediately.
    if not (user := lookup_user(name)):
        return None
        
    # Guard clause: If the hash validation fails, reject access.
    if not verify_password(plain, user.hash):
        return None
    
    # Credentials are fully validated; hand back the valid User domain object model.
    return user


# =====================================================================
# 4. TOKEN CREATION UTILITY (OUTBOUND CREDENTIAL)
# =====================================================================

def create_access_token(data: dict, expires: Optional[timedelta]):
    """Generates a secure, time-limited signed JWT string token to send back to the client browser."""
    # Create a shallow copy of the incoming payload data dict to avoid mutating original objects.
    src = data.copy()
    
    # Calculate universal time synchronization anchors.
    now = datetime.utcnow()

    # Enforce an automatic fallback lifetime safety limit if no expiration window is requested.
    if not expires:
        expires = timedelta(minutes=15)
    
    # Append the mandatory 'exp' (Expiration Time) claim metadata into the token body payload.
    src.update({"exp": now + expires})
    
    # Package, compress, and cryptographically sign the data dictionary package.
    encoded_jwt = jwt.encode(src, SECRET_KEY, algorithm=[ALGORITHM])

    return encoded_jwt


def get_all() -> List[User]:
    return data.get_all()


def get_one(name: str) -> User:
    return data.get_one(name)


def create(user: User) -> User:
    return data.create(user)


def modify(name: str, user: User) -> User:
    return data.modify(name, user)


def delete(name: str) -> None:
    return data.delete(name)
