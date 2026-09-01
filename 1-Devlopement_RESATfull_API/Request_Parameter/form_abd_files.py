# 1. IMPORTING REQUIRED MODULES
# 'FastAPI' is the main application class.
# 'Form' parses incoming HTML form data sent via 'application/x-www-form-urlencoded' or 'multipart/form-data'.
# 'File' tells FastAPI that a parameter should be treated as a raw file upload ('multipart/form-data').
# 'UploadFile' is FastAPI's rich, asynchronous file class backed by a temporary file on disk.
from fastapi import FastAPI, Form, File, UploadFile
from typing import List


# 2. INITIALIZING THE FASTAPI APP INSTANCE
app = FastAPI()


# 3. HTML FORM DATA HANDLING
# Note: Form data cannot be mapped directly from standard JSON bodies; it must be sent as 'application/x-www-form-urlencoded'.
@app.post("/form")
async def submit_form(
    # 'Form()': Instructs FastAPI to extract these values directly from the submitted HTML form fields.
    # Utility: Validates and casts form-encoded string inputs into appropriate Python types (e.g., 'age' cast to int).
    name: str = Form(), 
    age: int = Form()
):
    # Returns the parsed form fields as a JSON payload.
    return {"name": name, "age": age}


# 4. SMALL FILE UPLOADS IN MEMORY (`bytes`)
# Route: POST /file-bytes
# Note: Renamed endpoint path to avoid URL route collisions in FastAPI with the endpoint below.
@app.post('/file-bytes')
async def upload_file_bytes(
    # 'file: bytes = File()': Reads the entire uploaded file directly INTO MEMORY as raw bytes.
    # Utility: Best used ONLY for small files (e.g., small avatars, SVGs).
    # ⚠️ Warning: Uploading a 2GB file this way loads 2GB directly into server RAM, risking Out-Of-Memory crashes!
    file: bytes = File()
):
    # Returns the total size of the file buffer in bytes.
    return {"file_size_bytes": len(file)}


# 5. EFFICIENT SINGLE FILE UPLOAD (`UploadFile`)
# Route: POST /file
@app.post("/file")
async def upload_file_metadata(
    # 'UploadFile': Uses a spooling mechanism (stored in memory up to a small limit, then spooled to disk).
    # Utility: Handles large files (videos, datasets) safely without crashing RAM. 
    # Exposes rich metadata (.filename, .content_type) and async stream methods (.read(), .seek(), .write()).
    file: UploadFile = File(...)
):
    # Returns key metadata extracted from the file header without needing to read the entire file into memory.
    return {"filename": file.filename, "content_type": file.content_type}


# 6. MULTIPLE FILE UPLOADS (`List[UploadFile]`)
# Route: POST /files
@app.post("/files")
async def upload_multiple_files(
    # 'List[UploadFile]': Accepts multiple files submitted under a single multipart form field.
    # Utility: Ideal for bulk file batch processing (e.g., uploading a gallery of images or batch documents).
    files: List[UploadFile] = File(...)
):
    # Iterates through all uploaded file objects and returns a list of metadata dictionaries.
    return [
        {"filename": file.filename, "content_type": file.content_type} 
        for file in files
    ]