#!/usr/bin/env python3
"""
Program 88: HTTP Server
Demonstrates simple HTTP server implementation.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import threading
import time
from typing import Dict, Any
from pathlib import Path
import tempfile


class CustomHTTPHandler(BaseHTTPRequestHandler):
    """Custom HTTP request handler."""

    def log_message(self, format: str, *args) -> None:
        """Override to customize logging."""
        print(f"[{self.address_string()}] {format % args}")

    def do_GET(self) -> None:
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/':
            self._send_home()
        elif path == '/api/data':
            self._send_api_data()
        elif path == '/api/time':
            self._send_time()
        else:
            self._send_404()

    def do_POST(self) -> None:
        """Handle POST requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/api/echo':
            self._handle_echo()
        elif path == '/api/data':
            self._handle_data_post()
        else:
            self._send_404()

    def _send_home(self) -> None:
        """Send home page."""
        html = """
        <!DOCTYPE html>
        <html>
        <head><title>Custom HTTP Server</title></head>
        <body>
            <h1>Welcome to Custom HTTP Server</h1>
            <p>Available endpoints:</p>
            <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/api/data">API Data</a></li>
                <li><a href="/api/time">Current Time</a></li>
            </ul>
        </body>
        </html>
        """
        self._send_response(200, html.encode(), 'text/html')

    def _send_api_data(self) -> None:
        """Send JSON data."""
        data = {
            'status': 'success',
            'data': {
                'items': ['item1', 'item2', 'item3'],
                'count': 3
            }
        }
        self._send_json_response(200, data)

    def _send_time(self) -> None:
        """Send current time."""
        from datetime import datetime
        data = {
            'timestamp': datetime.now().isoformat(),
            'timezone': 'UTC'
        }
        self._send_json_response(200, data)

    def _handle_echo(self) -> None:
        """Echo POST data back."""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')

        response = {
            'echo': body,
            'length': content_length
        }
        self._send_json_response(200, response)

    def _handle_data_post(self) -> None:
        """Handle data POST."""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')

        try:
            data = json.loads(body)
            response = {
                'status': 'received',
                'data': data
            }
            self._send_json_response(200, response)
        except json.JSONDecodeError:
            self._send_json_response(400, {'error': 'Invalid JSON'})

    def _send_404(self) -> None:
        """Send 404 response."""
        html = "<h1>404 Not Found</h1>"
        self._send_response(404, html.encode(), 'text/html')

    def _send_response(self, status: int, body: bytes, content_type: str) -> None:
        """Send HTTP response."""
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json_response(self, status: int, data: Dict[str, Any]) -> None:
        """Send JSON response."""
        body = json.dumps(data, indent=2).encode('utf-8')
        self._send_response(status, body, 'application/json')


def demonstrate_basic_http_server() -> None:
    """Demonstrate basic HTTP server."""
    print("\n" + "=" * 60)
    print("BASIC HTTP SERVER")
    print("=" * 60)

    print("\n1. HTTP server components:")
    print("   - HTTPServer: Server class")
    print("   - BaseHTTPRequestHandler: Request handler")
    print("   - do_GET, do_POST: HTTP methods")

    print("\n2. Server lifecycle:")
    print("   create -> bind -> listen -> serve -> shutdown")


def run_custom_server(port: int, stop_event: threading.Event) -> None:
    """Run custom HTTP server."""
    server = HTTPServer(('127.0.0.1', port), CustomHTTPHandler)
    server.timeout = 1.0

    print(f"[Server] Started on port {port}")

    while not stop_event.is_set():
        server.handle_request()

    server.server_close()
    print("[Server] Stopped")


def demonstrate_custom_server() -> None:
    """Demonstrate custom HTTP server."""
    print("\n" + "=" * 60)
    print("CUSTOM HTTP SERVER")
    print("=" * 60)

    port = 10080
    stop_event = threading.Event()

    print(f"\n1. Starting server on port {port}...")

    server_thread = threading.Thread(
        target=run_custom_server,
        args=(port, stop_event),
        daemon=True
    )
    server_thread.start()
    time.sleep(0.5)

    # Make test requests
    import urllib.request

    print("\n2. Making test requests:")

    try:
        # GET request
        with urllib.request.urlopen(f'http://127.0.0.1:{port}/api/time', timeout=2) as response:
            data = json.loads(response.read())
            print(f"   GET /api/time: {data['timestamp']}")
    except Exception as e:
        print(f"   Error: {e}")

    # Cleanup
    stop_event.set()
    server_thread.join(timeout=2)
    print("\n3. Server stopped")


