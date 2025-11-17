#!/usr/bin/env python3
"""
Program 51: Middleware
Demonstrates request/response middleware, CORS handling, and logging.

Topics covered:
- Request/response middleware
- CORS (Cross-Origin Resource Sharing)
- Logging middleware
- Error handling middleware
- Authentication middleware
- Rate limiting middleware
- Request timing middleware
"""

from typing import Dict, Any, Callable
from datetime import datetime
import time


class MiddlewareDemo:
    """Demonstration of middleware patterns."""

    def demonstrate_basic_middleware(self) -> None:
        """Demonstrate basic middleware in FastAPI."""
        print("BASIC MIDDLEWARE")
        print("=" * 60)

        code = """
from fastapi import FastAPI, Request
from time import time

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    '''Middleware to add processing time header.'''
    start_time = time()

    # Process request and get response
    response = await call_next(request)

    # Calculate processing time
    process_time = time() - start_time

    # Add custom header
    response.headers["X-Process-Time"] = str(process_time)

    return response

@app.get("/")
def root():
    return {"message": "Hello"}

# The middleware runs before and after each request
"""
        print(code)

    def demonstrate_logging_middleware(self) -> None:
        """Demonstrate logging middleware."""
        print("\nLOGGING MIDDLEWARE")
        print("=" * 60)

        code = """
from fastapi import FastAPI, Request
import logging
from datetime import datetime
import json

app = FastAPI()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    '''Log all incoming requests and responses.'''

    # Log request
    logger.info(
        f"Request: {request.method} {request.url.path} "
        f"from {request.client.host}"
    )

    # Log request body for POST/PUT/PATCH
    if request.method in ["POST", "PUT", "PATCH"]:
        body = await request.body()
        if body:
            try:
                body_json = json.loads(body)
                logger.info(f"Request body: {body_json}")
            except:
                logger.info(f"Request body: {body[:100]}")  # First 100 chars

    # Process request
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    # Log response
    logger.info(
        f"Response: {response.status_code} "
        f"(processed in {process_time:.3f}s)"
    )

    return response

# Structured logging middleware
@app.middleware("http")
async def structured_logging(request: Request, call_next):
    '''Log requests with structured data.'''

    request_id = str(uuid.uuid4())
    start_time = time.time()

    # Add request ID to request state
    request.state.request_id = request_id

    # Process request
    response = await call_next(request)

    # Calculate duration
    duration = time.time() - start_time

    # Structured log entry
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": request_id,
        "method": request.method,
        "path": request.url.path,
        "query_params": str(request.query_params),
        "client_host": request.client.host,
        "status_code": response.status_code,
        "duration_ms": round(duration * 1000, 2),
        "user_agent": request.headers.get("user-agent", ""),
    }

    logger.info(json.dumps(log_data))

    # Add request ID to response header
    response.headers["X-Request-ID"] = request_id

    return response
"""
        print(code)

    def demonstrate_cors_middleware(self) -> None:
        """Demonstrate CORS middleware."""
        print("\nCORS MIDDLEWARE")
        print("=" * 60)

        code = """
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allowed HTTP methods
    allow_headers=["*"],  # Allowed headers
)

# More restrictive CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://example.com",
        "https://app.example.com",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=3600,  # Cache preflight requests for 1 hour
)

# Custom CORS middleware
from fastapi import Request

@app.middleware("http")
async def custom_cors(request: Request, call_next):
    '''Custom CORS middleware with more control.'''

    # Handle preflight requests
    if request.method == "OPTIONS":
        return Response(
            content="",
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
                "Access-Control-Allow-Headers": "Content-Type, Authorization",
                "Access-Control-Max-Age": "3600",
            }
        )

    # Process request
    response = await call_next(request)

    # Add CORS headers to response
    origin = request.headers.get("origin")
    if origin:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"

    return response

@app.get("/api/data")
def get_data():
    return {"data": "value"}
"""
        print(code)

    def demonstrate_authentication_middleware(self) -> None:
        """Demonstrate authentication middleware."""
        print("\nAUTHENTICATION MIDDLEWARE")
        print("=" * 60)

        code = """
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
import jwt

app = FastAPI()

# Public paths that don't require authentication
PUBLIC_PATHS = ["/", "/login", "/register", "/docs", "/openapi.json"]

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

@app.middleware("http")
async def authenticate_request(request: Request, call_next):
    '''Authenticate requests using JWT tokens.'''

    # Skip authentication for public paths
    if request.url.path in PUBLIC_PATHS:
        return await call_next(request)

    # Get token from Authorization header
    auth_header = request.headers.get("authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Missing or invalid authorization header"}
        )

    token = auth_header.split(" ")[1]

    try:
        # Verify token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Add user info to request state
        request.state.user = payload.get("sub")
        request.state.user_id = payload.get("user_id")

    except jwt.ExpiredSignatureError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Token has expired"}
        )
    except jwt.InvalidTokenError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid token"}
        )

    # Process request
    response = await call_next(request)
    return response

@app.get("/protected")
def protected_route(request: Request):
    # Access user from request state
    user = request.state.user
    return {"message": f"Hello {user}"}
"""
        print(code)

    def demonstrate_error_handling_middleware(self) -> None:
        """Demonstrate error handling middleware."""
        print("\nERROR HANDLING MIDDLEWARE")
        print("=" * 60)

        code = """
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import logging

app = FastAPI()
logger = logging.getLogger(__name__)

@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    '''Catch and handle all exceptions.'''

    try:
        response = await call_next(request)
        return response

    except ValueError as e:
        # Handle value errors
        logger.error(f"ValueError: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "Bad Request",
                "message": str(e)
            }
        )

    except PermissionError as e:
        # Handle permission errors
        logger.error(f"PermissionError: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "error": "Forbidden",
                "message": "You don't have permission to access this resource"
            }
        )

    except Exception as e:
        # Handle all other exceptions
        logger.exception(f"Unhandled exception: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred"
            }
        )

# Custom exception handler
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    '''Handle validation errors.'''
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "details": exc.errors()
        }
    )

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    '''Handle 404 errors.'''
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Not Found",
            "message": f"Path {request.url.path} not found"
        }
    )
"""
        print(code)

    def demonstrate_rate_limiting_middleware(self) -> None:
        """Demonstrate rate limiting middleware."""
        print("\nRATE LIMITING MIDDLEWARE")
        print("=" * 60)

        code = """
from fastapi import FastAPI, Request, HTTPException, status
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List

app = FastAPI()

# Rate limit storage (use Redis in production)
rate_limit_storage: Dict[str, List[datetime]] = defaultdict(list)

# Rate limit configuration
RATE_LIMIT_REQUESTS = 10
RATE_LIMIT_WINDOW = 60  # seconds

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    '''Rate limit requests by IP address.'''

    client_ip = request.client.host
    now = datetime.now()

    # Get request timestamps for this IP
    timestamps = rate_limit_storage[client_ip]

    # Remove old timestamps outside the window
    cutoff = now - timedelta(seconds=RATE_LIMIT_WINDOW)
    timestamps = [ts for ts in timestamps if ts > cutoff]
    rate_limit_storage[client_ip] = timestamps

    # Check rate limit
    if len(timestamps) >= RATE_LIMIT_REQUESTS:
        # Calculate retry-after time
        oldest = min(timestamps)
        retry_after = int((oldest + timedelta(seconds=RATE_LIMIT_WINDOW) - now).total_seconds())

        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "error": "Too Many Requests",
                "message": f"Rate limit exceeded. Try again in {retry_after} seconds."
            },
            headers={
                "Retry-After": str(retry_after),
                "X-RateLimit-Limit": str(RATE_LIMIT_REQUESTS),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(int((oldest + timedelta(seconds=RATE_LIMIT_WINDOW)).timestamp()))
            }
        )

    # Add current request timestamp
    timestamps.append(now)

    # Process request
    response = await call_next(request)

    # Add rate limit headers to response
    remaining = RATE_LIMIT_REQUESTS - len(timestamps)
    response.headers["X-RateLimit-Limit"] = str(RATE_LIMIT_REQUESTS)
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    response.headers["X-RateLimit-Reset"] = str(int((now + timedelta(seconds=RATE_LIMIT_WINDOW)).timestamp()))

    return response

# Token bucket rate limiting
class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = datetime.now()

    def consume(self, tokens: int = 1) -> bool:
        '''Try to consume tokens. Returns True if successful.'''
        self._refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def _refill(self):
        '''Refill tokens based on time elapsed.'''
        now = datetime.now()
        elapsed = (now - self.last_refill).total_seconds()
        tokens_to_add = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now

# Use token bucket
buckets: Dict[str, TokenBucket] = {}

@app.middleware("http")
async def token_bucket_middleware(request: Request, call_next):
    client_ip = request.client.host

    if client_ip not in buckets:
        buckets[client_ip] = TokenBucket(capacity=10, refill_rate=1.0)  # 1 token/second

    if not buckets[client_ip].consume():
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"error": "Rate limit exceeded"}
        )

    return await call_next(request)
"""
        print(code)

    def demonstrate_request_id_middleware(self) -> None:
        """Demonstrate request ID middleware."""
        print("\nREQUEST ID MIDDLEWARE")
        print("=" * 60)

        code = """
from fastapi import FastAPI, Request
import uuid

app = FastAPI()

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    '''Add unique request ID to each request.'''

    # Check if request already has an ID (from load balancer, etc.)
    request_id = request.headers.get("X-Request-ID")

    if not request_id:
        request_id = str(uuid.uuid4())

    # Add to request state for use in route handlers
    request.state.request_id = request_id

    # Process request
    response = await call_next(request)

    # Add request ID to response headers
    response.headers["X-Request-ID"] = request_id

    return response

@app.get("/test")
def test_route(request: Request):
    # Access request ID from request state
    request_id = request.state.request_id
    return {"request_id": request_id, "message": "Test"}
"""
        print(code)

    def demonstrate_compression_middleware(self) -> None:
        """Demonstrate compression middleware."""
        print("\nCOMPRESSION MIDDLEWARE")
        print("=" * 60)

        code = """
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()

# Add gzip compression middleware
app.add_middleware(
    GZipMiddleware,
    minimum_size=1000  # Only compress responses larger than 1000 bytes
)

@app.get("/large-data")
def get_large_data():
    # Response will be automatically compressed if > 1000 bytes
    return {"data": "x" * 10000}

# Custom compression middleware
from fastapi import Request, Response
import gzip

@app.middleware("http")
async def custom_gzip_middleware(request: Request, call_next):
    '''Custom gzip compression middleware.'''

    response = await call_next(request)

    # Check if client accepts gzip
    accept_encoding = request.headers.get("accept-encoding", "")
    if "gzip" not in accept_encoding:
        return response

    # Check content type (only compress text-based responses)
    content_type = response.headers.get("content-type", "")
    if not any(t in content_type for t in ["text/", "application/json", "application/xml"]):
        return response

    # Get response body
    body = b""
    async for chunk in response.body_iterator:
        body += chunk

    # Compress if large enough
    if len(body) > 1000:
        compressed_body = gzip.compress(body)

        return Response(
            content=compressed_body,
            status_code=response.status_code,
            headers={
                **dict(response.headers),
                "content-encoding": "gzip",
                "content-length": str(len(compressed_body))
            }
        )

    return Response(
        content=body,
        status_code=response.status_code,
        headers=dict(response.headers)
    )
"""
        print(code)

    def demonstrate_middleware_order(self) -> None:
        """Demonstrate middleware execution order."""
        print("\nMIDDLEWARE EXECUTION ORDER")
        print("=" * 60)

        code = """
from fastapi import FastAPI, Request

app = FastAPI()

# Middleware execution order:
# 1. First middleware added (outermost)
# 2. Second middleware added
# 3. Last middleware added (innermost)
# 4. Route handler
# 5. Last middleware (response)
# 6. Second middleware (response)
# 7. First middleware (response)

@app.middleware("http")
async def first_middleware(request: Request, call_next):
    print("First middleware - before request")
    response = await call_next(request)
    print("First middleware - after request")
    return response

@app.middleware("http")
async def second_middleware(request: Request, call_next):
    print("Second middleware - before request")
    response = await call_next(request)
    print("Second middleware - after request")
    return response

@app.middleware("http")
async def third_middleware(request: Request, call_next):
    print("Third middleware - before request")
    response = await call_next(request)
    print("Third middleware - after request")
    return response

@app.get("/test")
def test_route():
    print("Route handler")
    return {"message": "Test"}

# Output when accessing /test:
# First middleware - before request
# Second middleware - before request
# Third middleware - before request
# Route handler
# Third middleware - after request
# Second middleware - after request
# First middleware - after request

# Best practice: Add middleware in order of priority
# 1. CORS (must be first)
# 2. Error handling
# 3. Logging
# 4. Authentication
# 5. Rate limiting
# 6. Request ID
# 7. Compression (should be last)
"""
        print(code)


