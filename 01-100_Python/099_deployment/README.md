# Program 99: Deployment

Application packaging, distribution, and deployment strategies for Python projects.

## Description

This program demonstrates packaging Python applications for distribution, including setup.py, requirements, Docker containers, CI/CD pipelines, and deployment best practices. Essential for production deployments.

## Learning Objectives

- Master Python packaging (setuptools, pip)
- Create distributable packages
- Build Docker containers
- Implement CI/CD pipelines
- Deploy to production
- Manage dependencies

## Features

- **Package Structure**: Proper project layout
- **setup.py**: Package metadata and dependencies
- **requirements.txt**: Dependency management
- **pyproject.toml**: Modern packaging
- **Docker**: Containerization
- **CI/CD**: Automated testing and deployment
- **Environment Config**: Development, staging, production
- **Deployment Strategies**: Blue-green, rolling updates

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/099_deployment
python src/main.py
```

## Key Concepts

### Package Structure

```
myproject/
├── README.md
├── LICENSE
├── setup.py
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── mypackage/
│   ├── __init__.py
│   ├── module1.py
│   └── module2.py
├── tests/
│   └── test_module1.py
└── docs/
```

### setup.py

```python
from setuptools import setup, find_packages

setup(
    name='myproject',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.0',
        'click>=8.0.0',
    ],
    entry_points={
        'console_scripts': [
            'myapp=mypackage.cli:main',
        ],
    },
    python_requires='>=3.8',
)
```

### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

### docker-compose.yml

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
    depends_on:
      - db
  db:
    image: postgres:13
```

### CI/CD (GitHub Actions)

```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          # Deployment commands
```

### Environment Configuration

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    DATABASE_URL = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
```

### Building and Publishing

```bash
# Build package
python -m build

# Creates:
# dist/myproject-1.0.0-py3-none-any.whl
# dist/myproject-1.0.0.tar.gz

# Upload to PyPI
python -m twine upload dist/*
```

## Best Practices

1. **Use virtual environments**: Isolate dependencies
2. **Pin dependencies**: requirements.txt with versions
3. **Separate dev dependencies**: requirements-dev.txt
4. **Use environment variables**: Never commit secrets
5. **Test before deploying**: Automated CI/CD
6. **Deploy to staging first**: Test in production-like environment
7. **Monitor deployments**: Track errors and performance
8. **Have rollback plan**: Quick recovery from issues

## Testing

```bash
# Run tests
pytest tests/

# Build package locally
python -m build

# Test installation
pip install dist/myproject-1.0.0-py3-none-any.whl

# Build Docker image
docker build -t myapp:latest .

# Run container
docker run -p 8000:8000 myapp:latest

# Test deployment
# - Staging deployment
# - Production deployment
# - Rollback procedure
```

## Navigation

- **Previous**: [Program 98 - Scripting](../098_scripting/README.md)
- **Next**: [Program 100 - Performance Optimization](../100_performance_optimization/README.md)
- **Home**: [Main README](../README.md)
