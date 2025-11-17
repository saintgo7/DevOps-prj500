#!/usr/bin/env python3
"""
Program 45: Flask Templates
Demonstrates Jinja2 templating in Flask including template rendering,
filters, macros, and template inheritance.

Topics covered:
- Template rendering
- Template variables and expressions
- Control structures (if, for, etc.)
- Filters
- Template inheritance (extends, blocks)
- Macros
- Template context
"""

from typing import Dict, Any, List


class FlaskTemplatesDemo:
    """Demonstration of Flask templates and Jinja2."""

    def demonstrate_basic_rendering(self) -> None:
        """Demonstrate basic template rendering."""
        print("BASIC TEMPLATE RENDERING")
        print("=" * 60)

        print("\n1. Rendering Templates:")
        print("-" * 60)
        code = """
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Render template from templates/ directory
    return render_template('index.html')

@app.route('/user/<username>')
def user_profile(username):
    # Pass variables to template
    return render_template('profile.html', username=username)

@app.route('/dashboard')
def dashboard():
    # Pass multiple variables
    user = {'name': 'John', 'email': 'john@example.com'}
    posts = [
        {'title': 'First Post', 'date': '2024-01-01'},
        {'title': 'Second Post', 'date': '2024-01-02'}
    ]
    return render_template(
        'dashboard.html',
        user=user,
        posts=posts,
        page_title='Dashboard'
    )
"""
        print(code)

        print("2. Template Structure (templates/index.html):")
        print("-" * 60)
        template = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ page_title }}</title>
</head>
<body>
    <h1>Welcome to Flask</h1>
    <p>Current user: {{ username }}</p>
</body>
</html>
"""
        print(template)

    def demonstrate_template_syntax(self) -> None:
        """Demonstrate Jinja2 template syntax."""
        print("\nTEMPLATE SYNTAX")
        print("=" * 60)

        print("\n1. Variables and Expressions:")
        print("-" * 60)
        template = """
<!-- Variables -->
<h1>{{ page_title }}</h1>
<p>{{ user.name }}</p>
<p>{{ user['email'] }}</p>

<!-- Expressions -->
<p>{{ 2 + 2 }}</p>
<p>{{ 'hello' ~ ' ' ~ 'world' }}</p>  <!-- Concatenation -->
<p>{{ items | length }}</p>

<!-- Accessing attributes -->
<p>{{ user.name }}</p>
<p>{{ user.get_full_name() }}</p>

<!-- Safe vs Auto-escape -->
<p>{{ user_input }}</p>  <!-- Auto-escaped (safe from XSS) -->
<p>{{ html_content | safe }}</p>  <!-- Trust this HTML -->
"""
        print(template)

        print("2. Control Structures:")
        print("-" * 60)
        template = """
<!-- If statements -->
{% if user.is_authenticated %}
    <p>Welcome, {{ user.name }}!</p>
{% elif user.is_guest %}
    <p>Welcome, Guest!</p>
{% else %}
    <p>Please log in</p>
{% endif %}

<!-- For loops -->
<ul>
{% for item in items %}
    <li>{{ item.name }} - ${{ item.price }}</li>
{% endfor %}
</ul>

<!-- For loop with index -->
{% for item in items %}
    <p>{{ loop.index }}. {{ item }}</p>  <!-- 1-indexed -->
    <p>{{ loop.index0 }}. {{ item }}</p>  <!-- 0-indexed -->
{% endfor %}

<!-- For loop special variables -->
{% for item in items %}
    {% if loop.first %}
        <strong>First: {{ item }}</strong>
    {% elif loop.last %}
        <em>Last: {{ item }}</em>
    {% else %}
        {{ item }}
    {% endif %}
{% endfor %}

<!-- Empty clause -->
<ul>
{% for user in users %}
    <li>{{ user.name }}</li>
{% else %}
    <li>No users found</li>
{% endfor %}
</ul>

<!-- Loop filtering -->
{% for user in users if user.is_active %}
    <li>{{ user.name }}</li>
{% endfor %}
"""
        print(template)

    def demonstrate_filters(self) -> None:
        """Demonstrate Jinja2 filters."""
        print("\nTEMPLATE FILTERS")
        print("=" * 60)

        print("\n1. Built-in Filters:")
        print("-" * 60)
        template = """
