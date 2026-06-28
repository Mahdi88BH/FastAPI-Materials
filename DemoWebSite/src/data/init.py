import os
from sqlite3 import connect, Connection, Cursor, IntegrityError
from pathlib import Path
from typing import Optional

# --- GLOBAL STATE INITIALIZATION ---
# Initialize global variables to hold the active database connection and cursor.
# Setting them to None acts as a structural flag indicating the database is not connected yet.
conn: Connection | None = None
curs: Optional[Cursor] = None


def get_db(name: str | None = None, reset: bool = False):
    """Establishes a global, single-instance connection and cursor for the database.

    :param name: Optional string path to the database file.
    :param reset: If True, forces the current connection to close and recreates it.
    """
    # Instructs the function to modify the variables defined outside this function
    # at the global module level, instead of creating temporary local variables.
    global conn, curs

    # --- CHECK EXISTING CONNECTION (SINGLETON PATTERN) ---
    if conn:
        if not reset:
            # If a connection already exists and we ARE NOT forcing a reset,
            # exit the function early to reuse the existing connection.
            return
        # If reset=True, clear the connection variable so a new one can be made below.
        conn = None

    # --- DYNAMIC DATABASE PATH RESOLUTION ---
    if not name:
        # Step 1: Look for an environment variable named "CRYPTID_SQLITE_DB".
        name = os.getenv("CRYPTID_SQLITE_DB")

        # Step 2: Fallback to constructing an absolute local path if the env variable is missing.
        # Path(__file__) finds this current script file.
        # .resolve() gets the absolute path name.
        # .parents[1] navigates 2 levels up to find the root folder of the repository.
        top_dir = Path(__file__).resolve().parents[1]

        # Combine paths to point to a 'db' directory and file: /your/repo/top/db/cryptid.db
        db_dir = top_dir / "db"
        db_name = "cryptid.db"
        db_path = str(db_dir / db_name)

        # Re-verify environment variable; if still empty, default to the generated fallback absolute path string.
        name = os.getenv("CRYPTID_SQLITE_DB", db_path)

    # --- DRIVER INVOCATION (DB-API) ---
    # Open the network file connection pipe using the resolved path.
    # 'check_same_thread=False' allows multiple threads (like FastAPI's async loops)
    # to access this connection safely without throwing a multi-threading error.
    conn = connect(name, check_same_thread=False)

    # Spawn the cursor execution pointer to allow the app to run SQL queries over the connection.
    curs = conn.cursor()


# --- BOOTSTRAP TRIGGER ---
# Triggers the function immediately on startup to ensure the global 'conn' and 'curs'
# are fully loaded and ready for the rest of the application to import and execute.
# (Note: Added "= None" to the signature above so it can run without passing an argument)
get_db()




# 🧠 Important Considerations for this Architecture
# While this pattern works perfectly for small standalone scripts or 
# quick data automation prototypes, it presents two major drawbacks 
# when scaling up to high-traffic frameworks like FastAPI:

#   1.Global State Blocking: Utilizing a single global connection 
# block means all database commands share the same state. If two 
# users execute complex updates at the exact same millisecond, they 
# can cross paths or collide on the single open curs wrapper.

#   2.Hard to Test: Global variables are inherently difficult to 
# isolate during testing.

# As you move further into your FastAPI development journey, you will
# replace this global pattern by moving this exact instantiation into
# a Dependency Injection function (yield db) as we studied previously,
# allowing FastAPI to generate clean, safely isolated connection 
# handles automatically for every web request!