def demonstrate_simple_http_server() -> None:
    """Demonstrate SimpleHTTPRequestHandler."""
    print("\n" + "=" * 60)
    print("SIMPLE HTTP SERVER")
    print("=" * 60)

    print("\n1. SimpleHTTPRequestHandler:")
    print("   - Serves files from directory")
    print("   - Built-in directory listing")
    print("   - No custom logic needed")

    print("\n2. Usage:")
    print("   server = HTTPServer(addr, SimpleHTTPRequestHandler)")
    print("   server.serve_forever()")

    print("\n3. Command-line:")
    print("   python -m http.server 8000")


def demonstrate_http_methods() -> None:
    """Demonstrate HTTP methods."""
    print("\n" + "=" * 60)
    print("HTTP METHODS")
    print("=" * 60)

    print("\n1. Common HTTP methods:")
    methods = {
        'GET': 'Retrieve resource',
        'POST': 'Create resource',
        'PUT': 'Update resource',
        'DELETE': 'Delete resource',
        'HEAD': 'Get headers only',
        'OPTIONS': 'Get allowed methods',
        'PATCH': 'Partial update'
    }

    for method, description in methods.items():
        print(f"   {method:8} - {description}")

    print("\n2. Implementation:")
    print("   def do_GET(self): ...")
    print("   def do_POST(self): ...")
    print("   def do_PUT(self): ...")


def demonstrate_http_headers() -> None:
    """Demonstrate HTTP headers."""
    print("\n" + "=" * 60)
    print("HTTP HEADERS")
    print("=" * 60)

    print("\n1. Common request headers:")
    print("   - Content-Type")
    print("   - Content-Length")
    print("   - User-Agent")
    print("   - Accept")
    print("   - Authorization")

    print("\n2. Common response headers:")
    print("   - Content-Type")
    print("   - Content-Length")
    print("   - Server")
    print("   - Set-Cookie")
    print("   - Cache-Control")

    print("\n3. Setting headers:")
    print("   self.send_header('Content-Type', 'text/html')")
    print("   self.send_header('Content-Length', '100')")


def demonstrate_status_codes() -> None:
    """Demonstrate HTTP status codes."""
    print("\n" + "=" * 60)
    print("HTTP STATUS CODES")
    print("=" * 60)

    codes = {
        '2xx Success': {
            200: 'OK',
            201: 'Created',
            204: 'No Content'
        },
        '3xx Redirection': {
            301: 'Moved Permanently',
            302: 'Found',
            304: 'Not Modified'
        },
        '4xx Client Error': {
            400: 'Bad Request',
            401: 'Unauthorized',
            404: 'Not Found'
        },
        '5xx Server Error': {
            500: 'Internal Server Error',
            502: 'Bad Gateway',
            503: 'Service Unavailable'
        }
    }

    for category, status_codes in codes.items():
        print(f"\n{category}:")
        for code, description in status_codes.items():
            print(f"   {code} - {description}")


def demonstrate_content_types() -> None:
    """Demonstrate content types."""
    print("\n" + "=" * 60)
    print("CONTENT TYPES")
    print("=" * 60)

    print("\n1. Common MIME types:")
    types = {
        'text/html': 'HTML document',
        'text/plain': 'Plain text',
        'application/json': 'JSON data',
        'application/xml': 'XML data',
        'image/jpeg': 'JPEG image',
        'image/png': 'PNG image',
        'video/mp4': 'MP4 video',
        'application/pdf': 'PDF document'
    }

    for mime_type, description in types.items():
        print(f"   {mime_type:20} - {description}")

    print("\n2. Setting content type:")
    print("   self.send_header('Content-Type', 'application/json')")


def demonstrate_query_parameters() -> None:
    """Demonstrate handling query parameters."""
    print("\n" + "=" * 60)
    print("QUERY PARAMETERS")
    print("=" * 60)

    print("\n1. URL structure:")
    print("   http://host/path?key1=value1&key2=value2")

    print("\n2. Parsing query string:")
    from urllib.parse import urlparse, parse_qs

    url = "http://example.com/api?name=john&age=30"
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    print(f"   URL: {url}")
    print(f"   Path: {parsed.path}")
    print(f"   Params: {params}")


