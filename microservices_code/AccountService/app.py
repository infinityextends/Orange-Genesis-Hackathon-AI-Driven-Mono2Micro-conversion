from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Optional

from account_service.routes import accounts, authentication

app = FastAPI()

# Mount static files (for serving CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Include routers from modules
app.include_router(accounts.router)
app.include_router(authentication.router)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Root endpoint to serve the basic HTML UI.
    """
    return templates.TemplateResponse("index.html", {"request": request})
