#!/usr/bin/env python3
"""
Program 46: FastAPI Basics
Demonstrates FastAPI application structure, path operations, and responses.

Topics covered:
- Creating a FastAPI application
- Path operations (routes)
- Request and response handling
- Automatic API documentation
- Async/await support
- Response models and status codes
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class FastAPIBasicsDemo:
    """Demonstration of FastAPI basics and patterns."""

    def demonstrate_basic_app(self) -> None:
        """Demonstrate basic FastAPI application."""
        print("BASIC FASTAPI APPLICATION")
        print("=" * 60)

        code = """
from fastapi import FastAPI

# Create FastAPI application
app = FastAPI(
    title="My API",
    description="A simple FastAPI application",
    version="1.0.0"
)

# Define a path operation
@app.get("/")
def root():
    '''Root endpoint returning a welcome message.'''
    return {"message": "Hello, FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    '''Get item by ID.'''
    return {"item_id": item_id}

# Run with: uvicorn main:app --reload
# Automatic docs at: http://localhost:8000/docs (Swagger UI)
# Alternative docs: http://localhost:8000/redoc (ReDoc)
"""
        print(code)

    def demonstrate_path_operations(self) -> None:
        """Demonstrate different HTTP methods."""
        print("\nPATH OPERATIONS (HTTP METHODS)")
        print("=" * 60)

        code = """
from fastapi import FastAPI, status

app = FastAPI()

# GET - Retrieve data
@app.get("/items")
def list_items():
    return {"items": []}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id, "name": "Item"}

# POST - Create new resource
@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: dict):
    return {"id": 1, **item}

# PUT - Update/replace resource
@app.put("/items/{item_id}")
def update_item(item_id: int, item: dict):
    return {"item_id": item_id, **item}

# PATCH - Partial update
@app.patch("/items/{item_id}")
def partial_update_item(item_id: int, updates: dict):
    return {"item_id": item_id, "updates": updates}

# DELETE - Remove resource
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    return None

# HEAD - Get headers only
@app.head("/items/{item_id}")
def item_headers(item_id: int):
    return None

# OPTIONS - Get allowed methods
@app.options("/items")
def item_options():
    return None
"""
        print(code)

    def demonstrate_request_body(self) -> None:
        """Demonstrate request body with Pydantic models."""
        print("\nREQUEST BODY (Pydantic Models)")
        print("=" * 60)

        code = """
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# Define request model
class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    tax: Optional[float] = Field(None, ge=0)
    tags: list[str] = []

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice item",
                "price": 35.4,
                "tax": 3.2,
                "tags": ["electronics", "gadget"]
            }
        }

# Use model as request body
@app.post("/items")
def create_item(item: Item):
    # Automatic validation
    # Automatic JSON parsing
    # Automatic documentation
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict["price_with_tax"] = price_with_tax
    return item_dict

# Multiple body parameters
class User(BaseModel):
    username: str
    email: str

@app.post("/users/{user_id}/items")
def create_user_item(user_id: int, item: Item, user: User):
    return {"user_id": user_id, "item": item, "user": user}

# Singular values in body
from fastapi import Body

@app.post("/items/{item_id}")
def update_item(
    item_id: int,
    item: Item,
    importance: int = Body(...)  # Singular value in JSON body
):
    return {"item_id": item_id, "item": item, "importance": importance}
"""
        print(code)

    def demonstrate_response_models(self) -> None:
        """Demonstrate response models."""
        print("\nRESPONSE MODELS")
        print("=" * 60)

        code = """
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import Optional

app = FastAPI()

# Define models
class UserIn(BaseModel):
    '''User data for input (with password).'''
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserOut(BaseModel):
    '''User data for output (without password).'''
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserInDB(BaseModel):
    '''User data in database (with hashed password).'''
    username: str
    email: EmailStr
    hashed_password: str
    full_name: Optional[str] = None