def demonstrate_post_data() -> None:
    """Demonstrate handling POST data."""
    print("\n" + "=" * 60)
    print("POST DATA HANDLING")
    print("=" * 60)

    print("\n1. Reading POST data:")
    print("   content_length = int(self.headers['Content-Length'])")
    print("   body = self.rfile.read(content_length)")

    print("\n2. JSON data:")
    print("   data = json.loads(body)")

    print("\n3. Form data:")
    print("   from urllib.parse import parse_qs")
    print("   data = parse_qs(body.decode())")


def demonstrate_threading_server() -> None:
    """Demonstrate threaded HTTP server."""
    print("\n" + "=" * 60)
    print("THREADED HTTP SERVER")
    print("=" * 60)

    print("\n1. ThreadingHTTPServer:")
    print("   from http.server import ThreadingHTTPServer")
    print("   - Handles each request in separate thread")
    print("   - Better for concurrent requests")

    print("\n2. Usage:")
    print("   server = ThreadingHTTPServer(addr, handler)")
    print("   server.serve_forever()")


def demonstrate_https() -> None:
    """Demonstrate HTTPS concepts."""
    print("\n" + "=" * 60)
    print("HTTPS (Secure HTTP)")
    print("=" * 60)

    print("\n1. HTTPS features:")
    print("   ✓ Encryption (TLS/SSL)")
    print("   ✓ Authentication")
    print("   ✓ Data integrity")

    print("\n2. Setup requires:")
    print("   - SSL certificate")
    print("   - Private key")
    print("   - ssl.wrap_socket()")

    print("\n3. Port conventions:")
    print("   HTTP: 80")
    print("   HTTPS: 443")


def demonstrate_cors() -> None:
    """Demonstrate CORS headers."""
    print("\n" + "=" * 60)
    print("CORS (Cross-Origin Resource Sharing)")
    print("=" * 60)

    print("\n1. CORS headers:")
    print("   Access-Control-Allow-Origin: *")
    print("   Access-Control-Allow-Methods: GET, POST")
    print("   Access-Control-Allow-Headers: Content-Type")

    print("\n2. When needed:")
    print("   - API accessed from different domain")
    print("   - Browser enforces same-origin policy")
    print("   - CORS headers grant permission")


def demonstrate_error_handling() -> None:
    """Demonstrate error handling."""
    print("\n" + "=" * 60)
    print("ERROR HANDLING")
    print("=" * 60)

    print("\n1. Common errors:")
    print("   - Address already in use")
    print("   - Permission denied")
    print("   - Invalid request")

    print("\n2. Handling strategy:")
    print("   try:")
    print("       server.serve_forever()")
    print("   except KeyboardInterrupt:")
    print("       server.shutdown()")
    print("   finally:")
    print("       server.server_close()")


def demonstrate_best_practices() -> None:
    """Demonstrate best practices."""
    print("\n" + "=" * 60)
    print("BEST PRACTICES")
    print("=" * 60)

    print("\n1. Security:")
    print("   ✓ Validate all input")
    print("   ✓ Use HTTPS in production")
    print("   ✓ Implement authentication")
    print("   ✓ Set appropriate CORS headers")

    print("\n2. Performance:")
    print("   ✓ Use threaded server")
    print("   ✓ Implement caching")
    print("   ✓ Compress responses")
    print("   ✓ Set timeouts")

    print("\n3. Development:")
    print("   ✓ Use production-ready servers (gunicorn, uwsgi)")
    print("   ✓ Implement logging")
    print("   ✓ Handle all HTTP methods")
    print("   ✓ Return proper status codes")


def main() -> None:
    """Main function demonstrating HTTP server."""
    print("=" * 60)
    print("PYTHON HTTP SERVER")
    print("=" * 60)

    demonstrate_basic_http_server()
    demonstrate_custom_server()
    demonstrate_simple_http_server()
    demonstrate_http_methods()
    demonstrate_http_headers()
    demonstrate_status_codes()
    demonstrate_content_types()
    demonstrate_query_parameters()
    demonstrate_post_data()
    demonstrate_threading_server()
    demonstrate_https()
    demonstrate_cors()
    demonstrate_error_handling()
    demonstrate_best_practices()

    print("\n" + "=" * 60)
    print("All HTTP server demonstrations completed!")
    print("=" * 60)
    print("\nNote: For production, use frameworks like Flask, Django,")
    print("or servers like gunicorn, uwsgi instead of built-in server.")


if __name__ == "__main__":
    main()
