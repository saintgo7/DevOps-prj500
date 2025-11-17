#!/usr/bin/env python3
"""
Program 56: REST API
Demonstrates a complete REST API implementation with CRUD operations,
validation, error handling, and best practices.

Topics covered:
- Complete REST API structure
- CRUD endpoints
- Request validation
- Error handling
- Authentication/Authorization
- Database integration
- Testing patterns
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class RestAPIDemo:
    """Demonstration of complete REST API implementation."""

    def demonstrate_complete_api(self) -> None:
        """Demonstrate complete REST API structure."""
        print("COMPLETE REST API STRUCTURE")
        print("=" * 60)

        code = """
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

# === Database Setup ===
DATABASE_URL = "sqlite:///./blog.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# === Models ===
class BlogPost(Base):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    content = Column(String, nullable=False)
    author = Column(String(100), nullable=False)
    published = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# === Schemas ===
class BlogPostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1, max_length=100)

class BlogPostCreate(BlogPostBase):
    published: bool = False

class BlogPostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    published: Optional[bool] = None

class BlogPostResponse(BlogPostBase):
    id: int
    published: bool
    view_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaginatedResponse(BaseModel):
    items: List[BlogPostResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

# === Dependencies ===
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# === CRUD Operations ===
class BlogPostCRUD:
    @staticmethod
    def create(db: Session, post: BlogPostCreate) -> BlogPost:
        db_post = BlogPost(**post.dict())
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post

    @staticmethod
    def get(db: Session, post_id: int) -> Optional[BlogPost]:
        return db.query(BlogPost).filter(BlogPost.id == post_id).first()

    @staticmethod
    def get_multi(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        published_only: bool = False
    ) -> List[BlogPost]:
        query = db.query(BlogPost)
        if published_only:
            query = query.filter(BlogPost.published == True)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def count(db: Session, published_only: bool = False) -> int:
        query = db.query(BlogPost)
        if published_only:
            query = query.filter(BlogPost.published == True)
        return query.count()

    @staticmethod
    def update(db: Session, post_id: int, post_update: BlogPostUpdate) -> Optional[BlogPost]:
        db_post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
        if not db_post:
            return None

        update_data = post_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_post, field, value)

        db.commit()
        db.refresh(db_post)
        return db_post

    @staticmethod
    def delete(db: Session, post_id: int) -> bool:
        db_post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
        if not db_post:
            return False

        db.delete(db_post)
        db.commit()
        return True

# === FastAPI App ===
app = FastAPI(
    title="Blog API",
    description="A complete REST API for a blog",
    version="1.0.0"
)

# === Endpoints ===

# CREATE
@app.post("/posts", response_model=BlogPostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: BlogPostCreate, db: Session = Depends(get_db)):
    '''Create a new blog post.'''
    return BlogPostCRUD.create(db, post)

# READ - List all
@app.get("/posts", response_model=PaginatedResponse)
def list_posts(
    page: int = 1,
    page_size: int = 10,
    published_only: bool = False,
    db: Session = Depends(get_db)
):
    '''List all blog posts with pagination.'''
    skip = (page - 1) * page_size
    posts = BlogPostCRUD.get_multi(db, skip, page_size, published_only)
    total = BlogPostCRUD.count(db, published_only)

    return {
        "items": posts,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }

# READ - Get single
@app.get("/posts/{post_id}", response_model=BlogPostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    '''Get a specific blog post.'''
    post = BlogPostCRUD.get(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog post not found"
        )

    # Increment view count
    post.view_count += 1
    db.commit()

    return post

# UPDATE - Full update
@app.put("/posts/{post_id}", response_model=BlogPostResponse)
def update_post(
    post_id: int,
    post_update: BlogPostUpdate,
    db: Session = Depends(get_db)
):
    '''Update a blog post.'''
    post = BlogPostCRUD.update(db, post_id, post_update)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog post not found"
        )
    return post

# DELETE
@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    '''Delete a blog post.'''
    if not BlogPostCRUD.delete(db, post_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog post not found"
        )
    return None

# Custom actions
@app.post("/posts/{post_id}/publish", response_model=BlogPostResponse)
def publish_post(post_id: int, db: Session = Depends(get_db)):
    '''Publish a blog post.'''
    post = BlogPostCRUD.get(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog post not found"
        )

    post.published = True
    db.commit()
    db.refresh(post)
    return post

