#!/usr/bin/env python3
"""
Program 60: API Documentation
Demonstrates API documentation with OpenAPI, Swagger, and docstrings.

Topics covered:
- OpenAPI specification
- Swagger UI customization
- ReDoc documentation
- Docstring documentation
- Examples and schemas
- Response documentation
- Tags and grouping
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class APIDocumentationDemo:
    """Demonstration of API documentation patterns."""

    def demonstrate_openapi_basics(self) -> None:
        """Demonstrate OpenAPI basics."""
        print("OPENAPI BASICS")
        print("=" * 60)

        code = """
from fastapi import FastAPI
from pydantic import BaseModel, Field

# Configure FastAPI with metadata
app = FastAPI(
    title="My API",
    description="## A comprehensive API\\n\\n"
                "This API provides CRUD operations for users and posts.\\n\\n"
                "### Features\\n"
                "- User management\\n"
                "- Post creation and management\\n"
                "- Authentication with JWT\\n",
    version="2.0.0",
    terms_of_service="https://example.com/terms",
    contact={
        "name": "API Support",
        "url": "https://example.com/contact",
        "email": "support@example.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    openapi_tags=[
        {
            "name": "users",
            "description": "Operations with users",
        },
        {
            "name": "posts",
            "description": "Manage blog posts",
        },
        {
            "name": "auth",
            "description": "Authentication endpoints",
        }
    ]
)

# Access documentation at:
# - Swagger UI: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
# - OpenAPI Schema: http://localhost:8000/openapi.json
"""
        print(code)

    def demonstrate_schema_documentation(self) -> None:
        """Demonstrate documenting schemas with examples."""
        print("\nSCHEMA DOCUMENTATION")
        print("=" * 60)

        code = """
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# Documented models with examples
class UserBase(BaseModel):
    '''Base user model.'''
    username: str = Field(
        ...,
        title="Username",
        description="Unique username for the user",
        min_length=3,
        max_length=50,
        example="johndoe"
    )
    email: EmailStr = Field(
        ...,
        title="Email",
        description="User's email address",
        example="john@example.com"
    )
    full_name: Optional[str] = Field(
        None,
        title="Full Name",
        description="User's full name",
        max_length=100,
        example="John Doe"
    )

class UserCreate(UserBase):
    '''Schema for creating a user.'''
    password: str = Field(
        ...,
        title="Password",
        description="User's password (min 8 characters)",
        min_length=8,
        example="secretpassword123"
    )

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "password": "secretpassword123"
            }
        }

class UserResponse(UserBase):
    '''Schema for user response.'''
    id: int = Field(..., description="Unique user ID", example=1)
    is_active: bool = Field(..., description="Whether user is active", example=True)
    created_at: datetime = Field(..., description="User creation timestamp")

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "username": "johndoe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "is_active": True,
                "created_at": "2025-11-17T12:00:00"
            }
        }

# Multiple examples
class PostCreate(BaseModel):
    '''Schema for creating a post.'''
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    published: bool = Field(False)

    class Config:
        schema_extra = {
            "examples": {
                "normal": {
                    "summary": "A normal post",
                    "description": "A typical blog post",
                    "value": {
                        "title": "My Blog Post",
                        "content": "This is the content of my blog post.",
                        "published": False
                    }
                },
                "published": {
                    "summary": "A published post",
                    "description": "A post ready for publication",
                    "value": {
                        "title": "Published Article",
                        "content": "This article is ready to be published.",
                        "published": True
                    }
                }
            }
        }
"""
        print(code)

    def demonstrate_endpoint_documentation(self) -> None:
        """Demonstrate documenting endpoints."""
        print("\nENDPOINT DOCUMENTATION")
        print("=" * 60)

        code = """
from fastapi import FastAPI, Path, Query, Body, status
from typing import List

app = FastAPI()

# Basic documentation
@app.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["users"],
    summary="Create a new user",
    description="Create a new user with the provided information",
    response_description="The created user"
)
def create_user(user: UserCreate):
    '''
    Create a new user with all the information:

    - **username**: unique username (3-50 characters)
    - **email**: valid email address
    - **full_name**: optional full name
    - **password**: password (min 8 characters)

    Returns the created user object.
    '''
    # Implementation
    pass

# Detailed documentation with examples
@app.get(
    "/users/{user_id}",
    response_model=UserResponse,
    tags=["users"],
    summary="Get user by ID",
    responses={
        200: {
            "description": "Successful response",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "username": "johndoe",
                        "email": "john@example.com",
                        "is_active": True
                    }
                }
            }
        },
        404: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User not found"
                    }
                }
            }
        }
    }
)
def get_user(
    user_id: int = Path(..., description="The ID of the user to get", ge=1, example=1)
):
    '''
    Get a user by ID.

    Returns detailed user information if found.
    '''
    pass

