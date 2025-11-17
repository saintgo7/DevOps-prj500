#!/usr/bin/env python3
"""
Program 41: HTTP Basics
Demonstrates HTTP methods, status codes, headers, and requests.

Topics covered:
- HTTP methods (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)
- HTTP status codes and their meanings
- HTTP headers (request and response)
- HTTP request structure
- HTTP response structure
"""

from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
import json


class HTTPMethod(Enum):
    """Common HTTP methods."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"
    CONNECT = "CONNECT"


class HTTPStatus(Enum):
    """Common HTTP status codes."""
    # 1xx: Informational
    CONTINUE = (100, "Continue")
    SWITCHING_PROTOCOLS = (101, "Switching Protocols")

    # 2xx: Success
    OK = (200, "OK")
    CREATED = (201, "Created")
    ACCEPTED = (202, "Accepted")
    NO_CONTENT = (204, "No Content")

    # 3xx: Redirection
    MOVED_PERMANENTLY = (301, "Moved Permanently")
    FOUND = (302, "Found")
    NOT_MODIFIED = (304, "Not Modified")
    TEMPORARY_REDIRECT = (307, "Temporary Redirect")

    # 4xx: Client Errors
    BAD_REQUEST = (400, "Bad Request")
    UNAUTHORIZED = (401, "Unauthorized")
    FORBIDDEN = (403, "Forbidden")
    NOT_FOUND = (404, "Not Found")
    METHOD_NOT_ALLOWED = (405, "Method Not Allowed")
    CONFLICT = (409, "Conflict")
    UNPROCESSABLE_ENTITY = (422, "Unprocessable Entity")
    TOO_MANY_REQUESTS = (429, "Too Many Requests")

    # 5xx: Server Errors
    INTERNAL_SERVER_ERROR = (500, "Internal Server Error")
    NOT_IMPLEMENTED = (501, "Not Implemented")
    BAD_GATEWAY = (502, "Bad Gateway")
    SERVICE_UNAVAILABLE = (503, "Service Unavailable")
    GATEWAY_TIMEOUT = (504, "Gateway Timeout")


@dataclass
class HTTPHeader:
    """Represents an HTTP header."""
    name: str
    value: str

    def __str__(self) -> str:
        return f"{self.name}: {self.value}"


@dataclass
class HTTPRequest:
    """Represents an HTTP request."""
    method: HTTPMethod
    path: str
    version: str = "HTTP/1.1"
    headers: List[HTTPHeader] = None
    body: Optional[str] = None

    def __post_init__(self):
        if self.headers is None:
            self.headers = []

    def add_header(self, name: str, value: str) -> None:
        """Add a header to the request."""
        self.headers.append(HTTPHeader(name, value))

    def to_string(self) -> str:
        """Convert request to HTTP wire format."""
        lines = [f"{self.method.value} {self.path} {self.version}"]
        lines.extend(str(header) for header in self.headers)
        lines.append("")  # Empty line between headers and body
        if self.body:
            lines.append(self.body)
        return "\n".join(lines)


@dataclass
class HTTPResponse:
    """Represents an HTTP response."""
    status: HTTPStatus
    version: str = "HTTP/1.1"
    headers: List[HTTPHeader] = None
    body: Optional[str] = None

    def __post_init__(self):
        if self.headers is None:
            self.headers = []

    def add_header(self, name: str, value: str) -> None:
        """Add a header to the response."""
        self.headers.append(HTTPHeader(name, value))

    def to_string(self) -> str:
        """Convert response to HTTP wire format."""
        code, message = self.status.value
        lines = [f"{self.version} {code} {message}"]
        lines.extend(str(header) for header in self.headers)
        lines.append("")  # Empty line between headers and body
        if self.body:
            lines.append(self.body)
        return "\n".join(lines)


def demonstrate_http_methods() -> None:
    """Demonstrate different HTTP methods and their use cases."""
    print("HTTP METHODS")
    print("=" * 60)

    methods = {
        HTTPMethod.GET: "Retrieve a resource (idempotent, safe)",
        HTTPMethod.POST: "Create a new resource (not idempotent)",
        HTTPMethod.PUT: "Update/replace a resource (idempotent)",
        HTTPMethod.DELETE: "Delete a resource (idempotent)",
        HTTPMethod.PATCH: "Partially update a resource",
        HTTPMethod.HEAD: "Same as GET but no response body",
        HTTPMethod.OPTIONS: "Get allowed methods for a resource",
    }

    for method, description in methods.items():
        print(f"{method.value:8} - {description}")
    print()


def demonstrate_status_codes() -> None:
    """Demonstrate HTTP status codes by category."""
    print("HTTP STATUS CODES")
    print("=" * 60)

    categories = {
        "1xx - Informational": [
            HTTPStatus.CONTINUE,
            HTTPStatus.SWITCHING_PROTOCOLS,
        ],
        "2xx - Success": [
            HTTPStatus.OK,
            HTTPStatus.CREATED,
            HTTPStatus.ACCEPTED,
            HTTPStatus.NO_CONTENT,
        ],
        "3xx - Redirection": [
            HTTPStatus.MOVED_PERMANENTLY,
            HTTPStatus.FOUND,
            HTTPStatus.NOT_MODIFIED,
        ],
        "4xx - Client Errors": [
            HTTPStatus.BAD_REQUEST,
            HTTPStatus.UNAUTHORIZED,
            HTTPStatus.FORBIDDEN,
            HTTPStatus.NOT_FOUND,
            HTTPStatus.METHOD_NOT_ALLOWED,
        ],
        "5xx - Server Errors": [
            HTTPStatus.INTERNAL_SERVER_ERROR,
            HTTPStatus.BAD_GATEWAY,
            HTTPStatus.SERVICE_UNAVAILABLE,
        ],
    }

    for category, statuses in categories.items():
        print(f"\n{category}")
        print("-" * 60)
        for status in statuses:
            code, message = status.value
            print(f"  {code} {message}")
    print()


def demonstrate_common_headers() -> None:
    """Demonstrate common HTTP headers."""
    print("COMMON HTTP HEADERS")
    print("=" * 60)

    print("\nRequest Headers:")
    print("-" * 60)
    request_headers = {
        "Host": "api.example.com",
        "User-Agent": "Mozilla/5.0 (Python/3.11)",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "Content-Length": "123",
        "Authorization": "Bearer eyJhbGc...",
        "Cookie": "session_id=abc123",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
    }

    for name, value in request_headers.items():
        print(f"  {name}: {value}")

    print("\nResponse Headers:")
    print("-" * 60)
    response_headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Content-Length": "456",
        "Content-Encoding": "gzip",
        "Date": "Mon, 17 Nov 2025 12:00:00 GMT",
        "Server": "nginx/1.21.0",
        "Cache-Control": "max-age=3600, public",
        "ETag": '"33a64df551425fcc55e4d42a148795d9f25f89d4"',
        "Last-Modified": "Mon, 17 Nov 2025 11:00:00 GMT",
        "Set-Cookie": "session_id=xyz789; HttpOnly; Secure",
        "Access-Control-Allow-Origin": "*",
        "X-RateLimit-Limit": "100",
        "X-RateLimit-Remaining": "99",
    }

    for name, value in response_headers.items():
        print(f"  {name}: {value}")
    print()


def demonstrate_http_request() -> None:
    """Demonstrate building an HTTP request."""
    print("HTTP REQUEST EXAMPLE")
    print("=" * 60)

    # GET request
    print("\n1. Simple GET Request:")
    print("-" * 60)
    get_request = HTTPRequest(
        method=HTTPMethod.GET,
        path="/api/users/123"
    )
    get_request.add_header("Host", "api.example.com")
    get_request.add_header("Accept", "application/json")
    get_request.add_header("Authorization", "Bearer token123")
    print(get_request.to_string())

    # POST request with body
    print("\n2. POST Request with JSON Body:")
    print("-" * 60)
    body_data = {"name": "John Doe", "email": "john@example.com"}
    body_json = json.dumps(body_data, indent=2)

    post_request = HTTPRequest(
        method=HTTPMethod.POST,
        path="/api/users",
        body=body_json
    )
    post_request.add_header("Host", "api.example.com")
    post_request.add_header("Content-Type", "application/json")
    post_request.add_header("Content-Length", str(len(body_json)))
    print(post_request.to_string())
    print()


def demonstrate_http_response() -> None:
    """Demonstrate building an HTTP response."""
    print("HTTP RESPONSE EXAMPLE")
    print("=" * 60)

    # Success response
    print("\n1. Successful Response (200 OK):")
    print("-" * 60)
    response_data = {
        "id": 123,
        "name": "John Doe",
        "email": "john@example.com",
        "created_at": "2025-11-17T12:00:00Z"
    }
    response_body = json.dumps(response_data, indent=2)

    success_response = HTTPResponse(status=HTTPStatus.OK, body=response_body)
    success_response.add_header("Content-Type", "application/json")
    success_response.add_header("Content-Length", str(len(response_body)))
    success_response.add_header("Date", "Mon, 17 Nov 2025 12:00:00 GMT")
    print(success_response.to_string())

    # Error response
    print("\n2. Error Response (404 Not Found):")
    print("-" * 60)
    error_data = {
        "error": "Not Found",
        "message": "User with ID 999 not found",
        "status": 404
    }
    error_body = json.dumps(error_data, indent=2)

    error_response = HTTPResponse(status=HTTPStatus.NOT_FOUND, body=error_body)
    error_response.add_header("Content-Type", "application/json")
    error_response.add_header("Content-Length", str(len(error_body)))
    print(error_response.to_string())
    print()


def demonstrate_content_negotiation() -> None:
    """Demonstrate content negotiation with Accept headers."""
    print("CONTENT NEGOTIATION")
    print("=" * 60)

    content_types = {
        "application/json": "JSON format for APIs",
        "application/xml": "XML format for legacy systems",
        "text/html": "HTML for browser rendering",
        "text/plain": "Plain text for simple responses",
        "application/pdf": "PDF for document downloads",
        "image/jpeg": "JPEG images",
        "multipart/form-data": "Form data with file uploads",
    }

    print("\nCommon Content-Type values:")
    for content_type, description in content_types.items():
        print(f"  {content_type:25} - {description}")

    print("\nAccept Header Examples:")
    print("  Accept: application/json")
    print("  Accept: text/html,application/xhtml+xml")
    print("  Accept: */*  (accepts any content type)")
    print("  Accept: application/json; q=0.9, text/plain; q=0.8")
    print()


def main() -> None:
    """Main entry point demonstrating HTTP basics."""
    print("\n" + "=" * 60)
    print("PROGRAM 41: HTTP BASICS")
    print("=" * 60 + "\n")

    demonstrate_http_methods()
    demonstrate_status_codes()
    demonstrate_common_headers()
    demonstrate_http_request()
    demonstrate_http_response()
    demonstrate_content_negotiation()

    print("=" * 60)
    print("HTTP BEST PRACTICES")
    print("=" * 60)
    print("1. Use appropriate HTTP methods for operations")
    print("2. Return correct status codes for responses")
    print("3. Include proper headers (Content-Type, etc.)")
    print("4. Use HTTPS for secure communication")
    print("5. Implement proper error handling")
    print("6. Follow REST principles for APIs")
    print("7. Use compression (gzip) for large responses")
    print("8. Implement caching where appropriate")
    print("9. Set proper CORS headers for cross-origin requests")
    print("10. Version your APIs")
    print("=" * 60)


if __name__ == "__main__":
    main()
