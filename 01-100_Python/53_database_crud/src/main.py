#!/usr/bin/env python3
"""
Program 53: Database CRUD
Demonstrates comprehensive Create, Read, Update, Delete operations
with SQLAlchemy in a FastAPI context.

Topics covered:
- Complete CRUD implementation
- Query optimization
- Pagination
- Filtering and searching
- Error handling
- Database patterns
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class DatabaseCRUDDemo:
    """Demonstration of database CRUD operations."""

    def demonstrate_complete_crud(self) -> None:
        """Demonstrate complete CRUD implementation."""
        print("COMPLETE CRUD IMPLEMENTATION")
        print("=" * 60)

        code = """
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

Base = declarative_base()

# SQLAlchemy Model
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Pydantic Schemas
class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # For SQLAlchemy models

# CRUD Operations
class CRUDUser:
    '''CRUD operations for User model.'''

    def create(self, db: Session, user_in: UserCreate) -> UserDB:
        '''Create a new user.'''
        db_user = UserDB(
            username=user_in.username,
            email=user_in.email,
            full_name=user_in.full_name,
            hashed_password=hash_password(user_in.password)
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def get(self, db: Session, user_id: int) -> Optional[UserDB]:
        '''Get user by ID.'''
        return db.query(UserDB).filter(UserDB.id == user_id).first()

    def get_by_email(self, db: Session, email: str) -> Optional[UserDB]:
        '''Get user by email.'''
        return db.query(UserDB).filter(UserDB.email == email).first()

    def get_by_username(self, db: Session, username: str) -> Optional[UserDB]:
        '''Get user by username.'''
        return db.query(UserDB).filter(UserDB.username == username).first()

    def get_multi(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[UserDB]:
        '''Get multiple users with pagination.'''
        return db.query(UserDB).offset(skip).limit(limit).all()

    def update(
        self,
        db: Session,
        db_user: UserDB,
        user_in: UserUpdate
    ) -> UserDB:
        '''Update user.'''
        update_data = user_in.dict(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_user, field, value)

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def delete(self, db: Session, user_id: int) -> Optional[UserDB]:
        '''Delete user.'''
        user = db.query(UserDB).filter(UserDB.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
        return user

    def activate(self, db: Session, user_id: int) -> Optional[UserDB]:
        '''Activate user.'''
        user = self.get(db, user_id)
        if user:
            user.is_active = True
            db.commit()
            db.refresh(user)
        return user

    def deactivate(self, db: Session, user_id: int) -> Optional[UserDB]:
        '''Deactivate user.'''
        user = self.get(db, user_id)
        if user:
            user.is_active = False
            db.commit()
            db.refresh(user)
        return user

# Create instance
crud_user = CRUDUser()
"""
        print(code)

    def demonstrate_fastapi_crud(self) -> None:
        """Demonstrate CRUD endpoints in FastAPI."""
        print("\nFASTAPI CRUD ENDPOINTS")
        print("=" * 60)

        code = """
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE
@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    '''Create a new user.'''

    # Check if user already exists
    if crud_user.get_by_email(db, email=user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    if crud_user.get_by_username(db, username=user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    return crud_user.create(db=db, user_in=user)

# READ - List all users
@app.get("/users", response_model=List[UserResponse])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    '''List all users with pagination.'''
    users = crud_user.get_multi(db, skip=skip, limit=limit)
    return users

# READ - Get single user
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    '''Get user by ID.'''
    user = crud_user.get(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

# UPDATE
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db)
):
    '''Update user.'''
    user = crud_user.get(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check email uniqueness if updating email
    if user_in.email and user_in.email != user.email:
        if crud_user.get_by_email(db, email=user_in.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

    return crud_user.update(db=db, db_user=user, user_in=user_in)

# PATCH - Partial update
@app.patch("/users/{user_id}", response_model=UserResponse)
def partial_update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db)
):
    '''Partially update user.'''
    user = crud_user.get(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return crud_user.update(db=db, db_user=user, user_in=user_in)

# DELETE
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    '''Delete user.'''
    user = crud_user.delete(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return None

# Custom actions
@app.post("/users/{user_id}/activate", response_model=UserResponse)
def activate_user(user_id: int, db: Session = Depends(get_db)):
    '''Activate user.'''
    user = crud_user.activate(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@app.post("/users/{user_id}/deactivate", response_model=UserResponse)
def deactivate_user(user_id: int, db: Session = Depends(get_db)):
    '''Deactivate user.'''
    user = crud_user.deactivate(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
"""
        print(code)

    def demonstrate_advanced_queries(self) -> None:
        """Demonstrate advanced query patterns."""
        print("\nADVANCED QUERY PATTERNS")
        print("=" * 60)

        code = """
from sqlalchemy import and_, or_, not_, func
from sqlalchemy.orm import Session
from typing import Optional, List

class CRUDUser:
    def search(
        self,
        db: Session,
        query: Optional[str] = None,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[UserDB]:
        '''Search users with filters.'''

        q = db.query(UserDB)

        # Text search
        if query:
            search = f"%{query}%"
            q = q.filter(
                or_(
                    UserDB.username.ilike(search),
                    UserDB.email.ilike(search),
                    UserDB.full_name.ilike(search)
                )
            )

        # Active filter
        if is_active is not None:
            q = q.filter(UserDB.is_active == is_active)

        return q.offset(skip).limit(limit).all()

    def get_active_users(self, db: Session) -> List[UserDB]:
        '''Get all active users.'''
        return db.query(UserDB).filter(UserDB.is_active == True).all()

    def get_recent_users(
        self,
        db: Session,
        days: int = 7,
        limit: int = 10
    ) -> List[UserDB]:
        '''Get recently created users.'''
        cutoff = datetime.utcnow() - timedelta(days=days)
        return (
            db.query(UserDB)
            .filter(UserDB.created_at >= cutoff)
            .order_by(UserDB.created_at.desc())
            .limit(limit)
            .all()
        )

    def count(self, db: Session, is_active: Optional[bool] = None) -> int:
        '''Count users.'''
        q = db.query(func.count(UserDB.id))
        if is_active is not None:
            q = q.filter(UserDB.is_active == is_active)
        return q.scalar()

    def exists(self, db: Session, user_id: int) -> bool:
        '''Check if user exists.'''
        return db.query(
            db.query(UserDB).filter(UserDB.id == user_id).exists()
        ).scalar()

    def bulk_create(self, db: Session, users: List[UserCreate]) -> List[UserDB]:
        '''Bulk create users.'''
        db_users = [
            UserDB(
                username=user.username,
                email=user.email,
                full_name=user.full_name,
                hashed_password=hash_password(user.password)
            )
            for user in users
        ]
        db.add_all(db_users)
        db.commit()
        return db_users

    def bulk_update_status(
        self,
        db: Session,
        user_ids: List[int],
        is_active: bool
    ) -> int:
        '''Bulk update user status.'''
        count = (
            db.query(UserDB)
            .filter(UserDB.id.in_(user_ids))
            .update({UserDB.is_active: is_active}, synchronize_session=False)
        )
        db.commit()
        return count

    def bulk_delete(self, db: Session, user_ids: List[int]) -> int:
        '''Bulk delete users.'''
        count = (
            db.query(UserDB)
            .filter(UserDB.id.in_(user_ids))
            .delete(synchronize_session=False)
        )
        db.commit()
        return count
"""
        print(code)

    def demonstrate_pagination(self) -> None:
        """Demonstrate pagination patterns."""
        print("\nPAGINATION PATTERNS")
        print("=" * 60)

        code = """
from pydantic import BaseModel
from typing import Generic, TypeVar, List
from math import ceil

T = TypeVar('T')

class PaginationParams(BaseModel):
    '''Pagination parameters.'''
    page: int = 1
    page_size: int = 10

    def get_offset(self) -> int:
        return (self.page - 1) * self.page_size

class PaginatedResponse(BaseModel, Generic[T]):
    '''Paginated response.'''
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int

    @classmethod
    def create(
        cls,
        items: List[T],
        total: int,
        page: int,
        page_size: int
    ):
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=ceil(total / page_size) if page_size > 0 else 0
        )

# CRUD method with pagination
class CRUDUser:
    def get_paginated(
        self,
        db: Session,
        pagination: PaginationParams
    ) -> PaginatedResponse[UserResponse]:
        '''Get paginated users.'''

        # Get total count
        total = db.query(func.count(UserDB.id)).scalar()

        # Get page items
        users = (
            db.query(UserDB)
            .offset(pagination.get_offset())
            .limit(pagination.page_size)
            .all()
        )

        return PaginatedResponse.create(
            items=[UserResponse.from_orm(user) for user in users],
            total=total,
            page=pagination.page,
            page_size=pagination.page_size
        )

# FastAPI endpoint
@app.get("/users", response_model=PaginatedResponse[UserResponse])
def list_users(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db)
):
    '''List users with pagination.'''
    return crud_user.get_paginated(db, pagination)

# Cursor-based pagination (for large datasets)
class CursorPaginationParams(BaseModel):
    cursor: Optional[int] = None  # ID of last item
    limit: int = 10

def get_users_cursor(
    db: Session,
    params: CursorPaginationParams
) -> List[UserDB]:
    '''Get users with cursor pagination.'''
    q = db.query(UserDB)

    if params.cursor:
        q = q.filter(UserDB.id > params.cursor)

    return q.order_by(UserDB.id).limit(params.limit).all()
"""
        print(code)

    def demonstrate_filtering_sorting(self) -> None:
        """Demonstrate filtering and sorting."""
        print("\nFILTERING AND SORTING")
        print("=" * 60)

        code = """
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel

class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

class UserFilter(BaseModel):
    '''User filter parameters.'''
    search: Optional[str] = None
    is_active: Optional[bool] = None
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None
    sort_by: str = "created_at"
    sort_order: SortOrder = SortOrder.DESC

class CRUDUser:
    def get_filtered(
        self,
        db: Session,
        filters: UserFilter,
        skip: int = 0,
        limit: int = 100
    ) -> List[UserDB]:
        '''Get filtered and sorted users.'''

        q = db.query(UserDB)

        # Apply filters
        if filters.search:
            search = f"%{filters.search}%"
            q = q.filter(
                or_(
                    UserDB.username.ilike(search),
                    UserDB.email.ilike(search),
                    UserDB.full_name.ilike(search)
                )
            )

        if filters.is_active is not None:
            q = q.filter(UserDB.is_active == filters.is_active)

        if filters.created_after:
            q = q.filter(UserDB.created_at >= filters.created_after)

        if filters.created_before:
            q = q.filter(UserDB.created_at <= filters.created_before)

        # Apply sorting
        sort_column = getattr(UserDB, filters.sort_by, UserDB.created_at)
        if filters.sort_order == SortOrder.DESC:
            q = q.order_by(sort_column.desc())
        else:
            q = q.order_by(sort_column.asc())

        return q.offset(skip).limit(limit).all()

# FastAPI endpoint
@app.get("/users/filter", response_model=List[UserResponse])
def filter_users(
    filters: UserFilter = Depends(),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    '''Filter and sort users.'''
    users = crud_user.get_filtered(db, filters, skip, limit)
    return users
"""
        print(code)

    def demonstrate_error_handling(self) -> None:
        """Demonstrate error handling in CRUD operations."""
        print("\nERROR HANDLING")
        print("=" * 60)

        code = """
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, status

class CRUDUser:
    def create_safe(self, db: Session, user_in: UserCreate) -> UserDB:
        '''Create user with error handling.'''
        try:
            db_user = UserDB(
                username=user_in.username,
                email=user_in.email,
                full_name=user_in.full_name,
                hashed_password=hash_password(user_in.password)
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user

        except IntegrityError as e:
            db.rollback()
            if "username" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists"
                )
            elif "email" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Database constraint violation"
                )

        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error occurred"
            )

    def update_safe(
        self,
        db: Session,
        user_id: int,
        user_in: UserUpdate
    ) -> Optional[UserDB]:
        '''Update user with error handling.'''
        try:
            user = self.get(db, user_id)
            if not user:
                return None

            for field, value in user_in.dict(exclude_unset=True).items():
                setattr(user, field, value)

            db.commit()
            db.refresh(user)
            return user

        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Update violates database constraints"
            )

        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error occurred"
            )
"""
        print(code)


def main() -> None:
    """Main entry point demonstrating database CRUD operations."""
    print("\n" + "=" * 60)
    print("PROGRAM 53: DATABASE CRUD")
    print("=" * 60 + "\n")

    demo = DatabaseCRUDDemo()

    demo.demonstrate_complete_crud()
    demo.demonstrate_fastapi_crud()
    demo.demonstrate_advanced_queries()
    demo.demonstrate_pagination()
    demo.demonstrate_filtering_sorting()
    demo.demonstrate_error_handling()

    print("\n" + "=" * 60)
    print("CRUD BEST PRACTICES")
    print("=" * 60)
    print("1. Separate database models from API schemas")
    print("2. Use repository/service pattern for CRUD")
    print("3. Implement proper error handling")
    print("4. Add pagination to list endpoints")
    print("5. Validate input before database operations")
    print("6. Use transactions for complex operations")
    print("7. Index frequently queried columns")
    print("8. Implement soft deletes when appropriate")
    print("9. Use bulk operations for efficiency")
    print("10. Add proper logging for debugging")
    print("=" * 60)


if __name__ == "__main__":
    main()