<!-- String filters -->
{{ "hello world" | capitalize }}  <!-- Hello world -->
{{ "hello world" | title }}  <!-- Hello World -->
{{ "HELLO" | lower }}  <!-- hello -->
{{ "hello" | upper }}  <!-- HELLO -->
{{ "  hello  " | trim }}  <!-- hello -->
{{ "hello" | reverse }}  <!-- olleh -->
{{ "hello" | length }}  <!-- 5 -->
{{ "hello world" | replace("world", "there") }}  <!-- hello there -->

<!-- List filters -->
{{ [1, 2, 3] | join(', ') }}  <!-- 1, 2, 3 -->
{{ items | length }}
{{ items | first }}
{{ items | last }}
{{ [3, 1, 2] | sort }}  <!-- [1, 2, 3] -->
{{ [1, 2, 2, 3] | unique }}  <!-- [1, 2, 3] -->

<!-- Number filters -->
{{ 42.5678 | round(2) }}  <!-- 42.57 -->
{{ 1000000 | filesizeformat }}  <!-- 976.6 KiB -->

<!-- Date filters (requires datetime) -->
{{ now | strftime('%Y-%m-%d') }}

<!-- Default values -->
{{ user.name | default('Anonymous') }}
{{ user.email | default('No email', true) }}  <!-- true = treat empty string as missing -->

<!-- URL encoding -->
{{ "hello world" | urlencode }}  <!-- hello+world -->

<!-- Safe/escape -->
{{ user_html | safe }}  <!-- Don't escape HTML -->
{{ user_input | escape }}  <!-- Escape HTML (default) -->

<!-- JSON -->
{{ data | tojson }}  <!-- Convert to JSON -->
{{ data | tojson | safe }}  <!-- For use in <script> tags -->

<!-- Chaining filters -->
{{ "hello world" | title | reverse }}  <!-- dlroW olleH -->
"""
        print(template)

        print("2. Custom Filters:")
        print("-" * 60)
        code = """
from flask import Flask

app = Flask(__name__)

# Define custom filter
@app.template_filter('reverse_words')
def reverse_words(s):
    '''Reverse order of words in a string.'''
    return ' '.join(reversed(s.split()))

@app.template_filter('currency')
def currency_filter(value):
    '''Format number as currency.'''
    return f'${value:,.2f}'

@app.template_filter('pluralize')
def pluralize(count, singular='', plural='s'):
    '''Pluralize a word based on count.'''
    return singular if count == 1 else plural

# Or register filter
def datetime_format(value, format='%Y-%m-%d'):
    return value.strftime(format)

app.jinja_env.filters['datetime'] = datetime_format