# Query parameters documentation
@app.get(
    "/users",
    response_model=List[UserResponse],
    tags=["users"],
    summary="List users"
)
def list_users(
    skip: int = Query(
        0,
        description="Number of users to skip",
        ge=0,
        example=0
    ),
    limit: int = Query(
        10,
        description="Maximum number of users to return",
        ge=1,
        le=100,
        example=10
    ),
    is_active: Optional[bool] = Query(
        None,
        description="Filter by active status",
        example=True
    ),
    search: Optional[str] = Query(
        None,
        description="Search in username and email",
        min_length=3,
        example="john"
    )
):
    '''
    List users with optional filters and pagination.

    - **skip**: Number of users to skip (for pagination)
    - **limit**: Maximum number of users to return
    - **is_active**: Filter by active status
    - **search**: Search query
    '''
    pass

# Request body documentation
@app.put(
    "/users/{user_id}",
    response_model=UserResponse,
    tags=["users"]
)
def update_user(
    user_id: int = Path(..., description="User ID", ge=1),
    user: UserUpdate = Body(
        ...,
        examples={
            "normal": {
                "summary": "Normal update",
                "value": {
                    "full_name": "John Updated Doe",
                    "email": "newemails@example.com"
                }
            },
            "minimal": {
                "summary": "Minimal update",
                "value": {
                    "full_name": "New Name"
                }
            }
        }
    )
):
    '''Update user information.'''
    pass

# Deprecated endpoint
@app.get(
    "/users/old-endpoint",
    tags=["users"],
    deprecated=True,
    summary="Old endpoint (deprecated)"
)
def old_endpoint():
    '''
    This endpoint is deprecated.

    Please use `/users` instead.
    '''
    pass
"""
        print(code)

    def demonstrate_response_models(self) -> None:
        """Demonstrate response model documentation."""
        print("\nRESPONSE MODEL DOCUMENTATION")
        print("=" * 60)

        code = """
from typing import List, Union
from pydantic import BaseModel

# Error response model
class ErrorResponse(BaseModel):
    '''Standard error response.'''
    detail: str = Field(..., description="Error message")
    status_code: int = Field(..., description="HTTP status code")

    class Config:
        schema_extra = {
            "example": {
                "detail": "User not found",
                "status_code": 404
            }
        }

# Success response model
class SuccessResponse(BaseModel):
    '''Standard success response.'''
    message: str = Field(..., description="Success message")
    data: Optional[dict] = Field(None, description="Response data")

# Pagination response model
class PaginatedResponse(BaseModel):
    '''Paginated response.'''
    items: List[UserResponse] = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items", ge=0)
    page: int = Field(..., description="Current page number", ge=1)
    page_size: int = Field(..., description="Items per page", ge=1)
    total_pages: int = Field(..., description="Total number of pages", ge=0)

    class Config:
        schema_extra = {
            "example": {
                "items": [
                    {"id": 1, "username": "user1", "email": "user1@example.com"},
                    {"id": 2, "username": "user2", "email": "user2@example.com"}
                ],
                "total": 100,
                "page": 1,
                "page_size": 10,
                "total_pages": 10
            }
        }

# Multiple response types
@app.get(
    "/users/{user_id}",
    response_model=UserResponse,
    responses={
        200: {"model": UserResponse, "description": "Successful response"},
        404: {"model": ErrorResponse, "description": "User not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
def get_user(user_id: int):
    pass

# Union response types
class AdminResponse(UserResponse):
    '''Admin user response with extra fields.'''
    permissions: List[str] = Field(..., description="User permissions")

@app.get(
    "/users/{user_id}/detailed",
    response_model=Union[UserResponse, AdminResponse],
    tags=["users"]
)
def get_user_detailed(user_id: int, include_admin: bool = False):
    '''
    Get detailed user information.

    Returns AdminResponse if user is admin and include_admin=True.
    '''
    pass
"""
        print(code)

    def demonstrate_custom_docs(self) -> None:
        """Demonstrate customizing documentation."""
        print("\nCUSTOM DOCUMENTATION")
        print("=" * 60)

        code = """
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

app = FastAPI(docs_url=None, redoc_url=None)  # Disable default docs

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="My Custom API",
        version="2.0.0",
        description="Custom API description",
        routes=app.routes,
    )

    # Add custom fields
    openapi_schema["info"]["x-logo"] = {
        "url": "https://example.com/logo.png"
    }

    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Custom Swagger UI
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="My API - Swagger UI",
        oauth2_redirect_url="/docs/oauth2-redirect",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui.css",
        swagger_favicon_url="https://example.com/favicon.ico"
    )

# Custom ReDoc
@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="My API - ReDoc",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
        redoc_favicon_url="https://example.com/favicon.ico"
    )

