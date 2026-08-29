from fastapi import FastAPI, Form, File, UploadFile
from typing import List


app = FastAPI()

# The form does not allow to us to define pydantic model
@app.post("/form")
async def submit_form(name: str = Form(), age: int = Form()):
    return {"name": name, "age": age}


# Upload single ressource
@app.post('/file')
async def upload_file(file: bytes = File()):
    return {"file": len(file)}



# UploadFile alloaw is to retrive the metadata of the content
@app.post("/file")
async def upload_files(file: UploadFile = File(...)):
    return {"filename": file.filename, "content_type": file.content_type}


@app.post("/files")
async def upload_files(files: List[UploadFile] = File(...)):
    return [
        {"filename": file.filename, "content_type": file.content_type} 
        for file in files
    ]