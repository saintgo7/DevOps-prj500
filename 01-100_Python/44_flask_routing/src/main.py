#!/usr/bin/env python3
"""
Program 44: Flask Routing
Demonstrates advanced routing in Flask including URL parameters,
query strings, and route methods.

Topics covered:
- URL parameters (path variables)
- Variable rules and converters
- Query strings
- HTTP methods per route
- URL building
- Blueprints for organization
"""

from typing import Dict, Any, List


class FlaskRoutingDemo:
    """Demonstration of Flask routing patterns."""

    def demonstrate_url_parameters(self) -> None:
        """Demonstrate URL path parameters."""
        print("URL PATH PARAMETERS")
        print("=" * 60)

        code = """
from flask import Flask

app = Flask(__name__)

# String parameter (default)
@app.route('/user/<username>')
def show_user(username):
    return f'User: {username}'

# Integer parameter
@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Post ID: {post_id} (type: {type(post_id).__name__})'

# Float parameter
@app.route('/rating/<float:score>')
def show_rating(score):
    return f'Rating: {score}'

# Path parameter (accepts slashes)
@app.route('/file/<path:filepath>')
def show_file(filepath):
    return f'File path: {filepath}'
    # Example: /file/documents/2024/report.pdf
    # filepath = 'documents/2024/report.pdf'

# UUID parameter
from uuid import UUID

@app.route('/object/<uuid:object_id>')
def show_object(object_id):
    return f'Object ID: {object_id}'
    # Example: /object/550e8400-e29b-41d4-a716-446655440000

# Multiple parameters
@app.route('/users/<int:user_id>/posts/<int:post_id>')
def show_user_post(user_id, post_id):
    return f'User {user_id}, Post {post_id}'

# Optional parameters with default
@app.route('/page/')
@app.route('/page/<int:page_num>')
def show_page(page_num=1):
    return f'Page: {page_num}'
"""
        print(code)

    def demonstrate_query_strings(self) -> None:
        """Demonstrate handling query string parameters."""
        print("\nQUERY STRING PARAMETERS")
        print("=" * 60)

        code = """
from flask import Flask, request

app = Flask(__name__)

@app.route('/search')
def search():
    # Get single query parameter with default
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    # Get all values for a parameter (for multi-select)
    tags = request.args.getlist('tag')

    # Get all query parameters as dict
    all_params = request.args.to_dict()

    # Check if parameter exists
    if 'sort' in request.args:
        sort_by = request.args['sort']
    else:
        sort_by = 'date'

    return {
        'query': query,
        'page': page,
        'limit': limit,
        'tags': tags,
        'sort': sort_by,
        'all_params': all_params
    }

# Example URLs:
# /search?q=python
# /search?q=python&page=2&limit=20
# /search?q=python&tag=web&tag=api&tag=flask
# /search?q=python&sort=relevance&filter=recent

@app.route('/products')
def list_products():
    # Filtering with query parameters
    category = request.args.get('category')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    in_stock = request.args.get('in_stock', type=bool)

    # Build query based on parameters
    products = []  # Query database here

    return {
        'category': category,
        'price_range': {'min': min_price, 'max': max_price},
        'in_stock_only': in_stock,
        'products': products
    }

# Combining path and query parameters
@app.route('/users/<int:user_id>/posts')
def user_posts(user_id):
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'published')

    return {
        'user_id': user_id,
        'page': page,
        'status': status
    }
"""
        print(code)

    def demonstrate_custom_converters(self) -> None:
        """Demonstrate custom URL converters."""
        print("\nCUSTOM URL CONVERTERS")
        print("=" * 60)

        code = """
from flask import Flask
from werkzeug.routing import BaseConverter

app = Flask(__name__)

# Custom converter for lists
class ListConverter(BaseConverter):
    '''Convert comma-separated values to list.'''

    def to_python(self, value):
        return value.split(',')

    def to_url(self, values):
        return ','.join(str(v) for v in values)

# Register custom converter
app.url_map.converters['list'] = ListConverter

@app.route('/tags/<list:tag_list>')
def show_tags(tag_list):
    return {'tags': tag_list}
    # Example: /tags/python,flask,web
    # tag_list = ['python', 'flask', 'web']

# Custom converter for date ranges
from datetime import datetime

class DateConverter(BaseConverter):
    '''Convert YYYY-MM-DD format to datetime.'''

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value.strftime('%Y-%m-%d')

app.url_map.converters['date'] = DateConverter

@app.route('/reports/<date:start_date>/<date:end_date>')
def date_range_report(start_date, end_date):
    return {
        'start': start_date.isoformat(),
        'end': end_date.isoformat(),
        'days': (end_date - start_date).days
    }
    # Example: /reports/2024-01-01/2024-12-31

# Regex converter
import re

class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        super().__init__(map)
        self.regex = args[0]

app.url_map.converters['regex'] = RegexConverter

@app.route('/user/<regex("[a-z]{3,15}"):username>')
def show_user(username):
    # Only matches lowercase letters, 3-15 characters
    return f'User: {username}'
"""
        print(code)

    def demonstrate_http_methods(self) -> None:
        """Demonstrate handling different HTTP methods."""
        print("\nHTTP METHODS ROUTING")
        print("=" * 60)

        code = """
from flask import Flask, request, jsonify

app = Flask(__name__)

# Single method (default is GET)
@app.route('/users')
def get_users():
    return jsonify({'users': []})

# Multiple methods in one route
@app.route('/api/resource', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_resource():
    if request.method == 'GET':
        return jsonify({'message': 'GET request'})

    elif request.method == 'POST':
        data = request.get_json()
        return jsonify({'message': 'Created', 'data': data}), 201

    elif request.method == 'PUT':
        data = request.get_json()
        return jsonify({'message': 'Updated', 'data': data})

    elif request.method == 'DELETE':
        return '', 204

# Better approach: Separate routes for clarity
@app.route('/api/users', methods=['GET'])
def list_users():
    return jsonify({'users': []})

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    return jsonify(data), 201

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify({'id': user_id})

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    return jsonify({'id': user_id, **data})

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return '', 204

# Using method view classes
from flask.views import MethodView

class UserAPI(MethodView):
    '''Class-based view for user resource.'''

    def get(self, user_id):
        if user_id is None:
            # List users
            return jsonify({'users': []})
        else:
            # Get single user
            return jsonify({'id': user_id})

    def post(self):
        # Create user
        data = request.get_json()
        return jsonify(data), 201

    def put(self, user_id):
        # Update user
        data = request.get_json()
        return jsonify({'id': user_id, **data})

    def delete(self, user_id):
        # Delete user
        return '', 204

# Register class-based view
user_view = UserAPI.as_view('user_api')
app.add_url_rule('/users/', view_func=user_view, methods=['GET', 'POST'])
app.add_url_rule('/users/<int:user_id>', view_func=user_view,
                 methods=['GET', 'PUT', 'DELETE'])
"""
        print(code)

    def demonstrate_url_building(self) -> None:
        """Demonstrate URL building with url_for."""
        print("\nURL BUILDING (url_for)")
        print("=" * 60)

        code = """
from flask import Flask, url_for, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index'

@app.route('/user/<username>')
def profile(username):
    return f'User: {username}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Post: {post_id}'

# Building URLs
@app.route('/test')
def test_urls():
    # Build URL for index
    index_url = url_for('index')  # Returns: '/'

    # Build URL with parameters
    profile_url = url_for('profile', username='john')  # Returns: '/user/john'
    post_url = url_for('show_post', post_id=42)  # Returns: '/post/42'

    # With query parameters
    search_url = url_for('search', q='python', page=2)
    # Returns: '/search?q=python&page=2'

    # External URLs (absolute)
    external_url = url_for('index', _external=True)
    # Returns: 'http://localhost:5000/'

    # Different scheme
    https_url = url_for('index', _external=True, _scheme='https')
    # Returns: 'https://localhost:5000/'

    return {
        'index': index_url,
        'profile': profile_url,
        'post': post_url,
        'search': search_url,
        'external': external_url
    }

# Redirecting to named routes
@app.route('/old-profile')
def old_profile():
    return redirect(url_for('profile', username='default'))

@app.route('/go-home')
def go_home():
    return redirect(url_for('index'))

# In templates (Jinja2)
'''
<a href="{{ url_for('index') }}">Home</a>
<a href="{{ url_for('profile', username='john') }}">Profile</a>
<a href="{{ url_for('static', filename='style.css') }}">Stylesheet</a>
'''
"""
        print(code)

    def demonstrate_blueprints(self) -> None:
        """Demonstrate using blueprints for organization."""
        print("\nBLUEPRINTS (Route Organization)")
        print("=" * 60)

        print("\n1. Creating a Blueprint:")
        print("-" * 60)
        code = """
# File: app/users/routes.py
from flask import Blueprint, jsonify, request

# Create blueprint
users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/')
def list_users():
    return jsonify({'users': []})

@users_bp.route('/<int:user_id>')
def get_user(user_id):
    return jsonify({'id': user_id})

@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    return jsonify(data), 201

# File: app/posts/routes.py
posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

@posts_bp.route('/')
def list_posts():
    return jsonify({'posts': []})

@posts_bp.route('/<int:post_id>')
def get_post(post_id):
    return jsonify({'id': post_id})
"""
        print(code)

        print("2. Registering Blueprints:")
        print("-" * 60)
        code = """
# File: app/__init__.py
from flask import Flask
from app.users.routes import users_bp
from app.posts.routes import posts_bp

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(posts_bp)

    return app

# URLs will be:
# /users/ -> list_users
# /users/123 -> get_user
# /posts/ -> list_posts
# /posts/456 -> get_post
"""
        print(code)

        print("3. Blueprint with Different URL Prefix:")
        print("-" * 60)
        code = """
# Create API version blueprints
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api_v2 = Blueprint('api_v2', __name__, url_prefix='/api/v2')

@api_v1.route('/users')
def v1_users():
    return jsonify({'version': 1, 'users': []})

@api_v2.route('/users')
def v2_users():
    return jsonify({'version': 2, 'users': []})

app.register_blueprint(api_v1)
app.register_blueprint(api_v2)

# URLs:
# /api/v1/users
# /api/v2/users
"""
        print(code)

        print("4. Blueprint URL Building:")
        print("-" * 60)
        code = """
from flask import url_for

# Within same blueprint
url = url_for('.list_users')  # Relative to current blueprint

# From different blueprint
url = url_for('users.list_users')  # Qualified with blueprint name

# In blueprint
@users_bp.route('/profile')
def profile():
    # Redirect to another route in same blueprint
    return redirect(url_for('.list_users'))

    # Or to different blueprint
    return redirect(url_for('posts.list_posts'))
"""
        print(code)

    def demonstrate_route_decorators(self) -> None:
        """Demonstrate custom route decorators."""
        print("\nCUSTOM ROUTE DECORATORS")
        print("=" * 60)

        code = """
from functools import wraps
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# Authentication decorator
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            abort(401)
        token = auth_header.split(' ')[1]
        # Validate token here
        return f(*args, **kwargs)
    return decorated_function

@app.route('/protected')
@require_auth
def protected_route():
    return jsonify({'message': 'Access granted'})

# JSON validation decorator
def validate_json(*expected_keys):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()
            if not data:
                abort(400, 'JSON body required')

            missing = [key for key in expected_keys if key not in data]
            if missing:
                abort(400, f'Missing fields: {missing}')

            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/users', methods=['POST'])
@validate_json('name', 'email')
def create_user():
    data = request.get_json()
    return jsonify(data), 201

# Rate limiting decorator
from time import time
from collections import defaultdict

request_counts = defaultdict(list)

def rate_limit(max_requests, window_seconds):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr
            now = time()

            # Clean old requests
            request_counts[client_ip] = [
                req_time for req_time in request_counts[client_ip]
                if now - req_time < window_seconds
            ]

            # Check rate limit
            if len(request_counts[client_ip]) >= max_requests:
                abort(429, 'Rate limit exceeded')

            # Record this request
            request_counts[client_ip].append(now)

            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/api/data')
@rate_limit(max_requests=10, window_seconds=60)
def get_data():
    return jsonify({'data': 'value'})
"""
        print(code)


def main() -> None:
    """Main entry point demonstrating Flask routing."""
    print("\n" + "=" * 60)
    print("PROGRAM 44: FLASK ROUTING")
    print("=" * 60 + "\n")

    demo = FlaskRoutingDemo()

    demo.demonstrate_url_parameters()
    demo.demonstrate_query_strings()
    demo.demonstrate_custom_converters()
    demo.demonstrate_http_methods()
    demo.demonstrate_url_building()
    demo.demonstrate_blueprints()
    demo.demonstrate_route_decorators()

    print("\n" + "=" * 60)
    print("ROUTING BEST PRACTICES")
    print("=" * 60)
    print("1. Use meaningful, RESTful URL patterns")
    print("2. Use url_for() instead of hardcoding URLs")
    print("3. Organize routes with blueprints for large apps")
    print("4. Use appropriate HTTP methods for operations")
    print("5. Validate URL parameters and query strings")
    print("6. Use type converters for URL parameters")
    print("7. Implement consistent error handling")
    print("8. Document your routes (OpenAPI/Swagger)")
    print("9. Version your APIs in the URL (/api/v1/)")
    print("10. Use decorators for cross-cutting concerns")
    print("=" * 60)


if __name__ == "__main__":
    main()
