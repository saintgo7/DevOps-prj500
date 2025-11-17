# Program 88: HTTP Server

Building HTTP servers using http.server and implementing HTTP protocol.

## Description

This program demonstrates creating HTTP servers in Python using built-in modules and understanding HTTP protocol fundamentals. Covers request handling, responses, routing, and web server basics.

## Learning Objectives

- Understand HTTP protocol fundamentals
- Build HTTP servers with Python
- Handle HTTP requests and responses
- Implement request routing
- Serve static files
- Practice web server patterns

## Features

- **HTTP Server**: Built-in http.server module
- **Request Handling**: GET, POST, PUT, DELETE
- **Response Generation**: Status codes, headers, body
- **Static File Serving**: Serve files from directory
- **Routing**: URL pattern matching
- **Headers**: Parse and set HTTP headers
- **Content Types**: Handle different media types
- **Error Handling**: 404, 500, custom error pages

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/088_http_server
python src/main.py

# Access server
curl http://localhost:8000
```

## Key Concepts

### HTTP Request Structure

```
GET /path HTTP/1.1
Host: localhost:8000
User-Agent: curl/7.68.0
Accept: */*

[optional body]
```

### HTTP Response Structure

```
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 42

<html><body>Hello</body></html>
```

### HTTP Status Codes

**Success (2xx):**
- 200 OK
- 201 Created
- 204 No Content

**Redirection (3xx):**
- 301 Moved Permanently
- 302 Found
- 304 Not Modified

**Client Error (4xx):**
- 400 Bad Request
- 401 Unauthorized
- 404 Not Found
- 405 Method Not Allowed

**Server Error (5xx):**
- 500 Internal Server Error
- 502 Bad Gateway
- 503 Service Unavailable

### Basic HTTP Server

```python
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<h1>Hello World</h1>')

server = HTTPServer(('localhost', 8000), Handler)
server.serve_forever()
```

### Routing Pattern

```python
def do_GET(self):
    if self.path == '/':
        self.handle_home()
    elif self.path == '/api/data':
        self.handle_api()
    else:
        self.send_error(404)
```

### Content Types

- **text/html**: HTML pages
- **application/json**: JSON data
- **text/plain**: Plain text
- **image/png**: PNG images
- **application/octet-stream**: Binary data

## Best Practices

1. **Use proper status codes**: Match response to situation
2. **Set correct Content-Type**: Browser needs this
3. **Handle all HTTP methods**: GET, POST, etc.
4. **Validate input**: Sanitize paths and parameters
5. **Add security headers**: CORS, CSP, etc.
6. **Log requests**: Track access and errors
7. **Handle errors gracefully**: Don't expose stack traces
8. **Use frameworks for production**: Flask, FastAPI, Django

## Testing

```bash
# Run tests
pytest tests/

# Manual testing
# Start server
python src/main.py

# Test with curl
curl http://localhost:8000/
curl -X POST http://localhost:8000/api/data
curl -I http://localhost:8000/  # Headers only

# Test with browser
# Open http://localhost:8000 in browser

# Load testing
ab -n 1000 -c 10 http://localhost:8000/
```

## Navigation

- **Previous**: [Program 87 - TCP/UDP](../087_tcp_udp/README.md)
- **Next**: [Program 89 - Threading Advanced](../089_threading_advanced/README.md)
- **Home**: [Main README](../README.md)