@app.post("/posts/{post_id}/unpublish", response_model=BlogPostResponse)
def unpublish_post(post_id: int, db: Session = Depends(get_db)):
    '''Unpublish a blog post.'''
    post = BlogPostCRUD.get(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog post not found"
        )

    post.published = False
    db.commit()
    db.refresh(post)
    return post

# Search
@app.get("/posts/search", response_model=List[BlogPostResponse])
def search_posts(
    q: str,
    published_only: bool = True,
    db: Session = Depends(get_db)
):
    '''Search blog posts by title or content.'''
    query = db.query(BlogPost)

    if published_only:
        query = query.filter(BlogPost.published == True)

    query = query.filter(
        (BlogPost.title.contains(q)) | (BlogPost.content.contains(q))
    )

    return query.all()

# Health check
@app.get("/health")
def health_check():
    '''API health check.'''
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

# Run with: uvicorn main:app --reload
"""
        print(code)

    def demonstrate_error_handling(self) -> None:
        """Demonstrate comprehensive error handling."""
        print("\nCOMPREHENSIVE ERROR HANDLING")
        print("=" * 60)

        code = """
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from pydantic import BaseModel
import logging

app = FastAPI()
logger = logging.getLogger(__name__)

# Custom exceptions
class ResourceNotFoundError(Exception):
    def __init__(self, resource: str, resource_id: int):
        self.resource = resource
        self.resource_id = resource_id
        self.message = f"{resource} with ID {resource_id} not found"

class DuplicateResourceError(Exception):
    def __init__(self, resource: str, field: str, value: str):
        self.resource = resource
        self.field = field
        self.value = value
        self.message = f"{resource} with {field}='{value}' already exists"

# Error response model
class ErrorResponse(BaseModel):
    error: str
    message: str
    status_code: int
    timestamp: str
    path: str

# Exception handlers
@app.exception_handler(ResourceNotFoundError)
async def resource_not_found_handler(request: Request, exc: ResourceNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Not Found",
            "message": exc.message,
            "status_code": 404,
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path
        }
    )

@app.exception_handler(DuplicateResourceError)
async def duplicate_resource_handler(request: Request, exc: DuplicateResourceError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Conflict",
            "message": exc.message,
            "status_code": 409,
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "message": "Request validation failed",
            "details": exc.errors(),
            "status_code": 422,
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path
        }
    )

@app.exception_handler(SQLAlchemyError)
async def database_error_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"Database error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Database Error",
            "message": "A database error occurred",
            "status_code": 500,
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "status_code": 500,
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path
        }
    )

# Usage in endpoints
@app.get("/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not post:
        raise ResourceNotFoundError("BlogPost", post_id)
    return post

@app.post("/posts")
def create_post(post: BlogPostCreate, db: Session = Depends(get_db)):
    try:
        db_post = BlogPost(**post.dict())
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
    except IntegrityError as e:
        db.rollback()
        if "title" in str(e):
            raise DuplicateResourceError("BlogPost", "title", post.title)
        raise
"""
        print(code)

    def demonstrate_filtering_sorting(self) -> None:
        """Demonstrate advanced filtering and sorting."""
        print("\nADVANCED FILTERING AND SORTING")
        print("=" * 60)

        code = """
from fastapi import Query
from typing import Optional, List
from enum import Enum

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"

@app.get("/posts/advanced")
def list_posts_advanced(
    # Pagination
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),

    # Filtering
    author: Optional[str] = None,
    published: Optional[bool] = None,
    search: Optional[str] = None,
    created_after: Optional[datetime] = None,
    created_before: Optional[datetime] = None,
    min_views: Optional[int] = None,

    # Sorting
    sort_by: str = Query("created_at", regex="^(created_at|updated_at|title|view_count)$"),
    sort_order: SortOrder = SortOrder.desc,

    db: Session = Depends(get_db)
):
    '''List posts with advanced filtering and sorting.'''

    # Build query
    query = db.query(BlogPost)

    # Apply filters
    if author:
        query = query.filter(BlogPost.author == author)

    if published is not None:
        query = query.filter(BlogPost.published == published)

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (BlogPost.title.ilike(search_pattern)) |
            (BlogPost.content.ilike(search_pattern))
        )

    if created_after:
        query = query.filter(BlogPost.created_at >= created_after)

    if created_before:
        query = query.filter(BlogPost.created_at <= created_before)

    if min_views:
        query = query.filter(BlogPost.view_count >= min_views)

    # Get total count
    total = query.count()

    # Apply sorting
    sort_column = getattr(BlogPost, sort_by)
    if sort_order == SortOrder.desc:
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # Apply pagination
    skip = (page - 1) * page_size
    posts = query.offset(skip).limit(page_size).all()

    return {
        "items": posts,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
        "filters": {
            "author": author,
            "published": published,
            "search": search,
            "created_after": created_after,
            "created_before": created_before,
            "min_views": min_views
        },
        "sort": {
            "by": sort_by,
            "order": sort_order
        }
    }
