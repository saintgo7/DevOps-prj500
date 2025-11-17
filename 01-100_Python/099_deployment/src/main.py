#!/usr/bin/env python3
"""
Program 99: Deployment
Demonstrates packaging, distribution, and deployment strategies.
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any
import tempfile


def demonstrate_package_structure() -> None:
    """Demonstrate Python package structure."""
    print("\n" + "=" * 60)
    print("PACKAGE STRUCTURE")
    print("=" * 60)

    print("\n1. Basic package layout:")
    print("""
    myproject/
    ├── README.md
    ├── LICENSE
    ├── setup.py
    ├── requirements.txt
    ├── mypackage/
    │   ├── __init__.py
    │   ├── module1.py
    │   └── module2.py
    └── tests/
        ├── __init__.py
        ├── test_module1.py
        └── test_module2.py
    """)

    print("\n2. Key files:")
    print("   setup.py: Package metadata and dependencies")
    print("   __init__.py: Makes directory a package")
    print("   requirements.txt: List of dependencies")
    print("   README.md: Project documentation")


def demonstrate_setup_py() -> None:
    """Demonstrate setup.py configuration."""
    print("\n" + "=" * 60)
    print("SETUP.PY")
    print("=" * 60)

    print("\n1. Basic setup.py:")
    print("""
from setuptools import setup, find_packages

setup(
    name='myproject',
    version='1.0.0',
    author='Your Name',
    author_email='you@example.com',
    description='A short description',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/myproject',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.8',
    install_requires=[
        'requests>=2.25.0',
        'click>=8.0.0',
    ],
    entry_points={
        'console_scripts': [
            'myapp=mypackage.cli:main',
        ],
    },
)
    """)


def demonstrate_requirements() -> None:
    """Demonstrate requirements management."""
    print("\n" + "=" * 60)
    print("REQUIREMENTS")
    print("=" * 60)

    print("\n1. requirements.txt:")
    print("""
    # Core dependencies
    requests>=2.25.0,<3.0.0
    click==8.0.1
    pyyaml~=5.4

    # Development dependencies (requirements-dev.txt)
    pytest>=6.0.0
    black==21.5b1
    flake8>=3.9.0
    """)

    print("\n2. Version specifiers:")
    print("   ==  : Exact version")
    print("   >=  : Minimum version")
    print("   ~=  : Compatible version")
    print("   >=,<: Version range")

    print("\n3. Generating requirements:")
    print("   pip freeze > requirements.txt")
    print("   pip install -r requirements.txt")


def demonstrate_pyproject_toml() -> None:
    """Demonstrate modern Python packaging."""
    print("\n" + "=" * 60)
    print("PYPROJECT.TOML")
    print("=" * 60)

    print("\n1. Modern packaging with pyproject.toml:")
    print("""
[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "myproject"
version = "1.0.0"
description = "A sample project"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "you@example.com"}
]
dependencies = [
    "requests>=2.25.0",
    "click>=8.0.0"
]

[project.optional-dependencies]
dev = [
    "pytest>=6.0.0",
    "black>=21.5b1"
]

