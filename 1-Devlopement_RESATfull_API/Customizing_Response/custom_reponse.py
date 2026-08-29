# - HTMLResponse: This can be used to return an HTML response
# - PlainTextResponse: This can be used to return raw text
# - RedirectResponse: This can be used to make a redirection
# - StreamingResponse: This can be used to stream a flow of bytes
# - FileResponse: This can be used to automatically build a proper 
#     file response given the path of a file on the local disk

from fastapi.responses import (
    HTMLResponse, 
    PlainTextResponse,
    RedirectResponse,
    FileResponse)
from fastapi import FastAPI, Response, status
from pathlib import Path

app = FastAPI()

@app.get("/html", response_class=HTMLResponse)
async def get_html_content():
    return """
            <html>
                <head>
                    <title>Hello world!</title>
                </head>
                <body>
                    <h1>Hello world!</h1>
                </body>
            </html>
"""

@app.get("/text", response_class=PlainTextResponse)
async def get_text_context():
    return "Salaaaaaaaam"


@app.get('/redirect')
async def redirect():
    return RedirectResponse("/new-Url", 
                            status_code=status.HTTP_301_MOVED_PERMANENTLY)


@app.get("/image")
async def get_file():
    root_directory = Path(__file__).parent.parent.parent
    picture_path = root_directory / "images" / "BluePrint_Architecture.png"

    return FileResponse(picture_path)


@app.get('/xml')
async def get_xml_content():
    content = """<?xml version="1.0" encoding="UTF-8"?> 
    <Hello>World</Hello> """
    return Response(content=content, media_type="application/xml")