#!/usr/bin/env python3
"""
Program 43: Flask Basics
Demonstrates Flask application structure, routes, and request/response handling.

Topics covered:
- Creating a Flask application
- Defining routes and view functions
- Request object (accessing data)
- Response object (returning data)
- Request methods (GET, POST)
- JSON responses
"""

from typing import Dict, Any, List, Tuple
import json


class FlaskBasicsDemo:
    """Demonstration of Flask basics and patterns."""

    def demonstrate_basic_app(self) -> None:
        """Demonstrate basic Flask application structure."""
        print("BASIC FLASK APPLICATION")
        print("=" * 60)

        code = """
from flask import Flask

# Create Flask application instance
app = Flask(__name__)

# Define a simple route
@app.route('/')
def home():
    '''Handle requests to the root URL.'''
    return 'Hello, Flask!'

# Define another route
@app.route('/about')
def about():
    return 'This is the about page'

# Run the application
if __name__ == '__main__':
    # Debug mode for development only
    app.run(debug=True, host='0.0.0.0', port=5000)
"""
        print(code)

    def demonstrate_routes(self) -> None:
        """Demonstrate different types of routes."""
        print("\nDEFINING ROUTES")
        print("=" * 60)

        print("\n1. Static Routes:")
        print("-" * 60)
        code = """
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Home Page'

@app.route('/about')
def about():
    return 'About Page'

@app.route('/contact')
def contact():
    return 'Contact Page'
"""
        print(code)

        print("2. Routes with Multiple Endpoints:")
        print("-" * 60)
        code = """
# Multiple URLs for the same function
@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return 'Home Page'
"""
        print(code)

        print("3. Routes with Trailing Slashes:")
        print("-" * 60)
        code = """
# With trailing slash - /about/ redirects to /about
@app.route('/about')
def about():
    return 'About'

# Without trailing slash - /contact redirects to /contact/
@app.route('/contact/')
def contact():
    return 'Contact'
"""
        print(code)

    def demonstrate_request_methods(self) -> None:
        """Demonstrate handling different HTTP methods."""
        print("\nHTTP REQUEST METHODS")
        print("=" * 60)

        code = """
from flask import Flask, request

app = Flask(__name__)

# GET method only (default)
@app.route('/users')
def get_users():
    return {'users': ['Alice', 'Bob', 'Charlie']}

# POST method only
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    return {'message': 'User created', 'data': data}, 201

# Multiple methods in one route
@app.route('/user/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_detail(user_id):
    if request.method == 'GET':
        return {'id': user_id, 'name': 'John Doe'}

    elif request.method == 'PUT':
        data = request.get_json()
        return {'message': 'User updated', 'id': user_id, 'data': data}

    elif request.method == 'DELETE':
        return {'message': 'User deleted', 'id': user_id}

# Separate functions for clarity (recommended)
@app.route('/products', methods=['GET'])
def list_products():
    return {'products': []}

@app.route('/products', methods=['POST'])
def create_product():
    return {'message': 'Product created'}, 201
"""
        print(code)

    def demonstrate_request_object(self) -> None:
        """Demonstrate accessing request data."""
        print("\nREQUEST OBJECT")
        print("=" * 60)

        code = """
from flask import Flask, request

app = Flask(__name__)

@app.route('/demo', methods=['GET', 'POST'])
def request_demo():
    # Request method
    method = request.method

    # URL components
    url = request.url  # Full URL
    path = request.path  # Path only
    base_url = request.base_url

    # Query parameters (?key=value)
    name = request.args.get('name', 'Guest')  # With default
    page = request.args.get('page', type=int)  # With type conversion
    all_args = request.args.to_dict()

    # Form data (application/x-www-form-urlencoded)
    username = request.form.get('username')
    all_form_data = request.form.to_dict()

    # JSON data (application/json)
    json_data = request.get_json()
    # Or with error handling
    json_data = request.get_json(silent=True)

    # Headers
    content_type = request.headers.get('Content-Type')
    auth_header = request.headers.get('Authorization')
    all_headers = dict(request.headers)

    # Cookies
    session_id = request.cookies.get('session_id')

    # Files
    uploaded_file = request.files.get('file')
    if uploaded_file:
        filename = uploaded_file.filename
        uploaded_file.save(f'/uploads/{filename}')

    # Client information
    client_ip = request.remote_addr
    user_agent = request.user_agent.string

    return {
        'method': method,
        'path': path,
        'args': all_args,
        'client_ip': client_ip
    }
"""
        print(code)

    def demonstrate_response_object(self) -> None:
        """Demonstrate creating responses."""
        print("\nRESPONSE OBJECT")
        print("=" * 60)

        code = """
from flask import Flask, jsonify, make_response, redirect, url_for

app = Flask(__name__)

# 1. Simple string response (default: 200 OK)
@app.route('/hello')
def hello():
    return 'Hello, World!'

# 2. String with custom status code
@app.route('/created')
def created():
    return 'Resource created', 201

# 3. JSON response (automatically sets Content-Type)
@app.route('/api/user')
def get_user():
    user = {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'}
    return jsonify(user)

# 4. JSON with status code
@app.route('/api/user', methods=['POST'])
def create_user():
    return jsonify({'message': 'User created'}), 201

# 5. Response with custom headers
@app.route('/custom')
def custom_response():
    response = make_response(jsonify({'data': 'value'}))
    response.headers['X-Custom-Header'] = 'Custom Value'
    response.headers['Cache-Control'] = 'no-cache'
    response.status_code = 200
    return response

# 6. Tuple format (body, status, headers)
@app.route('/tuple')
def tuple_response():
    headers = {'X-Custom': 'Value'}
    return {'data': 'value'}, 200, headers

# 7. Set cookie
@app.route('/login')
def login():
    response = make_response(jsonify({'message': 'Logged in'}))
    response.set_cookie('session_id', 'abc123', max_age=3600, httponly=True)
    return response

# 8. Redirect
@app.route('/old-page')
def old_page():
    return redirect('/new-page')

# Redirect to named route
@app.route('/dashboard')
def dashboard():
    return redirect(url_for('home'))

# 9. Error responses
@app.route('/error')
def error():
    return jsonify({'error': 'Something went wrong'}), 500

# 10. No content
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Delete user logic here
    return '', 204  # No content
"""
        print(code)

    def demonstrate_json_api(self) -> None:
        """Demonstrate building a JSON API."""
        print("\nJSON API EXAMPLE")
        print("=" * 60)

        code = """
from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data store
users = [
    {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
    {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'},
]
next_id = 3

# GET all users
@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify({'users': users})

# GET single user
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)

# POST create user
@app.route('/api/users', methods=['POST'])
def create_user():
    global next_id

    data = request.get_json()

    # Validation
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Name and email required'}), 400

    new_user = {
        'id': next_id,
        'name': data['name'],
        'email': data['email']
    }
    users.append(new_user)
    next_id += 1

    return jsonify(new_user), 201

# PUT update user
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    user['name'] = data.get('name', user['name'])
    user['email'] = data.get('email', user['email'])

    return jsonify(user)

# DELETE user
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    users = [u for u in users if u['id'] != user_id]
    return '', 204
"""
        print(code)

    def demonstrate_error_handling(self) -> None:
        """Demonstrate error handling in Flask."""
        print("\nERROR HANDLING")
        print("=" * 60)

        code = """
from flask import Flask, jsonify

app = Flask(__name__)

# Custom error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

# Manual error triggering
from werkzeug.exceptions import NotFound, BadRequest

@app.route('/users/<int:user_id>')
def get_user(user_id):
    user = find_user(user_id)
    if user is None:
        raise NotFound('User not found')
    return jsonify(user)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        raise BadRequest('Request body is required')
    return jsonify(data), 201

# Generic exception handler
@app.errorhandler(Exception)
def handle_exception(error):
    # Log the error
    app.logger.error(f'Unhandled exception: {error}')
    return jsonify({'error': 'Internal server error'}), 500
"""
        print(code)

    def demonstrate_application_context(self) -> None:
        """Demonstrate Flask application context."""
        print("\nAPPLICATION CONTEXT")
        print("=" * 60)

        code = """
from flask import Flask, g, current_app

app = Flask(__name__)

# Configuration
app.config['DEBUG'] = True
app.config['DATABASE_URL'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'dev-secret-key'

# Before request hook
@app.before_request
def before_request():
    '''Runs before each request.'''
    g.user = None  # g is request-scoped storage
    # Could load user from session here

# After request hook
@app.after_request
def after_request(response):
    '''Runs after each request.'''
    response.headers['X-Custom-Header'] = 'Value'
    return response

# Teardown hook
@app.teardown_request
def teardown_request(exception):
    '''Runs at the end of request, even if exception occurred.'''
    # Close database connections, clean up resources
    pass

# Using g for request-scoped data
@app.route('/user/profile')
def profile():
    if g.user is None:
        return 'Not logged in', 401
    return f'Profile for {g.user}'

# Accessing config
@app.route('/config')
def show_config():
    debug_mode = current_app.config['DEBUG']
    return jsonify({'debug': debug_mode})
"""
        print(code)


def main() -> None:
    """Main entry point demonstrating Flask basics."""
    print("\n" + "=" * 60)
    print("PROGRAM 43: FLASK BASICS")
    print("=" * 60 + "\n")

    demo = FlaskBasicsDemo()

    demo.demonstrate_basic_app()
    demo.demonstrate_routes()
    demo.demonstrate_request_methods()
    demo.demonstrate_request_object()
    demo.demonstrate_response_object()
    demo.demonstrate_json_api()
    demo.demonstrate_error_handling()
    demo.demonstrate_application_context()

    print("\n" + "=" * 60)
    print("FLASK BEST PRACTICES")
    print("=" * 60)
    print("1. Use blueprints for organizing large applications")
    print("2. Never run with debug=True in production")
    print("3. Use environment variables for configuration")
    print("4. Validate and sanitize all user input")
    print("5. Use proper error handlers for all error codes")
    print("6. Use jsonify() for JSON responses (proper Content-Type)")
    print("7. Implement proper logging")
    print("8. Use before_request for authentication checks")
    print("9. Close database connections in teardown handlers")
    print("10. Use application factory pattern for testing")
    print("=" * 60)


if __name__ == "__main__":
    main()