# Custom CSS for Swagger
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Custom Swagger UI",
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,  # Hide models by default
            "docExpansion": "none",  # Collapse all endpoints by default
            "filter": True,  # Enable search filter
            "persistAuthorization": True,  # Remember auth between refreshes
        }
    )
"""
        print(code)

    def demonstrate_advanced_documentation(self) -> None:
        """Demonstrate advanced documentation features."""
        print("\nADVANCED DOCUMENTATION")
        print("=" * 60)

        code = """
from fastapi import FastAPI, File, UploadFile
from typing import List

app = FastAPI()

# File upload documentation
@app.post(
    "/upload",
    tags=["files"],
    summary="Upload a file",
    description="Upload a single file to the server"
)
async def upload_file(
    file: UploadFile = File(..., description="The file to upload")
):
    '''
    Upload a file.

    Accepts various file types:
    - Images: jpg, png, gif
    - Documents: pdf, docx, txt
    - Max size: 10MB
    '''
    return {"filename": file.filename}

# Multiple file upload
@app.post("/upload-multiple", tags=["files"])
async def upload_multiple_files(
    files: List[UploadFile] = File(..., description="Multiple files")
):
    '''Upload multiple files at once.'''
    return {"filenames": [f.filename for f in files]}

# Webhook documentation
@app.post(
    "/webhooks/github",
    tags=["webhooks"],
    summary="GitHub webhook",
    description="Endpoint for GitHub webhook notifications"
)
async def github_webhook(payload: dict):
    '''
    GitHub webhook endpoint.

    Handles the following events:
    - push
    - pull_request
    - issues

    See: https://docs.github.com/en/webhooks
    '''
    pass

# Custom tags with descriptions
tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. Login logic is also here.",
        "externalDocs": {
            "description": "Users external docs",
            "url": "https://example.com/docs/users",
        },
    },
    {
        "name": "posts",
        "description": "Manage blog posts",
    },
    {
        "name": "admin",
        "description": "Administrative operations",
    }
]

app = FastAPI(openapi_tags=tags_metadata)

# Group endpoints with tags
@app.get("/users", tags=["users"])
def list_users():
    pass

@app.post("/users", tags=["users"])
def create_user():
    pass

@app.get("/posts", tags=["posts"])
def list_posts():
    pass

@app.delete("/admin/users/{user_id}", tags=["admin", "users"])
def admin_delete_user(user_id: int):
    '''Delete user (admin only).'''
    pass

# Exclude from schema
@app.get("/internal", include_in_schema=False)
def internal_endpoint():
    '''Internal endpoint not shown in docs.'''
    pass

# OpenAPI callbacks (for async notifications)
@app.post(
    "/subscribe",
    callbacks={
        "notification": {
            "{$request.body.callback_url}": {
                "post": {
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "event": {"type": "string"},
                                        "data": {"type": "object"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Callback successfully processed"
                        }
                    }
                }
            }
        }
    }
)
def subscribe(callback_url: str):
    '''
    Subscribe to notifications.

    When events occur, we'll POST to your callback_url.
    '''
    pass
"""
        print(code)


def main() -> None:
    """Main entry point demonstrating API documentation."""
    print("\n" + "=" * 60)
    print("PROGRAM 60: API DOCUMENTATION")
    print("=" * 60 + "\n")

    demo = APIDocumentationDemo()

    demo.demonstrate_openapi_basics()
    demo.demonstrate_schema_documentation()
    demo.demonstrate_endpoint_documentation()
    demo.demonstrate_response_models()
    demo.demonstrate_custom_docs()
    demo.demonstrate_advanced_documentation()

    print("\n" + "=" * 60)
    print("API DOCUMENTATION BEST PRACTICES")
    print("=" * 60)
    print("1. Document all endpoints thoroughly")
    print("2. Provide clear descriptions and examples")
    print("3. Use tags to organize endpoints")
    print("4. Document all possible responses")
    print("5. Include authentication requirements")
    print("6. Add examples for request/response")
    print("7. Document query parameters and headers")
    print("8. Keep documentation up to date")
    print("9. Use semantic versioning")
    print("10. Test documentation examples")
    print("=" * 60)
    print("\n Documentation URLs:")
    print("  - Swagger UI: http://localhost:8000/docs")
    print("  - ReDoc: http://localhost:8000/redoc")
    print("  - OpenAPI JSON: http://localhost:8000/openapi.json")
    print("=" * 60)


if __name__ == "__main__":
    main()
