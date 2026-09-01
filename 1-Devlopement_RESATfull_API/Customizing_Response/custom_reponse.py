# 1. IMPORTING SPECIFIC RESPONSE CLASSES
# By default, FastAPI returns JSONResponse (serializing python dicts/models into JSON).
# Importing specialized response classes allows returning custom content-types like raw HTML, 
# plain text, HTTP redirects, direct file downloads, or custom media types (XML, CSV).
from fastapi.responses import (
    HTMLResponse, 
    PlainTextResponse,
    RedirectResponse,
    FileResponse)
from fastapi import FastAPI, Response, status
from pathlib import Path


# 2. INITIALIZING THE FASTAPI APP INSTANCE
app = FastAPI()


# 3. RETURNING RAW HTML RESPONSES
# Route: GET /html
# 'response_class=HTMLResponse': Informs FastAPI and OpenAPI/Swagger docs that this endpoint 
# returns raw HTML string instead of JSON. Sets 'Content-Type: text/html'.
@app.get("/html", response_class=HTMLResponse)
async def get_html_content():
    # Returns a multi-line raw HTML string directly rendered by client browsers.
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


# 4. RETURNING PLAIN TEXT RESPONSES
# Route: GET /text
# 'response_class=PlainTextResponse': Sets header 'Content-Type: text/plain'.
# Utility: Ideal for returning raw log outputs, plain configuration files, or simple string status checks.
@app.get("/text", response_class=PlainTextResponse)
async def get_text_context():
    return "Salaaaaaaaam"


# 5. PERFORMING HTTP REDIRECTS
# Route: GET /redirect
# 'RedirectResponse': Instructs the client browser or API client to automatically navigate to a different URL.
# 'status_code=status.HTTP_301_MOVED_PERMANENTLY': Sets HTTP 301 status (Permanent Redirect).
# Note: For temporary redirects, use 302 Found or 307 Temporary Redirect instead.
@app.get('/redirect')
async def redirect():
    return RedirectResponse("/new-Url", 
                            status_code=status.HTTP_301_MOVED_PERMANENTLY)


# 6. SERVING LOCAL FILES AUTOMATICALLY (`FileResponse`)
# Route: GET /image
# 'FileResponse': Takes a local filesystem path, efficiently streams the file in chunks, 
# and automatically sets the correct Content-Type (e.g., 'image/png') and Content-Length headers.
@app.get("/image")
async def get_file():
    # Constructing a dynamic path using pathlib.Path relative to the project directory
    root_directory = Path(__file__).parent.parent.parent
    picture_path = root_directory / "images" / "BluePrint_Architecture.png"

    # Efficiently streams the requested binary image directly to the client
    return FileResponse(picture_path)


# 7. RETURNING CUSTOM MEDIA TYPES (RAW XML / CSV / CUSTOM FORMATS)
# Route: GET /xml
# 'Response(content=..., media_type=...)': The base response class.
# Utility: Allows manual override to send custom data formats (like XML, SVG, iCal, or CSV) 
# by explicitly defining the string payload and setting 'media_type="application/xml"'.
@app.get('/xml')
async def get_xml_content():
    content = """<?xml version="1.0" encoding="UTF-8"?> 
    <Hello>World</Hello> """
    return Response(content=content, media_type="application/xml")