#!/usr/bin/env python3
"""
Program 50: Authorization
Demonstrates authorization patterns including RBAC (Role-Based Access Control),
permissions, and decorators for access control.

Topics covered:
- Role-Based Access Control (RBAC)
- Permission systems
- Authorization decorators
- Resource-based authorization
- Policy-based authorization
- Scope-based access control
"""

from typing import Dict, Any, List, Optional, Set
from enum import Enum


class AuthorizationDemo:
    """Demonstration of authorization patterns."""

    def demonstrate_rbac_basics(self) -> None:
        """Demonstrate Role-Based Access Control basics."""
        print("ROLE-BASED ACCESS CONTROL (RBAC)")
        print("=" * 60)

        code = """
from enum import Enum
from typing import Set

# Define roles
class Role(str, Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    GUEST = "guest"

# Define permissions
class Permission(str, Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN_ACCESS = "admin_access"
    MODERATE = "moderate"

# Role-Permission mapping
ROLE_PERMISSIONS = {
    Role.ADMIN: {
        Permission.READ,
        Permission.WRITE,
        Permission.DELETE,
        Permission.ADMIN_ACCESS,
        Permission.MODERATE
    },
    Role.MODERATOR: {
        Permission.READ,
        Permission.WRITE,
        Permission.MODERATE
    },
    Role.USER: {
        Permission.READ,
        Permission.WRITE
    },
    Role.GUEST: {
        Permission.READ
    }
}

class User:
    def __init__(self, username: str, role: Role):
        self.username = username
        self.role = role

    def has_permission(self, permission: Permission) -> bool:
        '''Check if user has a specific permission.'''
        return permission in ROLE_PERMISSIONS.get(self.role, set())

    def has_any_permission(self, permissions: Set[Permission]) -> bool:
        '''Check if user has any of the specified permissions.'''
        user_permissions = ROLE_PERMISSIONS.get(self.role, set())
        return bool(user_permissions.intersection(permissions))

    def has_all_permissions(self, permissions: Set[Permission]) -> bool:
        '''Check if user has all of the specified permissions.'''
        user_permissions = ROLE_PERMISSIONS.get(self.role, set())
        return permissions.issubset(user_permissions)

# Usage
admin = User("alice", Role.ADMIN)
user = User("bob", Role.USER)
guest = User("charlie", Role.GUEST)

print(admin.has_permission(Permission.DELETE))  # True
print(user.has_permission(Permission.DELETE))   # False
print(guest.has_permission(Permission.READ))    # True
print(guest.has_permission(Permission.WRITE))   # False
"""
        print(code)

    def demonstrate_fastapi_rbac(self) -> None:
        """Demonstrate RBAC in FastAPI."""
        print("\nRBAC IN FASTAPI")
        print("=" * 60)

        code = """
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Set
from enum import Enum

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Roles and Permissions
class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class Permission(str, Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"

ROLE_PERMISSIONS = {
    Role.ADMIN: {Permission.READ, Permission.WRITE, Permission.DELETE},
    Role.USER: {Permission.READ, Permission.WRITE},
    Role.GUEST: {Permission.READ}
}

class User(BaseModel):
    username: str
    role: Role

    def has_permission(self, permission: Permission) -> bool:
        return permission in ROLE_PERMISSIONS.get(self.role, set())

# Dependency to get current user (simplified)
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    # Decode token and get user (simplified)
    return User(username="alice", role=Role.ADMIN)

# Permission checker dependency
class PermissionChecker:
    def __init__(self, required_permission: Permission):
        self.required_permission = required_permission

    def __call__(self, user: User = Depends(get_current_user)) -> User:
        if not user.has_permission(self.required_permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: {self.required_permission} required"
            )
        return user

# Role checker dependency
class RoleChecker:
    def __init__(self, allowed_roles: Set[Role]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)) -> User:
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: role {user.role} not allowed"
            )
        return user

# Use in routes
@app.get("/public")
def public_route():
    return {"message": "Public access"}

@app.get("/items")
def get_items(user: User = Depends(PermissionChecker(Permission.READ))):
    return {"items": []}

@app.post("/items")
def create_item(user: User = Depends(PermissionChecker(Permission.WRITE))):
    return {"message": "Item created"}

@app.delete("/items/{item_id}")
def delete_item(
    item_id: int,
    user: User = Depends(PermissionChecker(Permission.DELETE))
):
    return {"message": f"Item {item_id} deleted"}

@app.get("/admin")
def admin_panel(user: User = Depends(RoleChecker({Role.ADMIN}))):
    return {"message": "Admin panel"}

@app.get("/staff")
def staff_panel(user: User = Depends(RoleChecker({Role.ADMIN, Role.MODERATOR}))):
    return {"message": "Staff panel"}
"""
        print(code)

    def demonstrate_resource_authorization(self) -> None:
        """Demonstrate resource-based authorization."""
        print("\nRESOURCE-BASED AUTHORIZATION")
        print("=" * 60)

        code = """
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    is_published: bool = False

class User(BaseModel):
    id: int
    username: str
    role: str

# Fake database
posts_db = {
    1: Post(id=1, title="Post 1", content="Content", author_id=1, is_published=True),
    2: Post(id=2, title="Post 2", content="Content", author_id=2, is_published=False),
}

def get_current_user() -> User:
    # Simplified - normally decode from token
    return User(id=1, username="alice", role="user")

def get_post(post_id: int) -> Post:
    post = posts_db.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# Authorization functions
def can_view_post(user: User, post: Post) -> bool:
    '''Check if user can view a post.'''
    # Admins can view all posts
    if user.role == "admin":
        return True

    # Users can view published posts
    if post.is_published:
        return True

    # Users can view their own unpublished posts
    if post.author_id == user.id:
        return True

    return False

def can_edit_post(user: User, post: Post) -> bool:
    '''Check if user can edit a post.'''
    # Admins can edit all posts
    if user.role == "admin":
        return True

    # Users can only edit their own posts
    return post.author_id == user.id

def can_delete_post(user: User, post: Post) -> bool:
    '''Check if user can delete a post.'''
    # Only admins or post author can delete
    return user.role == "admin" or post.author_id == user.id

# Routes with resource authorization
@app.get("/posts/{post_id}")
def get_post_route(
    post_id: int,
    user: User = Depends(get_current_user),
    post: Post = Depends(lambda post_id=post_id: get_post(post_id))
):
    if not can_view_post(user, post):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this post"
        )
    return post

@app.put("/posts/{post_id}")
def update_post(
    post_id: int,
    updates: dict,
    user: User = Depends(get_current_user),
    post: Post = Depends(lambda post_id=post_id: get_post(post_id))
):
    if not can_edit_post(user, post):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to edit this post"
        )

    # Update post
    for key, value in updates.items():
        setattr(post, key, value)

    return post

@app.delete("/posts/{post_id}")
def delete_post_route(
    post_id: int,
    user: User = Depends(get_current_user),
    post: Post = Depends(lambda post_id=post_id: get_post(post_id))
):
    if not can_delete_post(user, post):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post"
        )

    del posts_db[post_id]
    return {"message": "Post deleted"}

# Generic resource authorization decorator
class ResourceAuthorizer:
    def __init__(self, authorization_func):
        self.authorization_func = authorization_func

    def __call__(self, user: User, resource: any):
        if not self.authorization_func(user, resource):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this resource"
            )
        return resource
"""
        print(code)

    def demonstrate_policy_authorization(self) -> None:
        """Demonstrate policy-based authorization."""
        print("\nPOLICY-BASED AUTHORIZATION")
        print("=" * 60)

        code = """
from typing import Callable, Dict
from enum import Enum

# Define actions
class Action(str, Enum):
    VIEW = "view"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    PUBLISH = "publish"

# Policy class
class Policy:
    def __init__(self):
        self.rules: Dict[str, Callable] = {}

    def define(self, action: Action, resource_type: str):
        '''Decorator to define a policy rule.'''
        def decorator(func: Callable):
            key = f"{resource_type}:{action}"
            self.rules[key] = func
            return func
        return decorator

    def authorize(
        self,
        user: any,
        action: Action,
        resource_type: str,
        resource: any = None
    ) -> bool:
        '''Check if user is authorized to perform action on resource.'''
        key = f"{resource_type}:{action}"
        rule = self.rules.get(key)

        if not rule:
            return False

        if resource is not None:
            return rule(user, resource)
        else:
            return rule(user)

# Create policy instance
policy = Policy()

# Define policies for posts
@policy.define(Action.VIEW, "post")
def can_view_post(user, post):
    return (
        user.role == "admin" or
        post.is_published or
        post.author_id == user.id
    )

@policy.define(Action.CREATE, "post")
def can_create_post(user):
    return user.role in ["admin", "user"]

@policy.define(Action.UPDATE, "post")
def can_update_post(user, post):
    return user.role == "admin" or post.author_id == user.id

@policy.define(Action.DELETE, "post")
def can_delete_post(user, post):
    return user.role == "admin" or post.author_id == user.id

@policy.define(Action.PUBLISH, "post")
def can_publish_post(user, post):
    return (
        user.role == "admin" or
        (post.author_id == user.id and user.role != "guest")
    )

# Usage in FastAPI
from fastapi import FastAPI, Depends, HTTPException, status

app = FastAPI()

def authorize(action: Action, resource_type: str):
    '''Dependency factory for authorization.'''
    def dependency(
        user=Depends(get_current_user),
        resource=None
    ):
        if not policy.authorize(user, action, resource_type, resource):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not authorized to {action} {resource_type}"
            )
        return user
    return dependency

@app.get("/posts/{post_id}")
def get_post(
    post_id: int,
    post=Depends(get_post),
    user=Depends(authorize(Action.VIEW, "post"))
):
    return post

@app.post("/posts")
def create_post(
    post_data: dict,
    user=Depends(authorize(Action.CREATE, "post"))
):
    return {"message": "Post created"}

@app.put("/posts/{post_id}")
def update_post(
    post_id: int,
    updates: dict,
    post=Depends(get_post),
    user=Depends(authorize(Action.UPDATE, "post"))
):
    return {"message": "Post updated"}

@app.post("/posts/{post_id}/publish")
def publish_post(
    post_id: int,
    post=Depends(get_post),
    user=Depends(authorize(Action.PUBLISH, "post"))
):
    post.is_published = True
    return {"message": "Post published"}
"""
        print(code)

    def demonstrate_scope_authorization(self) -> None:
        """Demonstrate scope-based authorization."""
        print("\nSCOPE-BASED AUTHORIZATION")
        print("=" * 60)

        code = """
from typing import Set
from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from pydantic import BaseModel

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    scopes: Set[str]

def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme)
) -> User:
    '''Get current user and verify required scopes.'''

    # Decode token and get user (simplified)
    user = User(
        username="alice",
        scopes={"users:read", "users:write", "posts:read"}
    )

    # Check if user has required scopes
    for scope in security_scopes.scopes:
        if scope not in user.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required scope: {scope}",
                headers={"WWW-Authenticate": f'Bearer scope="{security_scopes.scope_str}"'}
            )

    return user

# Routes with scope requirements
@app.get("/users")
def get_users(
    user: User = Security(get_current_user, scopes=["users:read"])
):
    return {"users": []}

@app.post("/users")
def create_user(
    user_data: dict,
    user: User = Security(get_current_user, scopes=["users:write"])
):
    return {"message": "User created"}

@app.get("/users/{user_id}")
def get_user(
    user_id: int,
    user: User = Security(get_current_user, scopes=["users:read"])
):
    return {"user_id": user_id}

@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    user: User = Security(get_current_user, scopes=["users:delete"])
):
    return {"message": "User deleted"}

# Multiple scopes (all required)
@app.post("/admin/users")
def admin_create_user(
    user_data: dict,
    user: User = Security(get_current_user, scopes=["users:write", "admin:access"])
):
    return {"message": "Admin user created"}

# OAuth 2.0 scope patterns:
# - Resource:Action (e.g., users:read, posts:write)
# - Hierarchical (e.g., admin:users:write)
# - OpenID Connect (e.g., openid, profile, email)
"""
        print(code)

    def demonstrate_decorators(self) -> None:
        """Demonstrate authorization decorators."""
        print("\nAUTHORIZATION DECORATORS")
        print("=" * 60)

        code = """
from functools import wraps
from fastapi import HTTPException, status

# Role-based decorator
def require_role(*allowed_roles):
    '''Decorator to require specific roles.'''
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, user=None, **kwargs):
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )

            if user.role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Role {user.role} not authorized"
                )

            return await func(*args, user=user, **kwargs)
        return wrapper
    return decorator

# Permission-based decorator
def require_permission(*required_permissions):
    '''Decorator to require specific permissions.'''
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, user=None, **kwargs):
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )

            user_permissions = set(user.permissions)
            missing = set(required_permissions) - user_permissions

            if missing:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Missing permissions: {missing}"
                )

            return await func(*args, user=user, **kwargs)
        return wrapper
    return decorator

# Ownership decorator
def require_ownership(resource_param="resource"):
    '''Decorator to require resource ownership.'''
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, user=None, **kwargs):
            resource = kwargs.get(resource_param)

            if not resource:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Resource not found"
                )

            # Check ownership or admin
            if user.role != "admin" and resource.owner_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to access this resource"
                )

            return await func(*args, user=user, **kwargs)
        return wrapper
    return decorator

# Usage examples
@require_role("admin", "moderator")
async def admin_action(user):
    return {"message": "Admin action performed"}

@require_permission("delete")
async def delete_action(user):
    return {"message": "Delete action performed"}

@require_ownership("post")
async def update_post(user, post):
    return {"message": "Post updated"}
"""
        print(code)


def main() -> None:
    """Main entry point demonstrating authorization."""
    print("\n" + "=" * 60)
    print("PROGRAM 50: AUTHORIZATION")
    print("=" * 60 + "\n")

    demo = AuthorizationDemo()

    demo.demonstrate_rbac_basics()
    demo.demonstrate_fastapi_rbac()
    demo.demonstrate_resource_authorization()
    demo.demonstrate_policy_authorization()
    demo.demonstrate_scope_authorization()
    demo.demonstrate_decorators()

    print("\n" + "=" * 60)
    print("AUTHORIZATION BEST PRACTICES")
    print("=" * 60)
    print("1. Use RBAC for simple permission systems")
    print("2. Implement resource-level authorization")
    print("3. Use policy-based authorization for complex rules")
    print("4. Always check authorization after authentication")
    print("5. Fail securely (deny by default)")
    print("6. Use scopes for OAuth 2.0 APIs")
    print("7. Implement audit logging for access control")
    print("8. Separate authorization logic from business logic")
    print("9. Test authorization rules thoroughly")
    print("10. Document permission requirements clearly")
    print("=" * 60)


if __name__ == "__main__":
    main()