# Use response_model to filter output
@app.post("/users", response_model=UserOut)
def create_user(user: UserIn):
    # Even if we return UserInDB, only UserOut fields are sent
    hashed_password = f"hashed_{user.password}"
    user_in_db = UserInDB(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    # Password won't be in response!
    return user_in_db

# Response model with list
@app.get("/users", response_model=list[UserOut])
def list_users():
    return [
        {"username": "alice", "email": "alice@example.com"},
        {"username": "bob", "email": "bob@example.com"}
    ]

# Exclude unset values
@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
def get_item(item_id: int):
    # Only include fields that were explicitly set
    return {"name": "Item", "price": 10.5}
    # description, tax, tags won't be in response

# Exclude specific fields
@app.get("/items/{item_id}", response_model=Item, response_model_exclude={"tax"})
def get_item_no_tax(item_id: int):
    return {"name": "Item", "price": 10.5, "tax": 2.0}
    # tax won't be in response

# Include only specific fields
@app.get("/items/{item_id}", response_model=Item, response_model_include={"name", "price"})
def get_item_minimal(item_id: int):
    return {"name": "Item", "description": "...", "price": 10.5}
    # Only name and price in response
"""
        print(code)

    def demonstrate_status_codes(self) -> None:
        """Demonstrate status codes and responses."""
        print("\nSTATUS CODES AND RESPONSES")
        print("=" * 60)

        code = """
from fastapi import FastAPI, status, Response
from fastapi.responses import JSONResponse

app = FastAPI()

# Static status code
@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: dict):
    return item

# Status code constants
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    return None

# Dynamic status code
@app.get("/items/{item_id}")
def get_item(item_id: int, response: Response):
    if item_id == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Item not found"}
    return {"item_id": item_id}

# Return JSONResponse directly
@app.post("/login")
def login(username: str, password: str):
    if username == "user" and password == "pass":
        return JSONResponse(
            content={"message": "Login successful"},
            status_code=status.HTTP_200_OK,
            headers={"X-Token": "fake-token"}
        )
    return JSONResponse(
        content={"error": "Invalid credentials"},
        status_code=status.HTTP_401_UNAUTHORIZED
    )

# Custom response class
from fastapi.responses import PlainTextResponse

@app.get("/text", response_class=PlainTextResponse)
def get_text():
    return "Plain text response"

# HTML response
from fastapi.responses import HTMLResponse

@app.get("/html", response_class=HTMLResponse)
def get_html():
    return "<html><body><h1>Hello</h1></body></html>"

# Redirect response
from fastapi.responses import RedirectResponse

@app.get("/redirect")
def redirect():
    return RedirectResponse(url="/items")

# File response
from fastapi.responses import FileResponse

@app.get("/download/{filename}")
def download_file(filename: str):
    return FileResponse(
        path=f"/files/{filename}",
        filename=filename,
        media_type="application/octet-stream"
    )

# Streaming response
from fastapi.responses import StreamingResponse
import io

@app.get("/stream")
def stream_data():
    def generate():
        for i in range(10):
            yield f"Line {i}\n"

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )
"""
        print(code)

    def demonstrate_async_operations(self) -> None:
        """Demonstrate async/await support."""
        print("\nASYNC/AWAIT SUPPORT")
        print("=" * 60)

        code = """
from fastapi import FastAPI
import asyncio

app = FastAPI()

# Sync function (runs in thread pool)
@app.get("/sync")
def sync_operation():
    # Blocking I/O operations
    return {"message": "Sync operation"}

# Async function (runs in event loop)
@app.get("/async")
async def async_operation():
    # Non-blocking I/O with await
    await asyncio.sleep(1)  # Simulated async operation
    return {"message": "Async operation"}

# Async with database
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # Await database query
    # user = await db.fetch_one("SELECT * FROM users WHERE id = $1", user_id)
    await asyncio.sleep(0.1)  # Simulated DB query
    return {"user_id": user_id}

# Parallel async operations
@app.get("/dashboard")
async def get_dashboard():
    # Run multiple queries in parallel
    user_task = asyncio.create_task(fetch_user())
    posts_task = asyncio.create_task(fetch_posts())
    stats_task = asyncio.create_task(fetch_stats())

    user = await user_task
    posts = await posts_task
    stats = await stats_task

    return {"user": user, "posts": posts, "stats": stats}

async def fetch_user():
    await asyncio.sleep(0.1)
    return {"name": "John"}

async def fetch_posts():
    await asyncio.sleep(0.1)
    return []

async def fetch_stats():
    await asyncio.sleep(0.1)
    return {"views": 100}

