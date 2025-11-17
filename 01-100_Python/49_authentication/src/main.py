#!/usr/bin/env python3
"""
Program 49: Authentication
Demonstrates authentication mechanisms including JWT, sessions,
password hashing, and OAuth basics.

Topics covered:
- Password hashing with bcrypt
- JWT token generation and validation
- Session-based authentication
- OAuth 2.0 basics
- API key authentication
- Bearer token authentication
"""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta


class AuthenticationDemo:
    """Demonstration of authentication patterns."""

    def demonstrate_password_hashing(self) -> None:
        """Demonstrate password hashing with bcrypt."""
        print("PASSWORD HASHING")
        print("=" * 60)

        code = """
import bcrypt

# Hash a password
password = "mysecretpassword"
salt = bcrypt.gensalt()  # Generate salt
hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
print(f"Hashed: {hashed}")

# Verify password
def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    '''Verify a password against its hash.'''
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password
    )

# Check password
is_valid = verify_password("mysecretpassword", hashed)
print(f"Valid: {is_valid}")  # True

is_valid = verify_password("wrongpassword", hashed)
print(f"Valid: {is_valid}")  # False

# Using with user model
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    hashed_password: str

def create_user(username: str, email: str, password: str) -> User:
    '''Create user with hashed password.'''
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return User(
        username=username,
        email=email,
        hashed_password=hashed.decode('utf-8')
    )

def authenticate_user(username: str, password: str, user: User) -> bool:
    '''Authenticate user with password.'''
    return bcrypt.checkpw(
        password.encode('utf-8'),
        user.hashed_password.encode('utf-8')
    )

# Alternative: passlib (more flexible)
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

hashed = hash_password("mysecretpassword")
print(verify_password("mysecretpassword", hashed))  # True
"""
        print(code)

    def demonstrate_jwt_tokens(self) -> None:
        """Demonstrate JWT token generation and validation."""
        print("\nJWT TOKENS")
        print("=" * 60)

        code = """
import jwt
from datetime import datetime, timedelta
from typing import Optional

# Secret key (should be in environment variables)
SECRET_KEY = "your-secret-key-keep-it-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    '''Create JWT access token.'''
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    '''Verify and decode JWT token.'''
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None

# Create token
access_token = create_access_token(
    data={"sub": "user@example.com", "role": "admin"},
    expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
)
print(f"Token: {access_token}")

# Verify token
payload = verify_token(access_token)
if payload:
    print(f"User: {payload.get('sub')}")
    print(f"Role: {payload.get('role')}")
    print(f"Expires: {payload.get('exp')}")

# Refresh token pattern
def create_refresh_token(data: dict):
    '''Create long-lived refresh token.'''
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Token pair
def create_token_pair(user_email: str):
    '''Create access and refresh token pair.'''
    access_token = create_access_token(
        data={"sub": user_email, "type": "access"}
    )
    refresh_token = create_refresh_token(
        data={"sub": user_email}
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

tokens = create_token_pair("user@example.com")
print(f"Access token: {tokens['access_token']}")
print(f"Refresh token: {tokens['refresh_token']}")
"""
        print(code)

    def demonstrate_fastapi_auth(self) -> None:
        """Demonstrate authentication in FastAPI."""
        print("\nFASTAPI AUTHENTICATION")
        print("=" * 60)

        code = """
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

app = FastAPI()

# Configuration
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Models
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Fake database
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": pwd_context.hash("secret"),
        "disabled": False,
    }
}

# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependency to get current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception

    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Routes
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

# Protected route
@app.get("/protected")
async def protected_route(current_user: User = Depends(get_current_active_user)):
    return {"message": f"Hello {current_user.username}!"}
"""
        print(code)

    def demonstrate_session_auth(self) -> None:
        """Demonstrate session-based authentication."""
        print("\nSESSION-BASED AUTHENTICATION")
        print("=" * 60)

        code = """
from fastapi import FastAPI, Response, Cookie, HTTPException
from typing import Optional
import secrets

app = FastAPI()

# In-memory session store (use Redis in production)
sessions = {}

class Session:
    def __init__(self, user_id: int, username: str):
        self.session_id = secrets.token_urlsafe(32)
        self.user_id = user_id
        self.username = username
        self.created_at = datetime.utcnow()

    def is_valid(self) -> bool:
        # Check if session is less than 1 hour old
        age = datetime.utcnow() - self.created_at
        return age < timedelta(hours=1)

@app.post("/login")
def login(username: str, password: str, response: Response):
    # Authenticate user (simplified)
    if username == "user" and password == "pass":
        # Create session
        session = Session(user_id=1, username=username)
        sessions[session.session_id] = session

        # Set session cookie
        response.set_cookie(
            key="session_id",
            value=session.session_id,
            httponly=True,  # Prevent JavaScript access
            secure=True,    # HTTPS only
            samesite="lax", # CSRF protection
            max_age=3600    # 1 hour
        )

        return {"message": "Logged in successfully"}

    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/profile")
def get_profile(session_id: Optional[str] = Cookie(None)):
    if not session_id or session_id not in sessions:
        raise HTTPException(status_code=401, detail="Not authenticated")

    session = sessions[session_id]

    if not session.is_valid():
        del sessions[session_id]
        raise HTTPException(status_code=401, detail="Session expired")

    return {
        "user_id": session.user_id,
        "username": session.username
    }

@app.post("/logout")
def logout(response: Response, session_id: Optional[str] = Cookie(None)):
    if session_id and session_id in sessions:
        del sessions[session_id]

    response.delete_cookie("session_id")
    return {"message": "Logged out successfully"}

# Dependency for protected routes
from fastapi import Depends

def get_current_user_session(session_id: Optional[str] = Cookie(None)):
    if not session_id or session_id not in sessions:
        raise HTTPException(status_code=401, detail="Not authenticated")

    session = sessions[session_id]
    if not session.is_valid():
        del sessions[session_id]
        raise HTTPException(status_code=401, detail="Session expired")

    return session

@app.get("/protected")
def protected_route(session: Session = Depends(get_current_user_session)):
    return {"message": f"Hello {session.username}!"}
"""
        print(code)

    def demonstrate_api_key_auth(self) -> None:
        """Demonstrate API key authentication."""
        print("\nAPI KEY AUTHENTICATION")
        print("=" * 60)

        code = """
from fastapi import FastAPI, Security, HTTPException, status
from fastapi.security import APIKeyHeader, APIKeyQuery, APIKeyCookie

app = FastAPI()

# API key configuration
API_KEY = "your-api-key-here"
API_KEY_NAME = "X-API-Key"

# Different ways to receive API key
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_query = APIKeyQuery(name="api_key", auto_error=False)
api_key_cookie = APIKeyCookie(name="api_key", auto_error=False)

def get_api_key(
    api_key_header: str = Security(api_key_header),
    api_key_query: str = Security(api_key_query),
    api_key_cookie: str = Security(api_key_cookie),
):
    '''Validate API key from header, query, or cookie.'''
    if api_key_header == API_KEY:
        return api_key_header
    elif api_key_query == API_KEY:
        return api_key_query
    elif api_key_cookie == API_KEY:
        return api_key_cookie
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key"
        )

# Protected route with API key
@app.get("/protected")
def protected_route(api_key: str = Security(get_api_key)):
    return {"message": "API key valid"}

# Usage:
# curl -H "X-API-Key: your-api-key-here" http://localhost:8000/protected
# curl http://localhost:8000/protected?api_key=your-api-key-here

# Database-backed API keys
from typing import Optional

# Fake API key database
api_keys_db = {
    "key-user1-abc123": {"user_id": 1, "username": "user1", "active": True},
    "key-user2-def456": {"user_id": 2, "username": "user2", "active": True},
}

def validate_api_key(api_key: str = Security(api_key_header)):
    '''Validate API key against database.'''
    if api_key not in api_keys_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )

    key_data = api_keys_db[api_key]
    if not key_data["active"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key is inactive"
        )

    return key_data

@app.get("/user/profile")
def get_profile(key_data: dict = Security(validate_api_key)):
    return {
        "user_id": key_data["user_id"],
        "username": key_data["username"]
    }
"""
        print(code)

    def demonstrate_oauth2_basics(self) -> None:
        """Demonstrate OAuth 2.0 basics."""
        print("\nOAUTH 2.0 BASICS")
        print("=" * 60)

        code = """
# OAuth 2.0 Flow:
# 1. Client requests authorization from user
# 2. User grants authorization
# 3. Client receives authorization code
# 4. Client exchanges code for access token
# 5. Client uses access token to access resources

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import secrets

app = FastAPI()

# OAuth configuration
OAUTH_CLIENT_ID = "your-client-id"
OAUTH_CLIENT_SECRET = "your-client-secret"
OAUTH_REDIRECT_URI = "http://localhost:8000/callback"

# In-memory storage (use database in production)
authorization_codes = {}
access_tokens = {}

class TokenRequest(BaseModel):
    grant_type: str
    code: str
    redirect_uri: str
    client_id: str
    client_secret: str

@app.get("/authorize")
def authorize(
    client_id: str,
    redirect_uri: str,
    response_type: str,
    scope: str = "read"
):
    '''Step 1 & 2: User authorizes application.'''

    # Verify client_id and redirect_uri
    if client_id != OAUTH_CLIENT_ID:
        raise HTTPException(status_code=400, detail="Invalid client_id")

    # Generate authorization code
    auth_code = secrets.token_urlsafe(32)
    authorization_codes[auth_code] = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "user_id": 1  # After user login
    }

    # Redirect to client with code
    return {
        "redirect_url": f"{redirect_uri}?code={auth_code}"
    }

@app.post("/token")
def get_token(request: TokenRequest):
    '''Step 3 & 4: Exchange authorization code for access token.'''

    # Verify authorization code
    if request.code not in authorization_codes:
        raise HTTPException(status_code=400, detail="Invalid code")

    code_data = authorization_codes[request.code]

    # Verify client credentials
    if request.client_id != OAUTH_CLIENT_ID:
        raise HTTPException(status_code=400, detail="Invalid client_id")
    if request.client_secret != OAUTH_CLIENT_SECRET:
        raise HTTPException(status_code=400, detail="Invalid client_secret")
    if request.redirect_uri != code_data["redirect_uri"]:
        raise HTTPException(status_code=400, detail="Invalid redirect_uri")

    # Generate access token
    access_token = secrets.token_urlsafe(32)
    access_tokens[access_token] = {
        "user_id": code_data["user_id"],
        "scope": code_data["scope"],
        "expires_in": 3600
    }

    # Delete authorization code (one-time use)
    del authorization_codes[request.code]

    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": 3600,
        "scope": code_data["scope"]
    }

@app.get("/user")
def get_user(authorization: str):
    '''Step 5: Access protected resource with token.'''

    # Extract token from "Bearer <token>"
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = authorization.split(" ")[1]

    # Verify token
    if token not in access_tokens:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    token_data = access_tokens[token]

    return {
        "user_id": token_data["user_id"],
        "scope": token_data["scope"]
    }

# Using with third-party OAuth providers (Google, GitHub, etc.)
# Use libraries like: authlib, python-social-auth
"""
        print(code)


def main() -> None:
    """Main entry point demonstrating authentication."""
    print("\n" + "=" * 60)
    print("PROGRAM 49: AUTHENTICATION")
    print("=" * 60 + "\n")

    demo = AuthenticationDemo()

    demo.demonstrate_password_hashing()
    demo.demonstrate_jwt_tokens()
    demo.demonstrate_fastapi_auth()
    demo.demonstrate_session_auth()
    demo.demonstrate_api_key_auth()
    demo.demonstrate_oauth2_basics()

    print("\n" + "=" * 60)
    print("AUTHENTICATION BEST PRACTICES")
    print("=" * 60)
    print("1. Always hash passwords (never store plain text)")
    print("2. Use strong hashing algorithms (bcrypt, argon2)")
    print("3. Use HTTPS for all authentication endpoints")
    print("4. Implement rate limiting for login attempts")
    print("5. Use secure, httponly cookies for sessions")
    print("6. Set appropriate token expiration times")
    print("7. Implement token refresh mechanism")
    print("8. Never include sensitive data in JWT payloads")
    print("9. Validate tokens on every request")
    print("10. Use OAuth 2.0 for third-party authentication")
    print("=" * 60)


if __name__ == "__main__":
    main()
