from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from typing import Optional

import requests

app = FastAPI()

# Serve static files (like CSS, JavaScript)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Replace with your actual service URLs
CATALOG_SERVICE_URL = "http://localhost:8001"  # Example
ACCOUNT_SERVICE_URL = "http://localhost:8002"  # Example
ORDER_SERVICE_URL = "http://localhost:8003"  # Example
CART_SERVICE_URL = "http://localhost:8004"  # Example


# Placeholder functions for responsibilities
async def get_catalog_data():
    """Fetches catalog data from the CatalogService."""
    try:
        response = requests.get(f"{CATALOG_SERVICE_URL}/catalog")
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching catalog data: {e}")
        return []

async def get_cart_data():
    """Fetches cart data from the CartService."""
    try:
        response = requests.get(f"{CART_SERVICE_URL}/cart")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching cart data: {e}")
        return []

async def get_order_data():
    """Fetches order data from the OrderService."""
    try:
        response = requests.get(f"{ORDER_SERVICE_URL}/orders")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching order data: {e}")
        return []

async def authenticate_user(username, password):
    """Authenticates user against the AccountService."""
    try:
        response = requests.post(f"{ACCOUNT_SERVICE_URL}/login", json={"username": username, "password": password})
        response.raise_for_status()
        return response.json()  # Expecting a token or user info
    except requests.exceptions.RequestException as e:
        print(f"Error authenticating user: {e}")
        return None

async def register_user(username, password, email):
    """Registers a new user via the AccountService."""
    try:
        response = requests.post(f"{ACCOUNT_SERVICE_URL}/register", json={"username": username, "password": password, "email": email})
        response.raise_for_status()
        return response.json()  # Expecting confirmation or user info
    except requests.exceptions.RequestException as e:
        print(f"Error registering user: {e}")
        return None


# API Endpoints
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serves the main page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    """Serves the login form."""
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    """Handles user login."""
    user = await authenticate_user(username, password)
    if user:
        # Successful login - Redirect to the catalog or profile page
        return RedirectResponse(url="/catalog", status_code=302) # Redirect
    else:
        # Failed login - Show error on the login page
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

@app.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    """Serves the registration form."""
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register", response_class=HTMLResponse)
async def register(request: Request, username: str = Form(...), password: str = Form(...), email: str = Form(...)):
    """Handles user registration."""
    result = await register_user(username, password, email)
    if result:
        # Successful registration - Redirect to login or profile page
        return RedirectResponse(url="/login", status_code=302)
    else:
        # Failed registration - Show error on the registration page
        return templates.TemplateResponse("register.html", {"request": request, "error": "Registration failed"})


@app.get("/catalog", response_class=HTMLResponse)
async def read_catalog(request: Request):
    """Displays the catalog."""
    catalog_data = await get_catalog_data()
    return templates.TemplateResponse("catalog.html", {"request": request, "catalog": catalog_data})


@app.get("/cart", response_class=HTMLResponse)
async def read_cart(request: Request):
    """Displays the cart."""
    cart_data = await get_cart_data()
    return templates.TemplateResponse("cart.html", {"request": request, "cart": cart_data})


@app.get("/orders", response_class=HTMLResponse)
async def read_orders(request: Request):
    """Displays the user's orders."""
    order_data = await get_order_data()
    return templates.TemplateResponse("orders.html", {"request": request, "orders": order_data})