# Use sync vs async appropriately:
# - Use async for I/O-bound operations (DB, HTTP, files)
# - Use sync for CPU-bound operations or simple logic
# - Don't use async if you don't await anything
"""
        print(code)

    def demonstrate_dependencies(self) -> None:
        """Demonstrate dependency injection."""
        print("\nDEPENDENCY INJECTION")
        print("=" * 60)

        code = """
from fastapi import FastAPI, Depends, HTTPException
from typing import Optional

app = FastAPI()

# Simple dependency
def get_query_param(q: Optional[str] = None):
    return q

@app.get("/items")
def read_items(query: Optional[str] = Depends(get_query_param)):
    return {"query": query}

# Dependency with multiple parameters
def pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/users")
def list_users(page: dict = Depends(pagination)):
    return {"skip": page["skip"], "limit": page["limit"]}

# Class-based dependency
class Database:
    def __init__(self):
        self.connection = "db_connection"

    def get_users(self):
        return []

def get_db():
    db = Database()
    try:
        yield db
    finally:
        # Cleanup
        pass

@app.get("/users")
def get_users(db: Database = Depends(get_db)):
    users = db.get_users()
    return {"users": users}

# Nested dependencies
def verify_token(token: str):
    if token != "valid":
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

def get_current_user(token: str = Depends(verify_token)):
    return {"username": "john", "token": token}

@app.get("/me")
def read_current_user(user: dict = Depends(get_current_user)):
    return user

# Dependencies in path operation decorator
@app.get("/admin", dependencies=[Depends(verify_token)])
def admin_panel():
    # verify_token is called but result not used
    return {"message": "Admin panel"}
"""
        print(code)

    def demonstrate_documentation(self) -> None:
        """Demonstrate automatic documentation."""
        print("\nAUTOMATIC API DOCUMENTATION")
        print("=" * 60)

        code = """
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="My API",
    description="## A comprehensive API\\n\\nThis API does many things!",
    version="2.0.0",
    terms_of_service="https://example.com/terms",
    contact={
        "name": "API Support",
        "url": "https://example.com/contact",
        "email": "support@example.com"
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    }
)

class Item(BaseModel):
    name: str = Field(..., description="The name of the item")
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    description: Optional[str] = Field(None, max_length=300)

@app.post(
    "/items",
    summary="Create an item",
    description="Create a new item with all the information",
    response_description="The created item",
    tags=["items"]
)
def create_item(item: Item):
    '''
    Create an item with all the information:

    - **name**: each item must have a name
    - **price**: required price
    - **description**: optional description
    '''
    return item

# Grouping with tags
@app.get("/users", tags=["users"])
def get_users():
    return []

@app.post("/users", tags=["users"])
def create_user():
    return {}

@app.get("/items", tags=["items"])
def get_items():
    return []

# Deprecating endpoints
@app.get("/old-endpoint", deprecated=True)
def old_endpoint():
    return {"message": "This endpoint is deprecated"}

# Access docs at:
# http://localhost:8000/docs (Swagger UI)
# http://localhost:8000/redoc (ReDoc)
# http://localhost:8000/openapi.json (OpenAPI schema)
"""
        print(code)


def main() -> None:
    """Main entry point demonstrating FastAPI basics."""
    print("\n" + "=" * 60)
    print("PROGRAM 46: FASTAPI BASICS")
    print("=" * 60 + "\n")

    demo = FastAPIBasicsDemo()

    demo.demonstrate_basic_app()
    demo.demonstrate_path_operations()
    demo.demonstrate_request_body()
    demo.demonstrate_response_models()
    demo.demonstrate_status_codes()
    demo.demonstrate_async_operations()
    demo.demonstrate_dependencies()
    demo.demonstrate_documentation()

    print("\n" + "=" * 60)
    print("FASTAPI BEST PRACTICES")
    print("=" * 60)
    print("1. Use Pydantic models for validation")
    print("2. Use response_model to filter sensitive data")
    print("3. Use async/await for I/O-bound operations")
    print("4. Use dependency injection for reusable logic")
    print("5. Add proper documentation and examples")
    print("6. Use appropriate status codes")
    print("7. Handle errors with HTTPException")
    print("8. Use tags to organize endpoints")
    print("9. Validate with Pydantic Field constraints")
    print("10. Type hint everything for automatic docs")
    print("=" * 60)


if __name__ == "__main__":
    main()