# Usage in templates:
# {{ "hello world" | reverse_words }}  <!-- world hello -->
# {{ 1234.56 | currency }}  <!-- $1,234.56 -->
# {{ items | length }} item{{ items | length | pluralize }}
# {{ user.created_at | datetime('%Y-%m-%d %H:%M') }}
"""
        print(code)

    def demonstrate_template_inheritance(self) -> None:
        """Demonstrate template inheritance."""
        print("\nTEMPLATE INHERITANCE")
        print("=" * 60)

        print("\n1. Base Template (templates/base.html):")
        print("-" * 60)
        template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{% block title %}Default Title{% endblock %}</title>
    {% block head %}
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    {% endblock %}
</head>
<body>
    <header>
        <nav>
            {% block navigation %}
            <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/about">About</a></li>
            </ul>
            {% endblock %}
        </nav>
    </header>

    <main>
        {% block content %}
        <!-- Child template content goes here -->
        {% endblock %}
    </main>

    <footer>
        {% block footer %}
        <p>&copy; 2024 My Website</p>
        {% endblock %}
    </footer>

    {% block scripts %}
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    {% endblock %}
</body>
</html>
"""
        print(template)

        print("2. Child Template (templates/page.html):")
        print("-" * 60)
        template = """
{% extends "base.html" %}

{% block title %}Page Title{% endblock %}

{% block head %}
    {{ super() }}  <!-- Include parent's head block -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/page.css') }}">
{% endblock %}

{% block content %}
    <h1>{{ page_title }}</h1>
    <p>This is the page content.</p>

    {% for item in items %}
        <div class="item">{{ item }}</div>
    {% endfor %}
{% endblock %}

{% block scripts %}
    {{ super() }}  <!-- Include parent's scripts -->
    <script src="{{ url_for('static', filename='js/page.js') }}"></script>
{% endblock %}
"""
        print(template)

        print("3. Three-Level Inheritance:")
        print("-" * 60)
        template = """
<!-- templates/admin/base.html -->
{% extends "base.html" %}

{% block navigation %}
    <ul>
        <li><a href="/admin">Dashboard</a></li>
        <li><a href="/admin/users">Users</a></li>
        <li><a href="/admin/settings">Settings</a></li>
    </ul>
{% endblock %}

<!-- templates/admin/users.html -->
{% extends "admin/base.html" %}

{% block title %}User Management{% endblock %}

{% block content %}
    <h1>Users</h1>
    <table>
        {% for user in users %}
        <tr>
            <td>{{ user.name }}</td>
            <td>{{ user.email }}</td>
        </tr>
        {% endfor %}
    </table>
{% endblock %}
"""
        print(template)

    def demonstrate_macros(self) -> None:
        """Demonstrate Jinja2 macros."""
        print("\nTEMPLATE MACROS")
        print("=" * 60)

        print("\n1. Defining and Using Macros:")
        print("-" * 60)
        template = """
<!-- Define macro -->
{% macro render_user(user) %}
    <div class="user">
        <h3>{{ user.name }}</h3>
        <p>{{ user.email }}</p>
    </div>
{% endmacro %}

<!-- Use macro -->
{% for user in users %}
    {{ render_user(user) }}
{% endfor %}

<!-- Macro with optional parameters -->
{% macro input_field(name, value='', type='text', required=false) %}
    <input type="{{ type }}"
           name="{{ name }}"
           value="{{ value }}"
           {% if required %}required{% endif %}>
{% endmacro %}

<!-- Use with defaults -->
{{ input_field('username') }}
{{ input_field('email', type='email', required=true) }}
{{ input_field('password', type='password', required=true) }}

<!-- Macro with caller block -->
{% macro card(title) %}
    <div class="card">
        <h2>{{ title }}</h2>
        <div class="card-body">
            {{ caller() }}
        </div>
    </div>
{% endmacro %}

{% call card("User Profile") %}
    <p>Name: {{ user.name }}</p>
    <p>Email: {{ user.email }}</p>
{% endcall %}
"""
        print(template)

        print("2. Macro Files (templates/macros.html):")
        print("-" * 60)
        template = """
<!-- macros.html -->
{% macro render_pagination(page, total_pages) %}
    <nav>
        <ul class="pagination">
            {% for p in range(1, total_pages + 1) %}
                <li class="{% if p == page %}active{% endif %}">
                    <a href="?page={{ p }}">{{ p }}</a>
                </li>
            {% endfor %}
        </ul>
    </nav>
{% endmacro %}

{% macro render_form_field(field) %}
    <div class="form-group">
        <label for="{{ field.name }}">{{ field.label }}</label>
        <input type="{{ field.type }}"
               id="{{ field.name }}"
               name="{{ field.name }}"
               value="{{ field.value }}"
               class="form-control">
        {% if field.errors %}
            <div class="errors">
                {% for error in field.errors %}
                    <span class="error">{{ error }}</span>
                {% endfor %}
            </div>
        {% endif %}
    </div>
{% endmacro %}

<!-- Import and use in another template -->
{% from 'macros.html' import render_pagination, render_form_field %}

{{ render_pagination(current_page, total_pages) }}

{% for field in form.fields %}
    {{ render_form_field(field) }}
{% endfor %}
"""
        print(template)

    def demonstrate_includes(self) -> None:
        """Demonstrate template includes."""
        print("\nTEMPLATE INCLUDES")
        print("=" * 60)

        template = """
<!-- templates/_navbar.html -->
<nav>
    <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about">About</a></li>
        <li><a href="/contact">Contact</a></li>
    </ul>
</nav>

<!-- templates/page.html -->
{% include '_navbar.html' %}

<h1>Page Content</h1>

<!-- Include with context -->
{% include '_user_card.html' %}

<!-- Include without context (isolated) -->
{% include '_footer.html' without context %}

<!-- Include with variables -->
{% include '_message.html' with message='Success!', type='success' %}

<!-- Conditional include -->
{% if show_sidebar %}
    {% include '_sidebar.html' %}
{% endif %}

<!-- Include with ignore missing (won't error if file doesn't exist) -->
{% include '_optional.html' ignore missing %}
"""
        print(template)

    def demonstrate_context_processors(self) -> None:
        """Demonstrate context processors."""
        print("\nCONTEXT PROCESSORS")
        print("=" * 60)

        code = """
from flask import Flask
from datetime import datetime

app = Flask(__name__)

# Add variables available to all templates
@app.context_processor
def inject_now():
    '''Make current datetime available in all templates.'''
    return {'now': datetime.now()}

@app.context_processor
def inject_site_data():
    '''Inject site-wide data.'''
    return {
        'site_name': 'My Website',
        'site_url': 'https://example.com',
        'analytics_id': 'UA-12345678-1'
    }

# Template global functions
@app.template_global()
def get_user_avatar(user_id):
    '''Get user avatar URL.'''
    return f'/static/avatars/{user_id}.jpg'

# Usage in templates:
# {{ now }}
# {{ now.strftime('%Y-%m-%d') }}
# {{ site_name }}
# <img src="{{ get_user_avatar(user.id) }}">

# Template tests
@app.template_test()
def prime(n):
    '''Test if number is prime.'''
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Usage: {% if number is prime %}
"""
        print(code)

    def demonstrate_advanced_features(self) -> None:
        """Demonstrate advanced template features."""
        print("\nADVANCED FEATURES")
        print("=" * 60)

        print("\n1. Template Variables and Assignments:")
        print("-" * 60)
        template = """
<!-- Set variable -->
{% set user_count = users | length %}
<p>Total users: {{ user_count }}</p>

<!-- Set with block -->
{% set navigation %}
    <li><a href="/">Home</a></li>
    <li><a href="/about">About</a></li>
{% endset %}

<!-- With statement (create scope) -->
{% with message = 'Success!' %}
    <p>{{ message }}</p>
{% endwith %}

<!-- With from filter -->
{% with total = items | length %}
    <p>Total items: {{ total }}</p>
{% endwith %}
"""
        print(template)

        print("2. Whitespace Control:")
        print("-" * 60)
        template = """
<!-- Remove whitespace before tag -->
<div>
    {%- for item in items %}
        <li>{{ item }}</li>
    {% endfor -%}
</div>

<!-- Completely remove whitespace -->
{%- for item in items -%}
    {{ item }}
{%- endfor -%}
"""
        print(template)

        print("3. Comments:")
        print("-" * 60)
        template = """
<!-- HTML comment (visible in source) -->

{# Jinja2 comment (not in output) #}

{# Multi-line
   Jinja2
   comment #}
"""
        print(template)

        print("4. Escaping:")
        print("-" * 60)
        template = """
<!-- Output literal {{ }} -->
{{ '{{' }} variable {{ '}}' }}

<!-- Or use raw block -->
{% raw %}
    {{ this won't be processed }}
    {% neither will this %}
{% endraw %}
"""
        print(template)


def main() -> None:
    """Main entry point demonstrating Flask templates."""
    print("\n" + "=" * 60)
    print("PROGRAM 45: FLASK TEMPLATES")
    print("=" * 60 + "\n")

    demo = FlaskTemplatesDemo()

    demo.demonstrate_basic_rendering()
    demo.demonstrate_template_syntax()
    demo.demonstrate_filters()
    demo.demonstrate_template_inheritance()
    demo.demonstrate_macros()
    demo.demonstrate_includes()
    demo.demonstrate_context_processors()
    demo.demonstrate_advanced_features()

    print("\n" + "=" * 60)
    print("TEMPLATE BEST PRACTICES")
    print("=" * 60)
    print("1. Use template inheritance to avoid duplication")
    print("2. Extract reusable components into macros")
    print("3. Use filters for formatting, not business logic")
    print("4. Auto-escaping is enabled by default - use it!")
    print("5. Keep templates simple - complex logic in views")
    print("6. Use meaningful block names")
    print("7. Organize templates in subdirectories")
    print("8. Use context processors for global variables")
    print("9. Cache compiled templates in production")
    print("10. Test your templates with various data")
    print("=" * 60)


if __name__ == "__main__":
    main()
