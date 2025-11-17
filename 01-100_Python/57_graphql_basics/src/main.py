#!/usr/bin/env python3
"""
Program 57: GraphQL Basics
Demonstrates GraphQL concepts, queries, and mutations (conceptual demonstration).

Topics covered:
- GraphQL vs REST
- Schema definition
- Queries
- Mutations
- Resolvers
- GraphQL with Python (Strawberry/Graphene)
"""

from typing import Dict, Any, List, Optional


class GraphQLBasicsDemo:
    """Demonstration of GraphQL concepts and patterns."""

    def demonstrate_graphql_vs_rest(self) -> None:
        """Demonstrate differences between GraphQL and REST."""
        print("GRAPHQL VS REST")
        print("=" * 60)

        comparison = """
REST API:
---------
Multiple endpoints for different resources:
  GET /users/1
  GET /users/1/posts
  GET /posts/1/comments

Multiple requests to get related data (N+1 problem):
  1. GET /users/1          -> Get user
  2. GET /users/1/posts    -> Get user's posts
  3. GET /posts/1/comments -> Get post comments

Over-fetching (getting more data than needed):
  GET /users/1 returns:
  {
    "id": 1,
    "name": "John",
    "email": "john@example.com",
    "address": {...},        # Not needed
    "phone": "...",          # Not needed
    "created_at": "...",     # Not needed
    ...
  }

GraphQL:
--------
Single endpoint for all queries:
  POST /graphql

Single request for related data:
  query {
    user(id: 1) {
      name
      email
      posts {
        title
        comments {
          text
          author { name }
        }
      }
    }
  }

No over-fetching (get exactly what you need):
  query {
    user(id: 1) {
      name
      email
    }
  }

  Response:
  {
    "data": {
      "user": {
        "name": "John",
        "email": "john@example.com"
      }
    }
  }

GraphQL Advantages:
- Single endpoint
- Client specifies data needs
- No over/under-fetching
- Strong typing
- Self-documenting
- Real-time subscriptions

REST Advantages:
- Simpler to understand
- Better caching
- Simpler tooling
- Smaller learning curve
- Better for file uploads
"""
        print(comparison)

    def demonstrate_schema_definition(self) -> None:
        """Demonstrate GraphQL schema definition."""
        print("\nGRAPHQL SCHEMA DEFINITION")
        print("=" * 60)

        code = """
# GraphQL Schema Definition Language (SDL)

# Scalar types
scalar Date
scalar DateTime
scalar JSON

# Object types
type User {
  id: ID!              # ! means required
  username: String!
  email: String!
  fullName: String
  age: Int
  isActive: Boolean!
  createdAt: DateTime!
  posts: [Post!]!      # Array of Posts
  profile: UserProfile
}

type UserProfile {
  id: ID!
  bio: String
  avatarUrl: String
  user: User!
}

type Post {
  id: ID!
  title: String!
  content: String!
  published: Boolean!
  author: User!
  comments: [Comment!]!
  tags: [Tag!]!
  createdAt: DateTime!
}

type Comment {
  id: ID!
  text: String!
  author: User!
  post: Post!
  createdAt: DateTime!
}

type Tag {
  id: ID!
  name: String!
  posts: [Post!]!
}

# Input types (for mutations)
input CreateUserInput {
  username: String!
  email: String!
  fullName: String
  password: String!
}

input UpdateUserInput {
  username: String
  email: String
  fullName: String
}

input CreatePostInput {
  title: String!
  content: String!
  published: Boolean
  tagIds: [ID!]
}

# Query type (read operations)
type Query {
  # Get single user
  user(id: ID!): User

  # Get all users
  users(
    limit: Int = 10
    offset: Int = 0
    published: Boolean
  ): [User!]!

  # Search users
  searchUsers(query: String!): [User!]!

  # Get single post
  post(id: ID!): Post

  # Get all posts
  posts(
    authorId: ID
    published: Boolean
    limit: Int
    offset: Int
  ): [Post!]!

  # Current logged-in user
  me: User
}

# Mutation type (write operations)
type Mutation {
  # User mutations
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): Boolean!

  # Post mutations
  createPost(input: CreatePostInput!): Post!
  updatePost(id: ID!, title: String, content: String): Post!
  deletePost(id: ID!): Boolean!
  publishPost(id: ID!): Post!

  # Comment mutations
  addComment(postId: ID!, text: String!): Comment!
  deleteComment(id: ID!): Boolean!
}

# Subscription type (real-time updates)
type Subscription {
  postCreated: Post!
  postUpdated(id: ID!): Post!
  commentAdded(postId: ID!): Comment!
}

# Enums
enum UserRole {
  ADMIN
  MODERATOR
  USER
  GUEST
}

# Interfaces
interface Node {
  id: ID!
  createdAt: DateTime!
}

# Union types
union SearchResult = User | Post | Comment
"""
        print(code)

    def demonstrate_queries(self) -> None:
        """Demonstrate GraphQL queries."""
        print("\nGRAPHQL QUERIES")
        print("=" * 60)

        code = """
# Simple query
query {
  user(id: "1") {
    id
    username
    email
  }
}

# Query with variables
query GetUser($userId: ID!) {
  user(id: $userId) {
    id
    username
    email
  }
}

# Variables:
# {
#   "userId": "1"
# }

# Nested query
query {
  user(id: "1") {
    id
    username
    posts {
      id
      title
      comments {
        id
        text
        author {
          username
        }
      }
    }
  }
}

# Multiple queries in one request
query {
  user1: user(id: "1") {
    username
    email
  }

  user2: user(id: "2") {
    username
    email
  }

  posts {
    title
    author {
      username
    }
  }
}

# Query with fragments
query {
  user(id: "1") {
    ...UserFields
    posts {
      ...PostFields
    }
  }
}

fragment UserFields on User {
  id
  username
  email
  createdAt
}

fragment PostFields on Post {
  id
  title
  content
  published
}

# Query with directives
query GetUser($userId: ID!, $withPosts: Boolean!) {
  user(id: $userId) {
    id
    username
    posts @include(if: $withPosts) {
      title
    }
  }
}

# Pagination
query {
  posts(limit: 10, offset: 20) {
    id
    title
    author {
      username
    }
  }
}

# Filtering
query {
  posts(authorId: "1", published: true) {
    id
    title
    createdAt
  }
}

# Search
query {
  searchUsers(query: "john") {
    id
    username
    email
  }
}
"""
        print(code)

    def demonstrate_mutations(self) -> None:
        """Demonstrate GraphQL mutations."""
        print("\nGRAPHQL MUTATIONS")
        print("=" * 60)

        code = """
# Create mutation
mutation {
  createUser(input: {
    username: "johndoe"
    email: "john@example.com"
    fullName: "John Doe"
    password: "secret123"
  }) {
    id
    username
    email
    createdAt
  }
}

# Update mutation
mutation {
  updateUser(
    id: "1"
    input: {
      fullName: "John Updated Doe"
      email: "newemail@example.com"
    }
  ) {
    id
    username
    fullName
    email
  }
}

# Delete mutation
mutation {
  deleteUser(id: "1")
}

# Create with variables
mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    id
    title
    content
    author {
      username
    }
  }
}

# Variables:
# {
#   "input": {
#     "title": "My Post",
#     "content": "Post content",
#     "published": true,
#     "tagIds": ["1", "2"]
#   }
# }

# Multiple mutations
mutation {
  createPost(input: {
    title: "First Post"
    content: "Content"
  }) {
    id
  }

  createComment(postId: "1", text: "Great post!") {
    id
  }
}

# Mutation with return data
mutation {
  publishPost(id: "1") {
    id
    title
    published
    createdAt
  }
}
"""
        print(code)

    def demonstrate_python_graphql(self) -> None:
        """Demonstrate GraphQL with Python (Strawberry)."""
        print("\nGRAPHQL WITH PYTHON (STRAWBERRY)")
        print("=" * 60)

        code = """
# Using Strawberry GraphQL with FastAPI
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional
from datetime import datetime

# Define types
@strawberry.type
class User:
    id: strawberry.ID
    username: str
    email: str
    full_name: Optional[str] = None
    created_at: datetime

@strawberry.type
class Post:
    id: strawberry.ID
    title: str
    content: str
    published: bool
    author_id: strawberry.ID
    created_at: datetime

    @strawberry.field
    def author(self) -> User:
        # Resolver for author field
        return get_user(self.author_id)

# Input types
@strawberry.input
class CreateUserInput:
    username: str
    email: str
    full_name: Optional[str] = None
    password: str

@strawberry.input
class CreatePostInput:
    title: str
    content: str
    published: bool = False

# Fake database
users_db = {}
posts_db = {}

# Resolvers
def get_user(user_id: str) -> Optional[User]:
    return users_db.get(user_id)

def get_all_users() -> List[User]:
    return list(users_db.values())

def get_post(post_id: str) -> Optional[Post]:
    return posts_db.get(post_id)

def get_all_posts(published: Optional[bool] = None) -> List[Post]:
    posts = list(posts_db.values())
    if published is not None:
        posts = [p for p in posts if p.published == published]
    return posts

# Query type
@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: strawberry.ID) -> Optional[User]:
        return get_user(id)

    @strawberry.field
    def users(self) -> List[User]:
        return get_all_users()

    @strawberry.field
    def post(self, id: strawberry.ID) -> Optional[Post]:
        return get_post(id)

    @strawberry.field
    def posts(self, published: Optional[bool] = None) -> List[Post]:
        return get_all_posts(published)

# Mutation type
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, input: CreateUserInput) -> User:
        user_id = str(len(users_db) + 1)
        user = User(
            id=strawberry.ID(user_id),
            username=input.username,
            email=input.email,
            full_name=input.full_name,
            created_at=datetime.now()
        )
        users_db[user_id] = user
        return user

    @strawberry.mutation
    def create_post(self, input: CreatePostInput, author_id: strawberry.ID) -> Post:
        post_id = str(len(posts_db) + 1)
        post = Post(
            id=strawberry.ID(post_id),
            title=input.title,
            content=input.content,
            published=input.published,
            author_id=author_id,
            created_at=datetime.now()
        )
        posts_db[post_id] = post
        return post

    @strawberry.mutation
    def delete_post(self, id: strawberry.ID) -> bool:
        if id in posts_db:
            del posts_db[id]
            return True
        return False

# Create schema
schema = strawberry.Schema(query=Query, mutation=Mutation)

# Integrate with FastAPI
app = FastAPI()
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Access GraphQL playground at: http://localhost:8000/graphql
# Example query:
# {
#   users {
#     id
#     username
#     email
#   }
# }
#
# Example mutation:
# mutation {
#   createUser(input: {
#     username: "john"
#     email: "john@example.com"
#     password: "secret"
#   }) {
#     id
#     username
#   }
# }
"""
        print(code)

    def demonstrate_graphql_patterns(self) -> None:
        """Demonstrate GraphQL patterns and best practices."""
        print("\nGRAPHQL PATTERNS AND BEST PRACTICES")
        print("=" * 60)

        code = """
# 1. DataLoader pattern (solving N+1 queries)
from strawberry.dataloader import DataLoader

async def load_users(keys: List[str]) -> List[User]:
    '''Batch load users by IDs.'''
    # Load all users in one query
    users = await db.query(User).filter(User.id.in_(keys)).all()
    # Return in same order as keys
    user_map = {user.id: user for user in users}
    return [user_map.get(key) for key in keys]

user_loader = DataLoader(load_fn=load_users)

@strawberry.type
class Post:
    id: str
    author_id: str

    @strawberry.field
    async def author(self, info) -> User:
        # Uses DataLoader to batch requests
        return await info.context.user_loader.load(self.author_id)

# 2. Pagination (Relay-style cursor pagination)
@strawberry.type
class PageInfo:
    has_next_page: bool
    has_previous_page: bool
    start_cursor: Optional[str]
    end_cursor: Optional[str]

@strawberry.type
class PostEdge:
    cursor: str
    node: Post

@strawberry.type
class PostConnection:
    edges: List[PostEdge]
    page_info: PageInfo
    total_count: int

@strawberry.type
class Query:
    @strawberry.field
    def posts(
        self,
        first: Optional[int] = None,
        after: Optional[str] = None,
        last: Optional[int] = None,
        before: Optional[str] = None
    ) -> PostConnection:
        # Implement cursor pagination
        pass

# 3. Error handling
@strawberry.type
class Error:
    message: str
    code: str

@strawberry.type
class UserResult:
    user: Optional[User]
    errors: List[Error]

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, input: CreateUserInput) -> UserResult:
        try:
            user = create_user(input)
            return UserResult(user=user, errors=[])
        except ValidationError as e:
            return UserResult(
                user=None,
                errors=[Error(message=str(e), code="VALIDATION_ERROR")]
            )

# 4. Authentication and authorization
from strawberry.permission import BasePermission

class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    def has_permission(self, source, info, **kwargs) -> bool:
        return info.context.user is not None

@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsAuthenticated])
    def me(self, info) -> User:
        return info.context.user

# 5. Subscriptions (real-time updates)
import asyncio
from typing import AsyncGenerator

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def post_created(self) -> AsyncGenerator[Post, None]:
        while True:
            # Wait for new post
            post = await wait_for_new_post()
            yield post

    @strawberry.subscription
    async def comment_added(self, post_id: str) -> AsyncGenerator[Comment, None]:
        async for comment in listen_for_comments(post_id):
            yield comment

# 6. Custom scalars
import strawberry

@strawberry.scalar(
    serialize=lambda v: v.isoformat(),
    parse_value=lambda v: datetime.fromisoformat(v)
)
class DateTime:
    __class__ = datetime

# 7. Interfaces
@strawberry.interface
class Node:
    id: strawberry.ID

@strawberry.type
class User(Node):
    username: str

@strawberry.type
class Post(Node):
    title: str
"""
        print(code)


def main() -> None:
    """Main entry point demonstrating GraphQL basics."""
    print("\n" + "=" * 60)
    print("PROGRAM 57: GRAPHQL BASICS")
    print("=" * 60 + "\n")

    demo = GraphQLBasicsDemo()

    demo.demonstrate_graphql_vs_rest()
    demo.demonstrate_schema_definition()
    demo.demonstrate_queries()
    demo.demonstrate_mutations()
    demo.demonstrate_python_graphql()
    demo.demonstrate_graphql_patterns()

    print("\n" + "=" * 60)
    print("GRAPHQL BEST PRACTICES")
    print("=" * 60)
    print("1. Design schema from client perspective")
    print("2. Use DataLoader to avoid N+1 queries")
    print("3. Implement proper error handling")
    print("4. Use pagination for large datasets")
    print("5. Add authentication and authorization")
    print("6. Version schema carefully (add, don't remove)")
    print("7. Use subscriptions for real-time updates")
    print("8. Implement query depth and complexity limits")
    print("9. Cache responses when possible")
    print("10. Document schema with descriptions")
    print("=" * 60)


if __name__ == "__main__":
    main()
