#!/usr/bin/env python3
"""
Program 52: SQLAlchemy Basics
Demonstrates SQLAlchemy for database operations including engine,
session, declarative base, and models.

Topics covered:
- Database engine creation
- Session management
- Declarative base and models
- Table creation
- Basic queries
- SQLAlchemy Core vs ORM
"""

from typing import Dict, Any, List, Optional


class SQLAlchemyBasicsDemo:
    """Demonstration of SQLAlchemy basics."""

    def demonstrate_engine_creation(self) -> None:
        """Demonstrate database engine creation."""
        print("DATABASE ENGINE CREATION")
        print("=" * 60)

        code = """
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# SQLite (file-based)
engine = create_engine('sqlite:///database.db', echo=True)

# SQLite (in-memory)
engine = create_engine('sqlite:///:memory:', echo=True)

# PostgreSQL
engine = create_engine(
    'postgresql://user:password@localhost:5432/dbname',
    echo=True
)

# MySQL
engine = create_engine(
    'mysql+pymysql://user:password@localhost:3306/dbname',
    echo=True
)

# With connection pool
engine = create_engine(
    'postgresql://user:password@localhost/dbname',
    poolclass=QueuePool,
    pool_size=10,  # Number of connections to maintain
    max_overflow=20,  # Max additional connections
    pool_timeout=30,  # Timeout for getting connection
    pool_recycle=3600,  # Recycle connections after 1 hour
    echo=True  # Log SQL statements
)

# Engine configuration
engine = create_engine(
    'sqlite:///database.db',
    echo=False,  # Don't log SQL
    future=True,  # Use SQLAlchemy 2.0 style
)

# Test connection
with engine.connect() as conn:
    result = conn.execute("SELECT 1")
    print(result.scalar())  # 1
"""
        print(code)

    def demonstrate_declarative_base(self) -> None:
        """Demonstrate declarative base and models."""
        print("\nDECLARATIVE BASE AND MODELS")
        print("=" * 60)

        code = """
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Create base class
Base = declarative_base()

# Define models
class User(Base):
    '''User model.'''
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"

class Post(Base):
    '''Post model.'''
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    content = Column(String, nullable=False)  # TEXT in database
    published = Column(Boolean, default=False)
    views = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Post(title='{self.title}')>"

# Column types:
# Integer, BigInteger, SmallInteger
# String(length), Text
# Boolean
# Float, Numeric(precision, scale)
# DateTime, Date, Time
# JSON
# LargeBinary (BLOB)
# Enum

# Column constraints:
# primary_key=True
# unique=True
# nullable=False
# index=True
# autoincrement=True
# default=value or callable
# server_default="value" (database-level default)
# onupdate=callable

# Create tables
from sqlalchemy import create_engine

engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)

# Drop tables
# Base.metadata.drop_all(engine)

# Create specific tables
# User.__table__.create(engine)
# Post.__table__.create(engine)
"""
        print(code)

    def demonstrate_session_management(self) -> None:
        """Demonstrate session management."""
        print("\nSESSION MANAGEMENT")
        print("=" * 60)

        code = """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

engine = create_engine('sqlite:///database.db')

# Create session factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

# Use session
session = SessionLocal()

try:
    # Perform database operations
    user = User(username="john", email="john@example.com", password_hash="hashed")
    session.add(user)
    session.commit()

except Exception as e:
    session.rollback()
    print(f"Error: {e}")

finally:
    session.close()

# Using context manager (recommended)
with SessionLocal() as session:
    user = User(username="jane", email="jane@example.com", password_hash="hashed")
    session.add(user)
    session.commit()
    # Session automatically closed

# Scoped session (thread-local)
from sqlalchemy.orm import scoped_session

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Use in request/response cycle
def get_user(user_id):
    session = Session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        return user
    finally:
        Session.remove()  # Remove thread-local session

# Dependency for FastAPI
def get_db():
    '''Database session dependency.'''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Use in FastAPI
from fastapi import Depends

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    return user
"""
        print(code)

    def demonstrate_basic_queries(self) -> None:
        """Demonstrate basic database queries."""
        print("\nBASIC QUERIES")
        print("=" * 60)

        code = """
from sqlalchemy import select
from sqlalchemy.orm import Session

# Get session
session = SessionLocal()

# 1. Query all records
users = session.query(User).all()
# Or: users = session.execute(select(User)).scalars().all()

# 2. Query with filter
user = session.query(User).filter(User.username == "john").first()
# Or: user = session.execute(select(User).where(User.username == "john")).scalar_one_or_none()

# 3. Query by primary key
user = session.query(User).get(1)
# Or: user = session.get(User, 1)

# 4. Filter operations
users = session.query(User).filter(User.is_active == True).all()
users = session.query(User).filter(User.id > 10).all()
users = session.query(User).filter(User.username.like("%john%")).all()
users = session.query(User).filter(User.email.ilike("%example.com%")).all()
users = session.query(User).filter(User.id.in_([1, 2, 3])).all()

# 5. Multiple filters (AND)
users = session.query(User).filter(
    User.is_active == True,
    User.created_at > datetime(2024, 1, 1)
).all()

# 6. OR condition
from sqlalchemy import or_

users = session.query(User).filter(
    or_(User.username == "john", User.username == "jane")
).all()

# 7. AND/OR combination
from sqlalchemy import and_

users = session.query(User).filter(
    and_(
        User.is_active == True,
        or_(User.username == "john", User.email.like("%admin%"))
    )
).all()

# 8. Count
count = session.query(User).count()
count = session.query(User).filter(User.is_active == True).count()

# 9. Order by
users = session.query(User).order_by(User.created_at.desc()).all()
users = session.query(User).order_by(User.username.asc()).all()

# 10. Limit and offset (pagination)
users = session.query(User).limit(10).offset(20).all()

# 11. First and one
user = session.query(User).filter(User.id == 1).first()  # Returns None if not found
user = session.query(User).filter(User.id == 1).one()  # Raises if not exactly one

# 12. Distinct
usernames = session.query(User.username).distinct().all()

# 13. Specific columns
results = session.query(User.id, User.username).all()

# 14. Exists
exists = session.query(User).filter(User.username == "john").first() is not None

session.close()
"""
        print(code)

    def demonstrate_crud_operations(self) -> None:
        """Demonstrate CRUD operations."""
        print("\nCRUD OPERATIONS")
        print("=" * 60)

        code = """
from sqlalchemy.orm import Session

session = SessionLocal()

# CREATE
# Single record
user = User(
    username="john",
    email="john@example.com",
    password_hash="hashed_password"
)
session.add(user)
session.commit()
session.refresh(user)  # Refresh to get auto-generated id
print(f"Created user with ID: {user.id}")

# Multiple records
users = [
    User(username="alice", email="alice@example.com", password_hash="hash1"),
    User(username="bob", email="bob@example.com", password_hash="hash2")
]
session.add_all(users)
session.commit()

# READ
# Get by ID
user = session.get(User, 1)

# Get by filter
user = session.query(User).filter(User.username == "john").first()

# Get all
users = session.query(User).all()

# UPDATE
# Update single record
user = session.get(User, 1)
user.email = "newemail@example.com"
user.updated_at = datetime.utcnow()
session.commit()

# Update multiple records
session.query(User).filter(User.is_active == False).update({
    User.is_active: True
})
session.commit()

# DELETE
# Delete single record
user = session.get(User, 1)
session.delete(user)
session.commit()

# Delete multiple records
session.query(User).filter(User.created_at < datetime(2020, 1, 1)).delete()
session.commit()

# Bulk insert (faster for many records)
session.bulk_insert_mappings(User, [
    {"username": "user1", "email": "user1@example.com", "password_hash": "hash"},
    {"username": "user2", "email": "user2@example.com", "password_hash": "hash"}
])
session.commit()

# Bulk update
session.bulk_update_mappings(User, [
    {"id": 1, "is_active": False},
    {"id": 2, "is_active": False}
])
session.commit()

session.close()
"""
        print(code)

    def demonstrate_raw_sql(self) -> None:
        """Demonstrate executing raw SQL."""
        print("\nRAW SQL EXECUTION")
        print("=" * 60)

        code = """
from sqlalchemy import text

session = SessionLocal()

# Execute raw SQL
result = session.execute(text("SELECT * FROM users WHERE id = :id"), {"id": 1})
user = result.fetchone()

# Insert with raw SQL
session.execute(
    text("INSERT INTO users (username, email, password_hash) VALUES (:username, :email, :password)"),
    {"username": "john", "email": "john@example.com", "password": "hashed"}
)
session.commit()

# Update with raw SQL
session.execute(
    text("UPDATE users SET is_active = :active WHERE id = :id"),
    {"active": False, "id": 1}
)
session.commit()

# Using connection directly
from sqlalchemy import create_engine

engine = create_engine('sqlite:///database.db')

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM users"))
    for row in result:
        print(row)

    # With transaction
    with conn.begin():
        conn.execute(text("INSERT INTO users (username, email, password_hash) VALUES ('test', 'test@example.com', 'hash')"))

session.close()
"""
        print(code)

    def demonstrate_transactions(self) -> None:
        """Demonstrate transaction management."""
        print("\nTRANSACTION MANAGEMENT")
        print("=" * 60)

        code = """
from sqlalchemy.orm import Session

session = SessionLocal()

# Automatic transaction (commit/rollback)
try:
    user = User(username="john", email="john@example.com", password_hash="hash")
    session.add(user)

    post = Post(title="First Post", content="Content")
    session.add(post)

    session.commit()  # Commit both operations

except Exception as e:
    session.rollback()  # Rollback both if either fails
    print(f"Error: {e}")

finally:
    session.close()

# Explicit transaction with nested transactions
session = SessionLocal()

# Savepoint
try:
    user = User(username="alice", email="alice@example.com", password_hash="hash")
    session.add(user)
    session.flush()  # Send to database but don't commit

    # Savepoint
    session.begin_nested()
    try:
        post = Post(title="Post", content="Content")
        session.add(post)
        session.commit()  # Commit savepoint
    except Exception as e:
        session.rollback()  # Rollback savepoint only
        print(f"Post creation failed: {e}")

    session.commit()  # Commit user

except Exception as e:
    session.rollback()
    print(f"Transaction failed: {e}")

finally:
    session.close()

# Context manager for transactions
from contextlib import contextmanager

@contextmanager
def transaction_scope():
    '''Provide transactional scope for operations.'''
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# Usage
with transaction_scope() as session:
    user = User(username="bob", email="bob@example.com", password_hash="hash")
    session.add(user)
    # Automatically committed or rolled back
"""
        print(code)


def main() -> None:
    """Main entry point demonstrating SQLAlchemy basics."""
    print("\n" + "=" * 60)
    print("PROGRAM 52: SQLALCHEMY BASICS")
    print("=" * 60 + "\n")

    demo = SQLAlchemyBasicsDemo()

    demo.demonstrate_engine_creation()
    demo.demonstrate_declarative_base()
    demo.demonstrate_session_management()
    demo.demonstrate_basic_queries()
    demo.demonstrate_crud_operations()
    demo.demonstrate_raw_sql()
    demo.demonstrate_transactions()

    print("\n" + "=" * 60)
    print("SQLALCHEMY BEST PRACTICES")
    print("=" * 60)
    print("1. Always close sessions (use context managers)")
    print("2. Use connection pooling in production")
    print("3. Use transactions for data consistency")
    print("4. Use indexes for frequently queried columns")
    print("5. Avoid N+1 query problems (use joins)")
    print("6. Use bulk operations for many records")
    print("7. Use lazy loading carefully")
    print("8. Handle exceptions and rollback properly")
    print("9. Use scoped sessions in web applications")
    print("10. Keep models simple and focused")
    print("=" * 60)


if __name__ == "__main__":
    main()
