#!/usr/bin/env python3
"""
Program 42: Requests Library
Demonstrates using the requests library for HTTP operations.

Topics covered:
- GET and POST requests
- Query parameters and request bodies
- Sessions and connection pooling
- Authentication (Basic, Bearer, API keys)
- Error handling and timeouts
- Response handling
"""

from typing import Dict, Optional, Any
import json
from datetime import datetime


# Note: This is a demonstration file showing how to use requests library
# In production, you would import: import requests


class RequestsDemo:
    """Demonstration of requests library usage patterns."""

    def __init__(self, base_url: str = "https://api.example.com"):
        """
        Initialize the requests demo.

        Args:
            base_url: Base URL for API requests
        """
        self.base_url = base_url

    def demonstrate_get_request(self) -> None:
        """Demonstrate GET requests."""
        print("GET REQUESTS")
        print("=" * 60)

        # Simple GET request
        print("\n1. Simple GET Request:")
        print("-" * 60)
        code = """
import requests

response = requests.get('https://api.example.com/users')
print(f"Status: {response.status_code}")
print(f"Body: {response.json()}")
"""
        print(code)

        # GET with query parameters
        print("2. GET with Query Parameters:")
        print("-" * 60)
        code = """
import requests

params = {
    'page': 1,
    'limit': 10,
    'sort': 'created_at',
    'filter': 'active'
}

response = requests.get(
    'https://api.example.com/users',
    params=params
)

# URL: https://api.example.com/users?page=1&limit=10&sort=created_at&filter=active
print(response.url)
print(response.json())
"""
        print(code)

        # GET with headers
        print("3. GET with Custom Headers:")
        print("-" * 60)
        code = """
import requests

headers = {
    'User-Agent': 'MyApp/1.0',
    'Accept': 'application/json',
    'Authorization': 'Bearer eyJhbGc...'
}

response = requests.get(
    'https://api.example.com/users',
    headers=headers
)
"""
        print(code)

    def demonstrate_post_request(self) -> None:
        """Demonstrate POST requests."""
        print("\nPOST REQUESTS")
        print("=" * 60)

        # POST with JSON
        print("\n1. POST with JSON Body:")
        print("-" * 60)
        code = """
import requests

data = {
    'name': 'John Doe',
    'email': 'john@example.com',
    'age': 30
}

response = requests.post(
    'https://api.example.com/users',
    json=data  # Automatically sets Content-Type to application/json
)

print(f"Status: {response.status_code}")
print(f"Created user: {response.json()}")
"""
        print(code)

        # POST with form data
        print("2. POST with Form Data:")
        print("-" * 60)
        code = """
import requests

data = {
    'username': 'johndoe',
    'password': 'secret123'
}

response = requests.post(
    'https://api.example.com/login',
    data=data  # Sends as application/x-www-form-urlencoded
)
"""
        print(code)

        # POST with file upload
        print("3. POST with File Upload:")
        print("-" * 60)
        code = """
import requests

files = {
    'file': open('document.pdf', 'rb'),
    'thumbnail': open('preview.jpg', 'rb')
}

data = {
    'title': 'My Document',
    'description': 'Important file'
}

response = requests.post(
    'https://api.example.com/upload',
    files=files,
    data=data
)
"""
        print(code)

    def demonstrate_other_methods(self) -> None:
        """Demonstrate PUT, PATCH, DELETE methods."""
        print("\nOTHER HTTP METHODS")
        print("=" * 60)

        # PUT request
        print("\n1. PUT Request (Replace resource):")
        print("-" * 60)
        code = """
import requests

data = {
    'name': 'John Doe Updated',
    'email': 'john.updated@example.com',
    'age': 31
}

response = requests.put(
    'https://api.example.com/users/123',
    json=data
)
"""
        print(code)

        # PATCH request
        print("2. PATCH Request (Partial update):")
        print("-" * 60)
        code = """
import requests

data = {
    'email': 'newemail@example.com'  # Only update email
}

response = requests.patch(
    'https://api.example.com/users/123',
    json=data
)
"""
        print(code)

        # DELETE request
        print("3. DELETE Request:")
        print("-" * 60)
        code = """
import requests

response = requests.delete('https://api.example.com/users/123')

if response.status_code == 204:
    print("User deleted successfully")
"""
        print(code)

    def demonstrate_sessions(self) -> None:
        """Demonstrate session usage for connection pooling."""
        print("\nSESSIONS (Connection Pooling)")
        print("=" * 60)

        code = """
import requests

# Sessions maintain cookies and connection pooling
session = requests.Session()

# Set default headers for all requests
session.headers.update({
    'User-Agent': 'MyApp/1.0',
    'Accept': 'application/json'
})

# Login to get session cookie
login_response = session.post(
    'https://api.example.com/login',
    json={'username': 'user', 'password': 'pass'}
)

# Subsequent requests use the same session/cookies
users = session.get('https://api.example.com/users')
profile = session.get('https://api.example.com/profile')

# Logout
session.post('https://api.example.com/logout')
session.close()

# Using context manager (recommended)
with requests.Session() as session:
    response = session.get('https://api.example.com/data')
    # Session automatically closed
"""
        print(code)

    def demonstrate_authentication(self) -> None:
        """Demonstrate various authentication methods."""
        print("\nAUTHENTICATION METHODS")
        print("=" * 60)

        # Basic Auth
        print("\n1. Basic Authentication:")
        print("-" * 60)
        code = """
import requests
from requests.auth import HTTPBasicAuth

# Method 1: Using auth parameter
response = requests.get(
    'https://api.example.com/protected',
    auth=HTTPBasicAuth('username', 'password')
)

# Method 2: Shorthand tuple
response = requests.get(
    'https://api.example.com/protected',
    auth=('username', 'password')
)
"""
        print(code)

        # Bearer Token
        print("2. Bearer Token Authentication:")
        print("-" * 60)
        code = """
import requests

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

headers = {
    'Authorization': f'Bearer {token}'
}

response = requests.get(
    'https://api.example.com/protected',
    headers=headers
)
"""
        print(code)

        # API Key
        print("3. API Key Authentication:")
        print("-" * 60)
        code = """
import requests

# In header
headers = {'X-API-Key': 'your-api-key-here'}
response = requests.get('https://api.example.com/data', headers=headers)

# In query parameter
params = {'api_key': 'your-api-key-here'}
response = requests.get('https://api.example.com/data', params=params)
"""
        print(code)

        # OAuth 2.0
        print("4. OAuth 2.0:")
        print("-" * 60)
        code = """
from requests_oauthlib import OAuth2Session

client_id = 'your-client-id'
client_secret = 'your-client-secret'
redirect_uri = 'https://yourapp.com/callback'

oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)

# Get authorization URL
authorization_url, state = oauth.authorization_url(
    'https://provider.com/oauth/authorize'
)

# After user authorizes, exchange code for token
token = oauth.fetch_token(
    'https://provider.com/oauth/token',
    authorization_response=redirect_response,
    client_secret=client_secret
)

# Make authenticated requests
response = oauth.get('https://api.example.com/user')
"""
        print(code)

    def demonstrate_error_handling(self) -> None:
        """Demonstrate error handling and timeouts."""
        print("\nERROR HANDLING")
        print("=" * 60)

        code = """
import requests
from requests.exceptions import (
    ConnectionError,
    Timeout,
    HTTPError,
    RequestException
)

try:
    # Set timeout (connect timeout, read timeout)
    response = requests.get(
        'https://api.example.com/data',
        timeout=(3, 10)  # 3s to connect, 10s to read
    )

    # Raise exception for 4xx/5xx status codes
    response.raise_for_status()

    # Process successful response
    data = response.json()
    print(f"Success: {data}")

except Timeout:
    print("Request timed out")
except ConnectionError:
    print("Failed to connect to server")
except HTTPError as e:
    print(f"HTTP error occurred: {e}")
    print(f"Status code: {e.response.status_code}")
    print(f"Response body: {e.response.text}")
except RequestException as e:
    print(f"An error occurred: {e}")

# Check status without raising exception
response = requests.get('https://api.example.com/data')
if response.status_code == 200:
    print("Success")
elif response.status_code == 404:
    print("Resource not found")
elif response.status_code >= 500:
    print("Server error")
"""
        print(code)

    def demonstrate_response_handling(self) -> None:
        """Demonstrate response handling."""
        print("\nRESPONSE HANDLING")
        print("=" * 60)

        code = """
import requests

response = requests.get('https://api.example.com/data')

# Status code
print(f"Status: {response.status_code}")
print(f"OK: {response.ok}")  # True if status < 400

# Headers
print(f"Content-Type: {response.headers['Content-Type']}")
print(f"All headers: {response.headers}")

# Response body
print(f"Text: {response.text}")  # Raw text
print(f"JSON: {response.json()}")  # Parse as JSON
print(f"Content: {response.content}")  # Raw bytes

# Cookies
print(f"Cookies: {response.cookies}")

# Encoding
print(f"Encoding: {response.encoding}")
response.encoding = 'utf-8'  # Set encoding

# URL and history (redirects)
print(f"Final URL: {response.url}")
print(f"Redirects: {response.history}")

# Elapsed time
print(f"Response time: {response.elapsed.total_seconds()}s")

# Streaming large responses
with requests.get('https://example.com/large-file', stream=True) as r:
    r.raise_for_status()
    with open('output.bin', 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
"""
        print(code)

    def demonstrate_advanced_features(self) -> None:
        """Demonstrate advanced features."""
        print("\nADVANCED FEATURES")
        print("=" * 60)

        # Retries
        print("\n1. Automatic Retries:")
        print("-" * 60)
        code = """
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()

# Configure retry strategy
retry_strategy = Retry(
    total=3,  # Total number of retries
    backoff_factor=1,  # Wait 1, 2, 4 seconds between retries
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"]
)

adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.mount("http://", adapter)

response = session.get('https://api.example.com/data')
"""
        print(code)

        # Proxies
        print("2. Using Proxies:")
        print("-" * 60)
        code = """
import requests

proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'https://proxy.example.com:8080'
}

response = requests.get('https://api.example.com/data', proxies=proxies)
"""
        print(code)

        # SSL Verification
        print("3. SSL Certificate Verification:")
        print("-" * 60)
        code = """
import requests

# Disable SSL verification (not recommended for production)
response = requests.get('https://api.example.com/data', verify=False)

# Use custom CA bundle
response = requests.get('https://api.example.com/data', verify='/path/to/ca-bundle.crt')

# Client certificates
response = requests.get(
    'https://api.example.com/data',
    cert=('/path/to/client.cert', '/path/to/client.key')
)
"""
        print(code)


def main() -> None:
    """Main entry point demonstrating requests library."""
    print("\n" + "=" * 60)
    print("PROGRAM 42: REQUESTS LIBRARY")
    print("=" * 60 + "\n")

    demo = RequestsDemo()

    demo.demonstrate_get_request()
    demo.demonstrate_post_request()
    demo.demonstrate_other_methods()
    demo.demonstrate_sessions()
    demo.demonstrate_authentication()
    demo.demonstrate_error_handling()
    demo.demonstrate_response_handling()
    demo.demonstrate_advanced_features()

    print("\n" + "=" * 60)
    print("BEST PRACTICES")
    print("=" * 60)
    print("1. Always use timeouts to prevent hanging requests")
    print("2. Use sessions for multiple requests to same host")
    print("3. Handle exceptions properly (Timeout, ConnectionError, etc.)")
    print("4. Use raise_for_status() to catch HTTP errors")
    print("5. Close sessions when done (or use context managers)")
    print("6. Use streaming for large files")
    print("7. Implement retry logic for transient failures")
    print("8. Verify SSL certificates in production")
    print("9. Use connection pooling for better performance")
    print("10. Set appropriate User-Agent headers")
    print("=" * 60)


if __name__ == "__main__":
    main()
