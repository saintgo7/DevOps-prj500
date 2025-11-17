#!/usr/bin/env python3
"""
Program 55: API Design
Demonstrates REST API design principles including REST principles,
versioning, pagination, and best practices.

Topics covered:
- REST principles and constraints
- Resource naming conventions
- HTTP methods and status codes
- API versioning strategies
- Pagination patterns
- Error handling
- HATEOAS
"""

from typing import Dict, Any, List, Optional


class APIDesignDemo:
    """Demonstration of API design principles and best practices."""

    def demonstrate_rest_principles(self) -> None:
        """Demonstrate REST principles."""
        print("REST PRINCIPLES")
        print("=" * 60)

        principles = """
REST (Representational State Transfer) Constraints:

1. Client-Server Architecture
   - Separation of concerns
   - Client handles UI, server handles data
   - Independent evolution of each

2. Stateless
   - Each request contains all information needed
   - Server doesn't store client context
   - Improves scalability

3. Cacheable
   - Responses must define themselves as cacheable or not
   - Improves performance and scalability

4. Uniform Interface
   - Resource identification in requests
   - Resource manipulation through representations
   - Self-descriptive messages
   - HATEOAS (Hypermedia as the Engine of Application State)

5. Layered System
   - Client doesn't know if connected to end server
   - Allows for load balancers, proxies, caches

6. Code on Demand (Optional)
   - Server can extend client functionality
   - JavaScript, applets, etc.

REST API Characteristics:
- Uses HTTP methods correctly (GET, POST, PUT, DELETE, PATCH)
- Returns appropriate status codes
- Stateless communication
- Resource-based URLs
- JSON or XML representations
- Versioned
- Documented
"""
        print(principles)

    def demonstrate_resource_naming(self) -> None:
        """Demonstrate resource naming conventions."""
        print("\nRESOURCE NAMING CONVENTIONS")
        print("=" * 60)

        code = """
# GOOD: Resource naming follows REST conventions

# Collections (plural nouns)
GET    /users              # List all users
POST   /users              # Create a new user
GET    /users/{id}         # Get user by ID
PUT    /users/{id}         # Update user (full)
PATCH  /users/{id}         # Update user (partial)
DELETE /users/{id}         # Delete user

# Nested resources
GET    /users/{id}/posts           # Get user's posts
POST   /users/{id}/posts           # Create post for user
GET    /users/{id}/posts/{post_id} # Get specific post
PUT    /users/{id}/posts/{post_id} # Update post
DELETE /users/{id}/posts/{post_id} # Delete post

# Actions on resources (use POST with descriptive names)
POST   /users/{id}/activate        # Activate user
POST   /users/{id}/deactivate      # Deactivate user
POST   /users/{id}/send-email      # Send email to user
POST   /posts/{id}/publish         # Publish post
POST   /orders/{id}/cancel         # Cancel order

# Filtering, sorting, searching (query parameters)
GET    /users?status=active&sort=created_at&order=desc
GET    /posts?author_id=123&published=true
GET    /products?category=electronics&min_price=100

# Pagination
GET    /users?page=2&limit=20
GET    /users?offset=40&limit=20

# BAD: Avoid these patterns

# Don't use verbs in URLs
GET    /getUsers               # Bad
GET    /getAllActiveUsers      # Bad
POST   /createUser             # Bad
POST   /deleteUserById/{id}    # Bad

# Don't use singular for collections
GET    /user                   # Bad
POST   /user                   # Bad

# Don't nest too deeply (max 2-3 levels)
GET    /users/{id}/posts/{post_id}/comments/{comment_id}/likes/{like_id}  # Bad

# Use nouns, not verbs
GET    /users/{id}/activate    # Bad (should be POST)
GET    /posts/{id}/delete      # Bad (should be DELETE)

# Good alternatives
GET    /users/{id}             # Good
POST   /users/{id}/activate    # Good (action)
DELETE /posts/{id}             # Good

# Consistent naming
GET    /users                  # Good
GET    /user-profiles          # Good (kebab-case)
GET    /user_profiles          # Good (snake_case) - pick one style
GET    /userProfiles           # Avoid (camelCase in URLs)
"""
        print(code)

    def demonstrate_http_methods(self) -> None:
        """Demonstrate correct HTTP method usage."""
        print("\nHTTP METHODS USAGE")
        print("=" * 60)

        code = """
from fastapi import FastAPI, status

app = FastAPI()

# GET - Retrieve resources (Safe and Idempotent)
# - Should not modify data
# - Can be cached
# - Can be bookmarked

@app.get("/users")
def list_users():
    '''List all users.'''
    return {"users": []}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    '''Get specific user.'''
    return {"id": user_id}

# POST - Create new resources (Not idempotent)
# - Creates new resource
# - Returns 201 Created with Location header
# - Can have side effects

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: dict):
    '''Create new user.'''
    return {"id": 123, **user}

# PUT - Replace entire resource (Idempotent)
# - Replaces entire resource
# - Client provides full representation
# - Returns 200 OK or 204 No Content

@app.put("/users/{user_id}")
def replace_user(user_id: int, user: dict):
    '''Replace entire user.'''
    return {"id": user_id, **user}

# PATCH - Partial update (Can be idempotent)
# - Updates part of resource
# - Client provides only changed fields
# - Returns 200 OK

@app.patch("/users/{user_id}")
def update_user(user_id: int, updates: dict):
    '''Partially update user.'''
    return {"id": user_id, **updates}

# DELETE - Remove resource (Idempotent)
# - Deletes resource
# - Returns 204 No Content or 200 OK with body
# - Subsequent calls return 404 (idempotent result)

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    '''Delete user.'''
    return None

# HEAD - Like GET but no body
# - Check if resource exists
# - Get metadata
# - Check caching

@app.head("/users/{user_id}")
def check_user(user_id: int):
    '''Check if user exists.'''
    return None

# OPTIONS - Get allowed methods
# - Discover what methods are supported
# - CORS preflight requests

@app.options("/users")
def user_options():
    '''Get allowed methods for users endpoint.'''
    return None

# Method selection guide:
# - GET: Retrieve data
# - POST: Create resource or action
# - PUT: Replace entire resource
# - PATCH: Update part of resource
# - DELETE: Remove resource
"""
        print(code)

    def demonstrate_status_codes(self) -> None:
        """Demonstrate appropriate status code usage."""
        print("\nHTTP STATUS CODES")
        print("=" * 60)

        code = """
from fastapi import FastAPI, HTTPException, status, Response

app = FastAPI()

# 2xx Success

@app.get("/users/{user_id}")
def get_user(user_id: int):
    '''200 OK - Successful GET.'''
    return {"id": user_id}

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: dict, response: Response):
    '''201 Created - Resource created.'''
    new_id = 123
    response.headers["Location"] = f"/users/{new_id}"
    return {"id": new_id, **user}

@app.put("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_user(user_id: int, user: dict):
    '''204 No Content - Successful with no response body.'''
    return None

# 3xx Redirection

@app.get("/old-endpoint")
def old_endpoint(response: Response):
    '''301 Moved Permanently - Resource moved.'''
    response.status_code = status.HTTP_301_MOVED_PERMANENTLY
    response.headers["Location"] = "/new-endpoint"
    return None

@app.get("/temporary")
def temporary_redirect(response: Response):
    '''302 Found - Temporary redirect.'''
    response.status_code = status.HTTP_302_FOUND
    response.headers["Location"] = "/new-location"
    return None

# 4xx Client Errors

@app.get("/protected")
def protected_route():
    '''400 Bad Request - Invalid request.'''
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid request parameters"
    )

@app.get("/secure")
def secure_route():
    '''401 Unauthorized - Authentication required.'''
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required",
        headers={"WWW-Authenticate": "Bearer"}
    )

@app.get("/admin")
def admin_route():
    '''403 Forbidden - Authenticated but not authorized.'''
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient permissions"
    )

@app.get("/nonexistent")
def not_found():
    '''404 Not Found - Resource not found.'''
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Resource not found"
    )

@app.patch("/readonly")
def readonly_resource():
    '''405 Method Not Allowed - HTTP method not supported.'''
    raise HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail="PATCH not allowed on this resource"
    )

@app.post("/duplicate")
def create_duplicate():
    '''409 Conflict - Resource conflict.'''
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Resource already exists"
    )

@app.post("/invalid-data")
def invalid_data():
    '''422 Unprocessable Entity - Validation error.'''
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Validation failed"
    )

@app.get("/rate-limited")
def rate_limited(response: Response):
    '''429 Too Many Requests - Rate limit exceeded.'''
    raise HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail="Rate limit exceeded",
        headers={"Retry-After": "60"}
    )

# 5xx Server Errors

@app.get("/error")
def server_error():
    '''500 Internal Server Error - Server error.'''
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal server error"
    )

@app.get("/maintenance")
def maintenance():
    '''503 Service Unavailable - Service down.'''
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Service temporarily unavailable",
        headers={"Retry-After": "300"}
    )
"""
        print(code)

    def demonstrate_versioning(self) -> None:
        """Demonstrate API versioning strategies."""
        print("\nAPI VERSIONING STRATEGIES")
        print("=" * 60)

        code = """
from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

# 1. URL Path Versioning (Recommended)
# Pros: Clear, explicit, easy to test
# Cons: Duplicate code if not abstracted

@app.get("/api/v1/users")
def get_users_v1():
    return {"version": "1.0", "users": []}

@app.get("/api/v2/users")
def get_users_v2():
    return {"version": "2.0", "users": [], "metadata": {}}

# Using APIRouter for versions
from fastapi import APIRouter

router_v1 = APIRouter(prefix="/api/v1", tags=["v1"])
router_v2 = APIRouter(prefix="/api/v2", tags=["v2"])

@router_v1.get("/users")
def v1_users():
    return {"version": "1.0"}

@router_v2.get("/users")
def v2_users():
    return {"version": "2.0"}

app.include_router(router_v1)
app.include_router(router_v2)

# 2. Header Versioning
# Pros: Clean URLs
# Cons: Not visible in URL, harder to test

@app.get("/users")
def get_users(api_version: str = Header("1.0", alias="API-Version")):
    if api_version == "1.0":
        return {"version": "1.0", "users": []}
    elif api_version == "2.0":
        return {"version": "2.0", "users": []}
    else:
        raise HTTPException(status_code=400, detail="Unsupported API version")

# 3. Query Parameter Versioning
# Pros: Simple to implement
# Cons: Not RESTful, can be forgotten

@app.get("/users")
def get_users_query(version: str = "1.0"):
    if version == "1.0":
        return {"version": "1.0"}
    elif version == "2.0":
        return {"version": "2.0"}
    return {"error": "Unsupported version"}

# 4. Accept Header (Content Negotiation)
# Pros: RESTful
# Cons: Complex to implement

@app.get("/users")
def get_users_accept(accept: str = Header(None)):
    # Example: Accept: application/vnd.myapi.v2+json
    if "v2" in accept:
        return {"version": "2.0"}
    return {"version": "1.0"}

# Version deprecation
from datetime import datetime

@app.get("/api/v1/users")
def deprecated_endpoint():
    return {
        "data": [],
        "deprecated": True,
        "deprecation_date": "2025-01-01",
        "sunset_date": "2025-06-01",
        "migration_guide": "https://api.example.com/docs/migration/v1-to-v2"
    }

# Best practices:
# - Version from the start
# - Keep versions for reasonable time (12-24 months)
# - Announce deprecation well in advance
# - Document migration path
# - Support at least 2 versions
# - URL versioning is most common and recommended
"""
        print(code)

    def demonstrate_pagination(self) -> None:
        """Demonstrate pagination patterns."""
        print("\nPAGINATION PATTERNS")
        print("=" * 60)

        code = """
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional, Generic, TypeVar
from math import ceil

app = FastAPI()

T = TypeVar('T')

# 1. Offset/Limit Pagination (Most common)
class OffsetPagination(BaseModel):
    items: List[dict]
    total: int
    offset: int
    limit: int

@app.get("/users", response_model=OffsetPagination)
def get_users(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    # Simulated data
    total = 100
    items = [{"id": i} for i in range(offset, min(offset + limit, total))]

    return {
        "items": items,
        "total": total,
        "offset": offset,
        "limit": limit
    }

# 2. Page/Size Pagination
class PagePagination(BaseModel, Generic[T]):
    items: List[T]
    page: int
    page_size: int
    total_pages: int
    total_items: int

@app.get("/posts")
def get_posts(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    total_items = 95
    total_pages = ceil(total_items / page_size)
    offset = (page - 1) * page_size

    items = [{"id": i} for i in range(offset, min(offset + page_size, total_items))]

    return {
        "items": items,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "total_items": total_items
    }

# 3. Cursor Pagination (For large datasets)
from datetime import datetime

class CursorPagination(BaseModel):
    items: List[dict]
    next_cursor: Optional[str]
    has_more: bool

@app.get("/feed", response_model=CursorPagination)
def get_feed(
    cursor: Optional[str] = None,
    limit: int = Query(10, ge=1, le=100)
):
    # Cursor is typically the ID or timestamp of last item
    # Simulated data
    items = [{"id": i, "created_at": datetime.now()} for i in range(limit)]

    next_cursor = None
    has_more = False

    if len(items) == limit:
        # There might be more items
        next_cursor = str(items[-1]["id"])
        has_more = True

    return {
        "items": items,
        "next_cursor": next_cursor,
        "has_more": has_more
    }

# 4. Pagination with Links (HATEOAS style)
class LinkedPagination(BaseModel):
    items: List[dict]
    links: dict
    meta: dict

@app.get("/articles")
def get_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    base_url = "https://api.example.com/articles"
    total_items = 100
    total_pages = ceil(total_items / page_size)

    items = [{"id": i} for i in range((page-1) * page_size, min(page * page_size, total_items))]

    links = {
        "self": f"{base_url}?page={page}&page_size={page_size}",
        "first": f"{base_url}?page=1&page_size={page_size}",
        "last": f"{base_url}?page={total_pages}&page_size={page_size}",
    }

    if page > 1:
        links["prev"] = f"{base_url}?page={page-1}&page_size={page_size}"

    if page < total_pages:
        links["next"] = f"{base_url}?page={page+1}&page_size={page_size}"

    return {
        "items": items,
        "links": links,
        "meta": {
            "current_page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "total_items": total_items
        }
    }

# Choose pagination strategy based on:
# - Offset/Limit: Small to medium datasets
# - Page/Size: User-facing pagination
# - Cursor: Large datasets, infinite scroll, real-time feeds
# - Links: HATEOAS compliance
"""
        print(code)

    def demonstrate_error_responses(self) -> None:
        """Demonstrate consistent error responses."""
        print("\nERROR RESPONSE PATTERNS")
        print("=" * 60)

        code = """
from pydantic import BaseModel
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

# Standard error response model
class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[dict] = None
    status_code: int
    timestamp: str
    path: str

# Single error
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.status_code,
            "message": exc.detail,
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path
        }
    )

# Validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "message": "Request validation failed",
            "details": exc.errors(),
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path
        }
    )

# Application-specific errors
class APIError(Exception):
    def __init__(self, message: str, status_code: int, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details

@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.status_code,
            "message": exc.message,
            "details": exc.details,
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path
        }
    )

# Example error responses:
# {
#     "error": 404,
#     "message": "User not found",
#     "timestamp": "2025-11-17T12:00:00",
#     "path": "/users/999"
# }
#
# {
#     "error": 422,
#     "message": "Validation failed",
#     "details": [
#         {"field": "email", "message": "Invalid email format"},
#         {"field": "age", "message": "Must be at least 18"}
#     ],
#     "timestamp": "2025-11-17T12:00:00",
#     "path": "/users"
# }
"""
        print(code)


def main() -> None:
    """Main entry point demonstrating API design."""
    print("\n" + "=" * 60)
    print("PROGRAM 55: API DESIGN")
    print("=" * 60 + "\n")

    demo = APIDesignDemo()

    demo.demonstrate_rest_principles()
    demo.demonstrate_resource_naming()
    demo.demonstrate_http_methods()
    demo.demonstrate_status_codes()
    demo.demonstrate_versioning()
    demo.demonstrate_pagination()
    demo.demonstrate_error_responses()

    print("\n" + "=" * 60)
    print("API DESIGN BEST PRACTICES")
    print("=" * 60)
    print("1. Follow REST principles and constraints")
    print("2. Use resource-based URLs (nouns, not verbs)")
    print("3. Use appropriate HTTP methods and status codes")
    print("4. Version your API from the start")
    print("5. Implement pagination for list endpoints")
    print("6. Provide consistent error responses")
    print("7. Document your API (OpenAPI/Swagger)")
    print("8. Use HTTPS everywhere")
    print("9. Implement rate limiting")
    print("10. Support filtering, sorting, and searching")
    print("=" * 60)


if __name__ == "__main__":
    main()
