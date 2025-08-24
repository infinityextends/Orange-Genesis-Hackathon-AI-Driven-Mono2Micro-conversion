# CartService

A simple Cart Service implemented using FastAPI.

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn

## Installation

1. Clone the repository.
2. Create a virtual environment: `python3 -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`

## Usage

Run the application using Uvicorn:

uvicorn app:app --reload

Access the service at `http://localhost:8000`.

## Endpoints

- `GET /carts/{userId}`: Retrieve a user's cart.
- `POST /carts/{userId}/items`: Add an item to the user's cart.
- `PUT /carts/{userId}/items/{item_id}`: Update quantity of item in cart.
- `DELETE /carts/{userId}/items/{item_id}`: Remove an item from the user's cart.


**Explanation:**

1.  **`app.py`**: This is the main application file. It initializes the FastAPI app and includes the router from `carts/routes.py`.

2.  **`carts/models.py`**: Defines the data models `CartItem` and `Cart` using Pydantic for data validation and serialization.

3.  **`carts/routes.py`**: Defines the API endpoints for the cart service using a FastAPI router.  It handles the routing and calls the appropriate functions from the `cart_service`.

4.  **`carts/services.py`**: Contains the business logic for the cart service, including adding, removing, updating items, and calculating the cart total. It also includes an in-memory storage using a dictionary.  **Important:** In a real-world application, you would replace this with a persistent database.

5.  **`requirements.txt`**: Lists the Python packages required to run the application.

6. **`README.md`**: Provides basic information on how to set up and run the service.

**To Run the Application:**

1.  Make sure you have Python 3.7 or higher installed.
2.  Create a virtual environment: `python3 -m venv venv`
3.  Activate the virtual environment.
4.  Install the dependencies: `pip install -r requirements.txt`
5.  Run the application: `uvicorn app:app --reload`

The `--reload` flag enables automatic reloading of the server when you make changes to the code.  You can then access the API endpoints in your browser or using a tool like `curl` or Postman.  For example, to test the root endpoint, go to `http://localhost:8000/` in your browser.

This provides a basic, functional scaffold. Remember to replace the in-memory storage with a proper database for production use.  Also, flesh out the placeholder functions with the actual logic for interacting with the `CatalogService` and handling the `org.springframework.samples.jpetstore.domain.Cart` and `org.springframework.samples.jpetstore.domain.CartItem` objects, as per your original service definition.
