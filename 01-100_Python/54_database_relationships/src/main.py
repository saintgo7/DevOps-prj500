#!/usr/bin/env python3
"""
Program 54: Database Relationships
Demonstrates database relationships in SQLAlchemy including
one-to-many, many-to-many, and joins.

Topics covered:
- One-to-One relationships
- One-to-Many relationships
- Many-to-Many relationships
- Foreign keys
- Relationship configuration
- Joins and eager loading
"""

from typing import Dict, Any, List, Optional


class DatabaseRelationshipsDemo:
    """Demonstration of database relationships."""

    def demonstrate_one_to_many(self) -> None:
        """Demonstrate one-to-many relationships."""
        print("ONE-TO-MANY RELATIONSHIPS")
        print("=" * 60)

        code = """
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# One-to-Many: User has many Posts
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    # Relationship: one user has many posts
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship: many posts belong to one user
    author = relationship("User", back_populates="posts")

# Usage
from sqlalchemy.orm import Session

# Create user with posts
user = User(username="john", email="john@example.com")
user.posts = [
    Post(title="First Post", content="Content 1"),
    Post(title="Second Post", content="Content 2")
]
db.add(user)
db.commit()

# Access posts from user
user = db.query(User).filter(User.id == 1).first()
for post in user.posts:
    print(f"{post.title} by {post.author.username}")

# Access user from post
post = db.query(Post).filter(Post.id == 1).first()
print(f"Author: {post.author.username}")

# Create post for existing user
user = db.query(User).first()
post = Post(title="New Post", content="Content", author=user)
db.add(post)
db.commit()

# Delete user (cascade deletes posts)
user = db.query(User).first()
db.delete(user)  # All user's posts will be deleted too
db.commit()
"""
        print(code)

    def demonstrate_many_to_many(self) -> None:
        """Demonstrate many-to-many relationships."""
        print("\nMANY-TO-MANY RELATIONSHIPS")
        print("=" * 60)

        code = """
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Association table for many-to-many relationship
post_tags = Table(
    'post_tags',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(String, nullable=False)

    # Many-to-many relationship with Tag
    tags = relationship(
        "Tag",
        secondary=post_tags,
        back_populates="posts"
    )

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    # Many-to-many relationship with Post
    posts = relationship(
        "Post",
        secondary=post_tags,
        back_populates="tags"
    )

# Usage
# Create post with tags
post = Post(title="Python Tutorial", content="Content")
post.tags = [
    Tag(name="python"),
    Tag(name="tutorial"),
    Tag(name="programming")
]
db.add(post)
db.commit()

# Add existing tags to post
python_tag = db.query(Tag).filter(Tag.name == "python").first()
post.tags.append(python_tag)
db.commit()

# Access tags from post
post = db.query(Post).first()
for tag in post.tags:
    print(tag.name)

# Access posts from tag
tag = db.query(Tag).filter(Tag.name == "python").first()
for post in tag.posts:
    print(post.title)

# Remove tag from post
post.tags.remove(python_tag)
db.commit()

# Advanced: Association object with extra data
from sqlalchemy import DateTime
from datetime import datetime

class PostTag(Base):
    __tablename__ = 'post_tags'

    post_id = Column(Integer, ForeignKey('posts.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)  # Extra data

    # Relationships
    post = relationship("Post", backref="tag_associations")
    tag = relationship("Tag", backref="post_associations")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(200))

    # Access tags through association
    tags = relationship(
        "Tag",
        secondary="post_tags",
        viewonly=True
    )

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

# Usage with association object
post_tag = PostTag(post_id=1, tag_id=1)
db.add(post_tag)
db.commit()
"""
        print(code)

    def demonstrate_one_to_one(self) -> None:
        """Demonstrate one-to-one relationships."""
        print("\nONE-TO-ONE RELATIONSHIPS")
        print("=" * 60)

        code = """
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# One-to-One: User has one Profile
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)

    # One-to-one relationship
    profile = relationship(
        "UserProfile",
        back_populates="user",
        uselist=False,  # Makes it one-to-one
        cascade="all, delete-orphan"
    )

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    bio = Column(String(500))
    avatar_url = Column(String(200))

    # One-to-one relationship
    user = relationship("User", back_populates="profile")

# Usage
# Create user with profile
user = User(username="john")
user.profile = UserProfile(bio="Software developer", avatar_url="avatar.jpg")
db.add(user)
db.commit()

# Access profile from user
user = db.query(User).first()
print(user.profile.bio)

# Access user from profile
profile = db.query(UserProfile).first()
print(profile.user.username)
"""
        print(code)

    def demonstrate_relationship_configuration(self) -> None:
        """Demonstrate relationship configuration options."""
        print("\nRELATIONSHIP CONFIGURATION")
        print("=" * 60)

        code = """
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    # Cascade options
    posts = relationship(
        "Post",
        back_populates="author",
        cascade="all, delete-orphan",  # Delete posts when user deleted
        # cascade="all"  # Also delete but keep orphans
        # cascade="save-update, merge"  # Default
        # cascade="delete"  # Only delete
        passive_deletes=True  # Use database ON DELETE CASCADE
    )

    # Lazy loading options
    posts_lazy = relationship(
        "Post",
        lazy="select"  # Default: load on access
        # lazy="joined"  # Load with JOIN in same query
        # lazy="subquery"  # Load with subquery
        # lazy="selectin"  # Load with SELECT IN
        # lazy="dynamic"  # Return Query object (for filtering)
        # lazy="raise"  # Raise error if accessed (prevents N+1)
        # lazy="noload"  # Never load
    )

    # Order by
    posts_ordered = relationship(
        "Post",
        order_by="Post.created_at.desc()"
    )

    # Filter
    published_posts = relationship(
        "Post",
        primaryjoin="and_(User.id==Post.author_id, Post.published==True)"
    )

    # Foreign keys (explicit)
    posts_explicit = relationship(
        "Post",
        foreign_keys="[Post.author_id]"
    )

    # Remote side (for self-referential)
    parent_id = Column(Integer, ForeignKey("users.id"))
    children = relationship(
        "User",
        backref=backref("parent", remote_side=[id])
    )

# Bidirectional with different names
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship(
        "User",
        backref="authored_posts"
    )

# Join conditions
class Post(Base):
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer)

    author = relationship(
        "User",
        primaryjoin="Post.author_id==User.id",
        foreign_keys="[Post.author_id]"
    )
"""
        print(code)

    def demonstrate_joins(self) -> None:
        """Demonstrate joins and eager loading."""
        print("\nJOINS AND EAGER LOADING")
        print("=" * 60)

        code = """
from sqlalchemy.orm import joinedload, selectinload, subqueryload

# N+1 Problem (BAD)
users = db.query(User).all()
for user in users:
    print(user.username)
    for post in user.posts:  # Separate query for each user!
        print(post.title)

# Solution 1: Joined load (uses JOIN)
users = db.query(User).options(joinedload(User.posts)).all()
for user in users:
    for post in user.posts:  # No additional queries
        print(post.title)

# Solution 2: Selectin load (uses SELECT IN)
users = db.query(User).options(selectinload(User.posts)).all()

# Solution 3: Subquery load
users = db.query(User).options(subqueryload(User.posts)).all()

# Nested relationships
users = db.query(User).options(
    joinedload(User.posts).joinedload(Post.comments)
).all()

# Multiple relationships
users = db.query(User).options(
    joinedload(User.posts),
    joinedload(User.profile)
).all()

# Manual joins
from sqlalchemy import join

# Inner join
results = db.query(User, Post).join(Post).all()
for user, post in results:
    print(f"{user.username}: {post.title}")

# Left outer join
results = db.query(User).outerjoin(Post).all()

# Join with filter
results = (
    db.query(User)
    .join(Post)
    .filter(Post.published == True)
    .all()
)

# Multiple joins
results = (
    db.query(User)
    .join(Post)
    .join(Tag, Post.tags)
    .filter(Tag.name == "python")
    .all()
)

# Explicit join condition
results = (
    db.query(User)
    .join(Post, User.id == Post.author_id)
    .all()
)

# Select specific columns
results = (
    db.query(User.username, Post.title)
    .join(Post)
    .all()
)

# Count with join
count = (
    db.query(func.count(Post.id))
    .join(User)
    .filter(User.is_active == True)
    .scalar()
)

# Group by with join
from sqlalchemy import func

results = (
    db.query(
        User.username,
        func.count(Post.id).label('post_count')
    )
    .outerjoin(Post)
    .group_by(User.username)
    .all()
)

for username, count in results:
    print(f"{username}: {count} posts")
"""
        print(code)

    def demonstrate_complex_relationships(self) -> None:
        """Demonstrate complex relationship patterns."""
        print("\nCOMPLEX RELATIONSHIPS")
        print("=" * 60)

        code = """
# Self-referential relationship (Tree structure)
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    parent_id = Column(Integer, ForeignKey("categories.id"))

    # Self-referential relationships
    children = relationship(
        "Category",
        backref=backref("parent", remote_side=[id]),
        cascade="all, delete-orphan"
    )

# Usage
root = Category(name="Electronics")
root.children = [
    Category(name="Computers"),
    Category(name="Phones")
]
db.add(root)
db.commit()

# Many-to-many self-referential (Followers)
followers = Table(
    'followers',
    Base.metadata,
    Column('follower_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('followed_id', Integer, ForeignKey('users.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50))

    # Users this user follows
    following = relationship(
        "User",
        secondary=followers,
        primaryjoin=(id == followers.c.follower_id),
        secondaryjoin=(id == followers.c.followed_id),
        backref="followers"
    )

# Usage
user1 = db.query(User).filter(User.username == "alice").first()
user2 = db.query(User).filter(User.username == "bob").first()

user1.following.append(user2)  # alice follows bob
db.commit()

# Polymorphic relationships (Table inheritance)
class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True)
    type = Column(String(50))
    brand = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'vehicle',
        'polymorphic_on': type
    }

class Car(Vehicle):
    __tablename__ = "cars"

    id = Column(Integer, ForeignKey("vehicles.id"), primary_key=True)
    doors = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'car',
    }

class Motorcycle(Vehicle):
    __tablename__ = "motorcycles"

    id = Column(Integer, ForeignKey("vehicles.id"), primary_key=True)
    engine_cc = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'motorcycle',
    }

# Query returns appropriate subclass
vehicles = db.query(Vehicle).all()
for v in vehicles:
    if isinstance(v, Car):
        print(f"Car with {v.doors} doors")
    elif isinstance(v, Motorcycle):
        print(f"Motorcycle with {v.engine_cc}cc engine")
"""
        print(code)

    def demonstrate_relationship_loading_strategies(self) -> None:
        """Demonstrate loading strategies for relationships."""
        print("\nLOADING STRATEGIES")
        print("=" * 60)

        code = """
from sqlalchemy.orm import (
    joinedload, selectinload, subqueryload,
    lazyload, raiseload, noload
)

# Eager loading (load related data upfront)

# 1. Joined load - uses LEFT OUTER JOIN
users = db.query(User).options(joinedload(User.posts)).all()
# SQL: SELECT * FROM users LEFT OUTER JOIN posts ON ...
# Good for: One-to-one, small one-to-many
# Creates one query but can duplicate parent rows

# 2. Selectin load - uses SELECT IN
users = db.query(User).options(selectinload(User.posts)).all()
# SQL: SELECT * FROM users
#      SELECT * FROM posts WHERE author_id IN (1, 2, 3, ...)
# Good for: One-to-many, many-to-many
# Two queries but no row duplication

# 3. Subquery load - uses subquery
users = db.query(User).options(subqueryload(User.posts)).all()
# SQL: SELECT * FROM users
#      SELECT * FROM posts WHERE author_id IN (SELECT id FROM users)
# Good for: Similar to selectin but for complex queries

# Lazy loading (load on access)

# 4. Lazy load (default) - separate query per parent
users = db.query(User).options(lazyload(User.posts)).all()
for user in users:
    print(user.posts)  # Query executed here
# Can cause N+1 problem

# 5. Raise load - error if accessed
users = db.query(User).options(raiseload(User.posts)).all()
try:
    print(users[0].posts)  # Raises error
except Exception as e:
    print("Cannot access posts")
# Good for: Preventing N+1 in production

# 6. No load - return empty collection
users = db.query(User).options(noload(User.posts)).all()
print(users[0].posts)  # Returns []
# Good for: When you know you don't need the data

# Nested eager loading
users = db.query(User).options(
    joinedload(User.posts).joinedload(Post.comments).joinedload(Comment.author)
).all()

# Mixed strategies
users = db.query(User).options(
    joinedload(User.profile),  # One-to-one: use joined
    selectinload(User.posts)   # One-to-many: use selectin
).all()

# Contains eager - for filtering on relationship
users = (
    db.query(User)
    .join(User.posts)
    .filter(Post.published == True)
    .options(contains_eager(User.posts))
    .all()
)
# Reuses the join for eager loading
"""
        print(code)


def main() -> None:
    """Main entry point demonstrating database relationships."""
    print("\n" + "=" * 60)
    print("PROGRAM 54: DATABASE RELATIONSHIPS")
    print("=" * 60 + "\n")

    demo = DatabaseRelationshipsDemo()

    demo.demonstrate_one_to_many()
    demo.demonstrate_many_to_many()
    demo.demonstrate_one_to_one()
    demo.demonstrate_relationship_configuration()
    demo.demonstrate_joins()
    demo.demonstrate_complex_relationships()
    demo.demonstrate_relationship_loading_strategies()

    print("\n" + "=" * 60)
    print("RELATIONSHIP BEST PRACTICES")
    print("=" * 60)
    print("1. Use appropriate relationship types")
    print("2. Configure cascade options carefully")
    print("3. Avoid N+1 queries with eager loading")
    print("4. Use indexes on foreign keys")
    print("5. Use back_populates for bidirectional")
    print("6. Choose correct loading strategy")
    print("7. Use association objects for extra data")
    print("8. Be careful with circular dependencies")
    print("9. Use lazy='dynamic' for large collections")
    print("10. Test query performance with EXPLAIN")
    print("=" * 60)


if __name__ == "__main__":
    main()