"""
        print(code)

    def demonstrate_api_testing(self) -> None:
        """Demonstrate API testing patterns."""
        print("\nAPI TESTING PATTERNS")
        print("=" * 60)

        code = """
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Test database setup
TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(bind=test_engine, autocommit=False, autoflush=False)

# Override get_db dependency
def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Test client
client = TestClient(app)

# Fixtures
@pytest.fixture
def setup_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def sample_post():
    return {
        "title": "Test Post",
        "content": "This is a test post",
        "author": "Test Author"
    }

# Tests
def test_create_post(setup_database, sample_post):
    '''Test creating a blog post.'''
    response = client.post("/posts", json=sample_post)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == sample_post["title"]
    assert data["author"] == sample_post["author"]
    assert "id" in data

def test_get_post(setup_database, sample_post):
    '''Test getting a blog post.'''
    # Create post
    create_response = client.post("/posts", json=sample_post)
    post_id = create_response.json()["id"]

    # Get post
    response = client.get(f"/posts/{post_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == post_id
    assert data["title"] == sample_post["title"]

def test_get_nonexistent_post(setup_database):
    '''Test getting a non-existent post.'''
    response = client.get("/posts/9999")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_update_post(setup_database, sample_post):
    '''Test updating a blog post.'''
    # Create post
    create_response = client.post("/posts", json=sample_post)
    post_id = create_response.json()["id"]

    # Update post
    update_data = {"title": "Updated Title"}
    response = client.put(f"/posts/{post_id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"

def test_delete_post(setup_database, sample_post):
    '''Test deleting a blog post.'''
    # Create post
    create_response = client.post("/posts", json=sample_post)
    post_id = create_response.json()["id"]

    # Delete post
    response = client.delete(f"/posts/{post_id}")

    assert response.status_code == 204

    # Verify deleted
    get_response = client.get(f"/posts/{post_id}")
    assert get_response.status_code == 404

def test_list_posts(setup_database, sample_post):
    '''Test listing posts with pagination.'''
    # Create multiple posts
    for i in range(5):
        post = sample_post.copy()
        post["title"] = f"Post {i}"
        client.post("/posts", json=post)

    # List posts
    response = client.get("/posts?page=1&page_size=3")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 5
    assert len(data["items"]) == 3
    assert data["total_pages"] == 2

def test_validation_error(setup_database):
    '''Test validation error.'''
    invalid_post = {
        "title": "",  # Empty title
        "content": "Content",
        "author": "Author"
    }

    response = client.post("/posts", json=invalid_post)

    assert response.status_code == 422
    assert "validation" in response.json()["detail"][0]["type"]

# Run tests: pytest test_main.py -v
"""
        print(code)


def main() -> None:
    """Main entry point demonstrating REST API."""
    print("\n" + "=" * 60)
    print("PROGRAM 56: REST API")
    print("=" * 60 + "\n")

    demo = RestAPIDemo()

    demo.demonstrate_complete_api()
    demo.demonstrate_error_handling()
    demo.demonstrate_filtering_sorting()
    demo.demonstrate_api_testing()

    print("\n" + "=" * 60)
    print("REST API BEST PRACTICES")
    print("=" * 60)
    print("1. Follow REST principles consistently")
    print("2. Use appropriate HTTP methods and status codes")
    print("3. Implement comprehensive error handling")
    print("4. Add request validation with Pydantic")
    print("5. Implement pagination for list endpoints")
    print("6. Support filtering and sorting")
    print("7. Write comprehensive tests")
    print("8. Document with OpenAPI/Swagger")
    print("9. Use dependency injection")
    print("10. Separate concerns (models, schemas, CRUD)")
    print("=" * 60)


if __name__ == "__main__":
    main()