def main() -> None:
    """Main entry point demonstrating middleware."""
    print("\n" + "=" * 60)
    print("PROGRAM 51: MIDDLEWARE")
    print("=" * 60 + "\n")

    demo = MiddlewareDemo()

    demo.demonstrate_basic_middleware()
    demo.demonstrate_logging_middleware()
    demo.demonstrate_cors_middleware()
    demo.demonstrate_authentication_middleware()
    demo.demonstrate_error_handling_middleware()
    demo.demonstrate_rate_limiting_middleware()
    demo.demonstrate_request_id_middleware()
    demo.demonstrate_compression_middleware()
    demo.demonstrate_middleware_order()

    print("\n" + "=" * 60)
    print("MIDDLEWARE BEST PRACTICES")
    print("=" * 60)
    print("1. Add middleware in correct order (CORS first)")
    print("2. Handle errors gracefully in middleware")
    print("3. Use middleware for cross-cutting concerns")
    print("4. Log important events (requests, errors)")
    print("5. Implement rate limiting to prevent abuse")
    print("6. Add request IDs for tracking")
    print("7. Use compression for large responses")
    print("8. Keep middleware lightweight and fast")
    print("9. Use dependency injection when possible")
    print("10. Test middleware thoroughly")
    print("=" * 60)


if __name__ == "__main__":
    main()
