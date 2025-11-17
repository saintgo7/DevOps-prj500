#!/usr/bin/env python3
"""
Program 47: FastAPI Routing
Demonstrates advanced routing in FastAPI including path parameters,
query parameters, and request body handling.

Topics covered:
- Path parameters with type validation
- Query parameters with defaults
- Request body with Pydantic models
- Multiple parameters combinations
- Parameter validation
- APIRouter for organization
"""

from typing import Dict, Any, List, Optional
from enum import Enum


class FastAPIRoutingDemo:
    """Demonstration of FastAPI routing patterns."""

    def demonstrate_path_parameters(self) -> None:
        """Demonstrate path parameters with validation."""
        print("PATH PARAMETERS")
        print("=" * 60)

        code = """
from fastapi import FastAPI, Path
from typing import Optional

app = FastAPI()

# Basic path parameter
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

# Path parameter with validation
@app.get("/items/{item_id}")
def read_item(
    item_id: int = Path(..., title="The ID of the item", ge=1, le=1000)
):
    '''
    Path parameter with constraints:
    - ge: greater than or equal to 1
    - le: less than or equal to 1000
    '''
    return {"item_id": item_id}

# String path parameter
@app.get("/users/{username}")
def get_user(
    username: str = Path(..., min_length=3, max_length=20, regex="^[a-zA-Z0-9_]+$")
):
    return {"username": username}

# Path parameter with Enum
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
def get_model(model_name: ModelName):
    # Auto-validation against enum values
    # Auto-documentation with allowed values
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "AlexNet model"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN model"}
    return {"model_name": model_name, "message": "ResNet model"}

# Path-like parameters
@app.get("/files/{file_path:path}")
def read_file(file_path: str):
    # Matches paths like: /files/home/user/docs/file.txt
    return {"file_path": file_path}

# Multiple path parameters
@app.get("/users/{user_id}/posts/{post_id}")
def get_user_post(
    user_id: int = Path(..., ge=1),
    post_id: int = Path(..., ge=1)
):
    return {"user_id": user_id, "post_id": post_id}

# UUID path parameter
from uuid import UUID

@app.get("/objects/{object_id}")
def get_object(object_id: UUID):
    return {"object_id": str(object_id)}
"""
        print(code)

    def demonstrate_query_parameters(self) -> None:
        """Demonstrate query parameters."""
        print("\nQUERY PARAMETERS")
        print("=" * 60)

        code = """
from fastapi import FastAPI, Query
from typing import Optional

app = FastAPI()

# Basic query parameter
@app.get("/items")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

# Optional query parameter
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    result = {"item_id": item_id}
    if q:
        result["q"] = q
    return result

# Query parameter with validation
@app.get("/items")
def read_items(
    q: Optional[str] = Query(
        None,
        title="Query string",
        description="Search query string",
        min_length=3,
        max_length=50,
        regex="^[a-zA-Z0-9 ]+$"
    ),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return {"q": q, "skip": skip, "limit": limit}

# Required query parameter
@app.get("/items")
def read_items(q: str = Query(..., min_length=3)):
    # ... means required
    return {"q": q}

# Query parameter with default
@app.get("/items")
def read_items(
    q: str = Query("default", min_length=3),
    hidden: bool = Query(False)
):
    return {"q": q, "hidden": hidden}

# Multiple values for same parameter
@app.get("/items")
def read_items(q: Optional[list[str]] = Query(None)):
    # URL: /items?q=foo&q=bar&q=baz
    return {"q": q}

# With default list
@app.get("/items")
def read_items(q: list[str] = Query(["default1", "default2"])):
    return {"q": q}

# Alias for query parameter
@app.get("/items")
def read_items(
    item_id: Optional[str] = Query(None, alias="item-id")
):
    # Can use item-id in URL but item_id in Python
    # URL: /items?item-id=foo
    return {"item_id": item_id}

# Deprecated parameter
@app.get("/items")
def read_items(
    q: Optional[str] = Query(None, deprecated=True)
):
    return {"q": q}

# Hidden from documentation
@app.get("/items")
def read_items(
    hidden_param: Optional[str] = Query(None, include_in_schema=False)
):
    return {"hidden": hidden_param}

# Boolean query parameters
@app.get("/items")
def read_items(
    is_active: bool = Query(True),
    include_deleted: bool = Query(False)
):
    # URL: /items?is_active=true&include_deleted=false
    # Also accepts: yes/no, on/off, 1/0
    return {"is_active": is_active, "include_deleted": include_deleted}

# Combining path and query parameters
@app.get("/users/{user_id}/items")
def read_user_items(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    q: Optional[str] = None
):
    return {"user_id": user_id, "skip": skip, "limit": limit, "q": q}
"""
        print(code)

    def demonstrate_request_body(self) -> None:
        """Demonstrate request body parameters."""
        print("\nREQUEST BODY")
        print("=" * 60)

        code = """
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# Pydantic model for request body
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0, description="Price must be positive")
    tax: Optional[float] = Field(None, ge=0)

@app.post("/items")
def create_item(item: Item):
    return item

# Multiple body parameters
class User(BaseModel):
    username: str
    email: str

@app.post("/items")
def create_item(item: Item, user: User):
    return {"item": item, "user": user}

# Mix body with path and query
@app.put("/items/{item_id}")
def update_item(
    item_id: int,
    item: Item,
    q: Optional[str] = None
):
    result = {"item_id": item_id, "item": item}
    if q:
        result["q"] = q
    return result

# Single value in body
@app.post("/items/{item_id}")
def update_item(
    item_id: int,
    item: Item,
    importance: int = Body(..., ge=1, le=5)
):
    # Body will be: {"item": {...}, "importance": 3}
    return {"item_id": item_id, "item": item, "importance": importance}

# Embed single model
@app.post("/items")
def create_item(item: Item = Body(..., embed=True)):
    # Body will be: {"item": {...}}
    # Without embed, body would be just: {...}
    return item

# Multiple body params with extra data
@app.post("/offers")
def create_offer(
    item: Item,
    user: User,
    discount: float = Body(..., gt=0, lt=100)
):
    return {"item": item, "user": user, "discount": discount}

# Nested models
class Image(BaseModel):
    url: str
    name: str

class ExtendedItem(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    images: list[Image] = []

@app.post("/items")
def create_item(item: ExtendedItem):
    return item

# List of models
@app.post("/items/bulk")
def create_items(items: list[Item]):
    return {"items_count": len(items), "items": items}

# Dict request body
@app.post("/items/dict")
def create_items(items: dict[str, float]):
    # Body: {"item1": 10.5, "item2": 20.0}
    return items
"""
        print(code)

    def demonstrate_field_validation(self) -> None:
        """Demonstrate Pydantic field validation."""
        print("\nFIELD VALIDATION")
        print("=" * 60)

        code = """
from pydantic import BaseModel, Field, validator, root_validator
from typing import Optional
from datetime import datetime

class Item(BaseModel):
    # String constraints
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

    # Numeric constraints
    price: float = Field(..., gt=0, description="Must be positive")
    quantity: int = Field(..., ge=0, le=10000)
    discount: Optional[float] = Field(None, ge=0, le=100)

    # Regex validation
    sku: str = Field(..., regex="^[A-Z]{3}-[0-9]{4}$")

    # List constraints
    tags: list[str] = Field(default=[], max_items=10)
    images: list[str] = Field(default=[], min_items=1, max_items=5)

    # Custom example for docs
    class Config:
        schema_extra = {
            "example": {
                "name": "Awesome Product",
                "description": "A great product",
                "price": 99.99,
                "quantity": 100,
                "sku": "ABC-1234",
                "tags": ["electronics", "gadget"]
            }
        }

    # Custom validator
    @validator('name')
    def name_must_not_contain_spam(cls, v):
        if 'spam' in v.lower():
            raise ValueError('Name cannot contain spam')
        return v.title()  # Capitalize

    @validator('discount')
    def discount_check(cls, v, values):
        # Access other fields
        if v and 'price' in values and v > values['price']:
            raise ValueError('Discount cannot exceed price')
        return v

    # Validate all string fields
    @validator('*', pre=True)
    def empty_str_to_none(cls, v):
        if v == '':
            return None
        return v

    # Root validator (validate entire model)
    @root_validator
    def check_total(cls, values):
        price = values.get('price', 0)
        discount = values.get('discount', 0)
        if discount and discount > price * 0.5:
            raise ValueError('Discount cannot exceed 50% of price')
        return values

# Use in FastAPI
from fastapi import FastAPI

app = FastAPI()

@app.post("/items")
def create_item(item: Item):
    return item
"""
        print(code)

    def demonstrate_form_data(self) -> None:
        """Demonstrate form data handling."""
        print("\nFORM DATA")
        print("=" * 60)

        code = """
from fastapi import FastAPI, Form, File, UploadFile
from typing import Optional

app = FastAPI()

# Form fields
@app.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...)
):
    return {"username": username}

# Form with validation
@app.post("/signup")
def signup(
    username: str = Form(..., min_length=3, max_length=20),
    password: str = Form(..., min_length=8),
    email: str = Form(...),
    age: Optional[int] = Form(None, ge=18)
):
    return {"username": username, "email": email}

# File upload
@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": file.size
    }

# Multiple file upload
@app.post("/upload-multiple")
async def upload_files(files: list[UploadFile] = File(...)):
    return [
        {"filename": file.filename, "size": file.size}
        for file in files
    ]

# Form with file
@app.post("/upload-with-metadata")
async def upload_with_metadata(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: Optional[str] = Form(None)
):
    # Read file content
    content = await file.read()
    return {
        "filename": file.filename,
        "title": title,
        "description": description,
        "size": len(content)
    }

# Optional file
@app.post("/upload-optional")
def upload_optional(
    file: Optional[UploadFile] = File(None)
):
    if file:
        return {"filename": file.filename}
    return {"message": "No file uploaded"}

# Bytes file (small files)
@app.post("/upload-bytes")
def upload_bytes(file: bytes = File(...)):
    return {"file_size": len(file)}
"""
        print(code)

    def demonstrate_api_router(self) -> None:
        """Demonstrate APIRouter for organization."""
        print("\nAPI ROUTER (Organization)")
        print("=" * 60)

        print("\n1. Creating Routers:")
        print("-" * 60)
        code = """
# File: routers/users.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

class User(BaseModel):
    name: str
    email: str

@router.get("/")
def get_users():
    return {"users": []}

@router.get("/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

@router.post("/")
def create_user(user: User):
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int):
    return {"deleted": user_id}

# File: routers/items.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

@router.get("/")
def get_items(skip: int = 0, limit: int = 10):
    return {"items": []}

@router.get("/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}
"""
        print(code)

        print("2. Including Routers in Main App:")
        print("-" * 60)
        code = """
# File: main.py
from fastapi import FastAPI
from routers import users, items

app = FastAPI()

# Include routers
app.include_router(users.router)
app.include_router(items.router)

# With custom prefix
app.include_router(
    users.router,
    prefix="/api/v1",
    tags=["v1"]
)

# URLs will be:
# /api/v1/users/
# /api/v1/users/{user_id}
# /api/v1/items/
# /api/v1/items/{item_id}
"""
        print(code)

        print("3. Nested Routers:")
        print("-" * 60)
        code = """
from fastapi import APIRouter

# Main API router
api_router = APIRouter()

# Version 1 router
v1_router = APIRouter()

# Users router
users_router = APIRouter(prefix="/users", tags=["users"])

@users_router.get("/")
def get_users():
    return []

# Include users in v1
v1_router.include_router(users_router)

# Include v1 in api
api_router.include_router(v1_router, prefix="/v1")

# Include in main app
from fastapi import FastAPI
app = FastAPI()
app.include_router(api_router, prefix="/api")

# URL: /api/v1/users/
"""
        print(code)

    def demonstrate_dependencies_in_routing(self) -> None:
        """Demonstrate dependencies in routing."""
        print("\nDEPENDENCIES IN ROUTING")
        print("=" * 60)

        code = """
from fastapi import APIRouter, Depends, HTTPException

# Common dependency
def verify_token(token: str):
    if token != "secret":
        raise HTTPException(status_code=401)
    return token

def verify_admin(token: str = Depends(verify_token)):
    if token != "admin-secret":
        raise HTTPException(status_code=403)
    return True

# Router with dependency
router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(verify_admin)]  # Applied to all routes
)

@router.get("/users")
def admin_get_users():
    # verify_admin runs automatically
    return {"users": []}

@router.delete("/users/{user_id}")
def admin_delete_user(user_id: int):
    # verify_admin runs automatically
    return {"deleted": user_id}

# Override dependency for specific route
@router.get("/public")
def public_route():
    # No admin check for this route
    return {"message": "Public"}
"""
        print(code)


def main() -> None:
    """Main entry point demonstrating FastAPI routing."""
    print("\n" + "=" * 60)
    print("PROGRAM 47: FASTAPI ROUTING")
    print("=" * 60 + "\n")

    demo = FastAPIRoutingDemo()

    demo.demonstrate_path_parameters()
    demo.demonstrate_query_parameters()
    demo.demonstrate_request_body()
    demo.demonstrate_field_validation()
    demo.demonstrate_form_data()
    demo.demonstrate_api_router()
    demo.demonstrate_dependencies_in_routing()

    print("\n" + "=" * 60)
    print("ROUTING BEST PRACTICES")
    print("=" * 60)
    print("1. Use path parameters for resource identification")
    print("2. Use query parameters for filtering/pagination")
    print("3. Use request body for complex data")
    print("4. Validate all inputs with Pydantic")
    print("5. Organize routes with APIRouter")
    print("6. Use consistent naming conventions")
    print("7. Add proper validation constraints")
    print("8. Document parameters with descriptions")
    print("9. Use Enums for fixed choices")
    print("10. Group related routes with tags")
    print("=" * 60)


if __name__ == "__main__":
    main()
