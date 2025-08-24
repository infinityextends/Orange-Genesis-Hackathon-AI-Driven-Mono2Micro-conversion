document.addEventListener('DOMContentLoaded', function() {
    const API_BASE_URL = "http://localhost:8000";
    const responseArea = document.getElementById('response-area');

    function displayResponse(data) {
        responseArea.textContent = JSON.stringify(data, null, 2);
    }

    function handleApiCall(apiEndpoint, method = 'GET', body = null) {
        fetch(`${API_BASE_URL}${apiEndpoint}`, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: body ? JSON.stringify(body) : null
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => displayResponse(data))
        .catch(error => displayResponse({ error: error.message }));
    }

    // Example API calls
    document.getElementById('getCategories').addEventListener('click', () => handleApiCall('/categories'));
    document.getElementById('getProduct').addEventListener('click', () => handleApiCall('/products/1'));
    document.getElementById('getItem').addEventListener('click', () => handleApiCall('/items/1'));
    document.getElementById('getProductItems').addEventListener('click', () => handleApiCall('/products/1/items'));
});

**Explanation and How to Run:**

1.  **File Structure:**
    .
    ├── app.py
    ├── models.py
    ├── database.py
    ├── requirements.txt
    └── ui
        ├── index.html
        └── static
            ├── script.js
            └── style.css

2.  **`app.py` (Main Application):**
    *   Imports necessary modules from FastAPI and SQLAlchemy.
    *   Defines the API endpoints (`/categories`, `/categories/{categoryId}`, `/products/{productId}`, `/items/{itemId}`, `/products/{productId}/items`).
    *   Uses placeholder functions (`check_inventory`, `update_inventory`) to represent the core logic. *These need to be implemented with actual database interactions.*
    *   Includes error handling (e.g., `HTTPException` for "not found").
    *   Sets up CORS to allow requests from any origin (for development purposes). **Important:**  In production, restrict `allow_origins` to your actual frontend domain.

3.  **`models.py` (SQLAlchemy Models):**
    *   Defines the database models (`Category`, `Product`, `Item`) using SQLAlchemy.
    *   Includes relationships between the models (e.g., a `Category` can have multiple `Product`s).
    *   Uses `declarative_base` for defining the models.

4.  **`database.py` (Database Configuration):**
    *   Configures the SQLAlchemy engine and session.
    *   Uses SQLite for simplicity.  **Change `SQLALCHEMY_DATABASE_URL` to your desired database.**  If using PostgreSQL, you'll need to install `psycopg2-binary` as well.
    *   Provides a dependency injection function (`get_db`) to create and close database sessions for each request.

5.  **`requirements.txt`:**
    *   Lists the Python packages required for the project.  Includes `fastapi`, `uvicorn`, `SQLAlchemy`, `python-dotenv`, `requests`, `Jinja2`, and `python-multipart`.

6.  **`ui/index.html`:**
    *   A very basic HTML file with buttons that trigger JavaScript functions to call the API endpoints.
    *   Displays the JSON response in a `<div id="response">`.

7.  **`ui/static/style.css` and `ui/static/script.js`:**
    *   Basic styling and JavaScript for the UI to make it a little more presentable and functional.

**To Run the Application:**

1.  **Install Dependencies:**

    pip install -r requirements.txt

2.  **Run the FastAPI Application:**

    uvicorn app:app --reload

    This will start the server, and you can access the API endpoints (e.g., `http://localhost:8000/categories`).

3.  **Serve the UI:**

    You can't directly serve the `ui/index.html` file with `uvicorn`.  You have a few options:

    *   **Simple Python HTTP Server (for testing):**  Navigate to the `ui` directory in your terminal and run:

        python -m http.server 8001

        Then open `http://localhost:8001/index.html` in your browser.  *This is only for simple testing; it's not suitable for production.*

    *   **FastAPI Static Files:**  (More integrated approach) You can modify `app.py` to serve the static files:

        from fastapi.staticfiles import StaticFiles

        app.mount("/static", StaticFiles(directory="ui/static"), name="static")

        @app.get("/")
        async def read_root():
            return HTMLResponse(open("ui/index.html").read())

        Add `from fastapi.responses import HTMLResponse` at the top of `app.py`.  Now, you can access the UI at `http://localhost:8000/`.  **Important:** This serves `index.html` at the root `/`.  You might want to adjust the route if you want your API documentation at `/`.

4.  **Testing:**

    *   Open your browser and go to the UI (`http://localhost:8001/index.html` or `http://localhost:8000/` depending on how you served it).
    *   Click the buttons to call the API endpoints.  The responses will be displayed in the `response` div.

**Key Improvements and Considerations:**

*   **Database Interactions:**  The placeholder functions (`check_inventory`, `update_inventory`) *must* be implemented with actual database queries using SQLAlchemy.  You'll need to create DAOs (Data Access Objects) as described in your original service definition if you want a more structured approach.  The provided code directly uses the SQLAlchemy session for simplicity.
*   **Error Handling:** The code includes basic error handling (e.g., `HTTPException` for "not found").  You should add more robust error handling and logging.
*   **Data Validation:**  Consider using Pydantic models (integrated with FastAPI) for data validation to ensure that the data being passed to your API endpoints is valid.
*   **Security:**  For production, implement proper authentication and authorization.
*   **Asynchronous Operations:** FastAPI is built on `asyncio`.  If your database interactions or other operations are potentially long-running, consider using asynchronous versions of the SQLAlchemy drivers (e.g., `asyncpg` for PostgreSQL) to avoid blocking the event loop.
*   **Testing:**  Write unit tests to ensure that your API endpoints and business logic are working correctly.  Use `pytest` or similar testing frameworks.
*   **Configuration:** Use environment variables (e.g., with `python-dotenv`) to configure settings like the database URL.  This makes your application more portable.
*   **Dependency Injection:** FastAPI's dependency injection system is used for the database session.  Use it for other dependencies as well to improve testability and maintainability.
*   **Documentation:** FastAPI automatically generates API documentation using OpenAPI (Swagger UI) and ReDoc.  Access it at `/docs` and `/redoc` after starting the server.

This detailed response provides a solid foundation for building your `CatalogService` with FastAPI. Remember to fill in the placeholder functions with your actual business logic and database interactions.