[project.scripts]
myapp = "mypackage.cli:main"
    """)


def demonstrate_building_packages() -> None:
    """Demonstrate building Python packages."""
    print("\n" + "=" * 60)
    print("BUILDING PACKAGES")
    print("=" * 60)

    print("\n1. Build process:")
    print("   # Install build tools")
    print("   pip install build wheel")

    print("\n   # Build package")
    print("   python -m build")

    print("\n2. Output:")
    print("   dist/")
    print("   ├── myproject-1.0.0-py3-none-any.whl")
    print("   └── myproject-1.0.0.tar.gz")

    print("\n3. Wheel vs Source:")
    print("   .whl: Binary distribution (faster install)")
    print("   .tar.gz: Source distribution (universal)")


def demonstrate_virtual_environments() -> None:
    """Demonstrate virtual environment usage."""
    print("\n" + "=" * 60)
    print("VIRTUAL ENVIRONMENTS")
    print("=" * 60)

    print("\n1. Creating virtual environment:")
    print("   python -m venv venv")
    print("   python3 -m venv .venv")

    print("\n2. Activating:")
    print("   # Linux/Mac")
    print("   source venv/bin/activate")
    print("   # Windows")
    print("   venv\\Scripts\\activate")

    print("\n3. Using virtualenv:")
    print("   (venv) $ pip install -r requirements.txt")
    print("   (venv) $ python app.py")
    print("   (venv) $ deactivate")


def demonstrate_docker_deployment() -> None:
    """Demonstrate Docker deployment."""
    print("\n" + "=" * 60)
    print("DOCKER DEPLOYMENT")
    print("=" * 60)

    print("\n1. Dockerfile:")
    print("""
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
    """)

    print("\n2. Building and running:")
    print("   docker build -t myapp:latest .")
    print("   docker run -p 8000:8000 myapp:latest")

    print("\n3. docker-compose.yml:")
    print("""
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://db/myapp
    depends_on:
      - db
  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
    """)


def demonstrate_deployment_strategies() -> None:
    """Demonstrate deployment strategies."""
    print("\n" + "=" * 60)
    print("DEPLOYMENT STRATEGIES")
    print("=" * 60)

    print("\n1. Manual deployment:")
    print("   - Copy files to server")
    print("   - Install dependencies")
    print("   - Restart services")
    print("   Pros: Simple, direct control")
    print("   Cons: Error-prone, not scalable")

    print("\n2. CI/CD pipeline:")
    print("   - Push code to repository")
    print("   - Automated tests run")
    print("   - Automatic deployment on success")
    print("   Tools: GitHub Actions, GitLab CI, Jenkins")

    print("\n3. Container orchestration:")
    print("   - Package as Docker container")
    print("   - Deploy to Kubernetes/Docker Swarm")
    print("   - Auto-scaling and load balancing")


def demonstrate_environment_configuration() -> None:
    """Demonstrate environment configuration."""
    print("\n" + "=" * 60)
    print("ENVIRONMENT CONFIGURATION")
    print("=" * 60)

    print("\n1. .env file:")
    print("""
    DATABASE_URL=postgresql://localhost/mydb
    SECRET_KEY=your-secret-key
    DEBUG=False
    LOG_LEVEL=INFO
    """)

    print("\n2. Loading environment variables:")
    print("""
    import os
    from dotenv import load_dotenv

    load_dotenv()

    DATABASE_URL = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    """)

    print("\n3. Environment-specific configs:")
    print("   .env.development")
    print("   .env.staging")
    print("   .env.production")


def demonstrate_deployment_checklist() -> None:
    """Demonstrate deployment checklist."""
    print("\n" + "=" * 60)
    print("DEPLOYMENT CHECKLIST")
    print("=" * 60)

    print("\n1. Pre-deployment:")
    print("   ☐ Run all tests")
    print("   ☐ Update version number")
    print("   ☐ Update CHANGELOG")
    print("   ☐ Review dependencies")
    print("   ☐ Security scan")

    print("\n2. Deployment:")
    print("   ☐ Backup database")
    print("   ☐ Deploy to staging first")
    print("   ☐ Run smoke tests")
    print("   ☐ Deploy to production")
    print("   ☐ Monitor logs")

    print("\n3. Post-deployment:")
    print("   ☐ Verify functionality")
    print("   ☐ Check error logs")
    print("   ☐ Monitor performance")
    print("   ☐ Update documentation")
    print("   ☐ Tag release in git")


def demonstrate_publishing_to_pypi() -> None:
    """Demonstrate publishing to PyPI."""
    print("\n" + "=" * 60)
    print("PUBLISHING TO PYPI")
    print("=" * 60)

    print("\n1. Setup PyPI account:")
    print("   - Register at pypi.org")
    print("   - Generate API token")
    print("   - Configure .pypirc")

    print("\n2. Build and upload:")
    print("   # Build package")
    print("   python -m build")

    print("\n   # Upload to TestPyPI (testing)")
    print("   python -m twine upload --repository testpypi dist/*")

    print("\n   # Upload to PyPI (production)")
    print("   python -m twine upload dist/*")

    print("\n3. Versioning:")
    print("   - Semantic versioning: MAJOR.MINOR.PATCH")
    print("   - Example: 1.2.3")
    print("   - Increment MAJOR for breaking changes")


def demonstrate_ci_cd_example() -> None:
    """Demonstrate CI/CD configuration."""
    print("\n" + "=" * 60)
    print("CI/CD EXAMPLE")
    print("=" * 60)

    print("\n1. GitHub Actions (.github/workflows/deploy.yml):")
    print("""
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest
      - name: Run tests
        run: pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to production
        run: |
          # Deployment commands here
          echo "Deploying..."
    """)


def demonstrate_monitoring_deployment() -> None:
    """Demonstrate deployment monitoring."""
    print("\n" + "=" * 60)
    print("DEPLOYMENT MONITORING")
    print("=" * 60)

    print("\n1. Application monitoring:")
    print("   - Error tracking (Sentry)")
    print("   - Performance monitoring (New Relic)")
    print("   - Uptime monitoring (Pingdom)")

    print("\n2. Logging:")
    print("   - Centralized logging (ELK stack)")
    print("   - Log aggregation (CloudWatch)")
    print("   - Log levels and rotation")

    print("\n3. Metrics:")
    print("   - Request rates")
    print("   - Response times")
    print("   - Error rates")
    print("   - Resource usage")


def demonstrate_rollback_strategy() -> None:
    """Demonstrate rollback strategy."""
    print("\n" + "=" * 60)
    print("ROLLBACK STRATEGY")
    print("=" * 60)

    print("\n1. Version control:")
    print("   - Tag releases in git")
    print("   - Keep deployment artifacts")
    print("   - Document rollback procedures")

    print("\n2. Database migrations:")
    print("   - Make migrations reversible")
    print("   - Test rollback in staging")
    print("   - Keep data backups")

    print("\n3. Blue-Green deployment:")
    print("   - Maintain two environments")
    print("   - Deploy to inactive (green)")
    print("   - Switch traffic if successful")
    print("   - Easy rollback (switch back)")


def demonstrate_best_practices() -> None:
    """Demonstrate deployment best practices."""
    print("\n" + "=" * 60)
    print("DEPLOYMENT BEST PRACTICES")
    print("=" * 60)

    print("\n1. Automation:")
    print("   ✓ Automate testing")
    print("   ✓ Automate deployment")
    print("   ✓ Infrastructure as code")
    print("   ✓ Automated rollbacks")

    print("\n2. Security:")
    print("   ✓ Never commit secrets")
    print("   ✓ Use environment variables")
    print("   ✓ Scan for vulnerabilities")
    print("   ✓ Keep dependencies updated")

    print("\n3. Testing:")
    print("   ✓ Unit tests")
    print("   ✓ Integration tests")
    print("   ✓ Smoke tests in production")
    print("   ✓ Load testing")

    print("\n4. Documentation:")
    print("   ✓ Deployment procedures")
    print("   ✓ Rollback procedures")
    print("   ✓ Environment setup")
    print("   ✓ Troubleshooting guide")


def main() -> None:
    """Main function demonstrating deployment."""
    print("=" * 60)
    print("PYTHON DEPLOYMENT")
    print("=" * 60)

    demonstrate_package_structure()
    demonstrate_setup_py()
    demonstrate_requirements()
    demonstrate_pyproject_toml()
    demonstrate_building_packages()
    demonstrate_virtual_environments()
    demonstrate_docker_deployment()
    demonstrate_deployment_strategies()
    demonstrate_environment_configuration()
    demonstrate_deployment_checklist()
    demonstrate_publishing_to_pypi()
    demonstrate_ci_cd_example()
    demonstrate_monitoring_deployment()
    demonstrate_rollback_strategy()
    demonstrate_best_practices()

    print("\n" + "=" * 60)
    print("All deployment demonstrations completed!")
    print("=" * 60)
    print("\nKey tools:")
    print("- pip, setuptools, wheel: Packaging")
    print("- Docker: Containerization")
    print("- GitHub Actions/GitLab CI: CI/CD")
    print("- Kubernetes: Orchestration")


if __name__ == "__main__":
    main()
