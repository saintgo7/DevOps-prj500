#!/usr/bin/env python3
"""
Program 48: Pydantic Models
Demonstrates Pydantic for data validation, parsing, and serialization.

Topics covered:
- BaseModel and basic validation
- Field types and constraints
- Custom validators
- Nested models
- Model configuration
- Serialization and deserialization
- JSON Schema generation
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class PydanticModelsDemo:
    """Demonstration of Pydantic models and validation."""

    def demonstrate_basic_models(self) -> None:
        """Demonstrate basic Pydantic models."""
        print("BASIC PYDANTIC MODELS")
        print("=" * 60)

        code = """
from pydantic import BaseModel
from typing import Optional

# Define model
class User(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int] = None
    is_active: bool = True

# Create instance (validates automatically)
user = User(id=1, name="John", email="john@example.com")
print(user)
# Output: id=1 name='John' email='john@example.com' age=None is_active=True

# Access fields
print(user.name)  # John
print(user.age)   # None

# Validation error for wrong types
try:
    user = User(id="not_an_int", name="John", email="john@example.com")
except ValueError as e:
    print(f"Validation error: {e}")

# Required field missing
try:
    user = User(id=1, name="John")  # Missing email
except ValueError as e:
    print(f"Validation error: {e}")

# Convert to dict
print(user.dict())
# {'id': 1, 'name': 'John', 'email': 'john@example.com', 'age': None, 'is_active': True}

# Convert to JSON
print(user.json())
# {"id":1,"name":"John","email":"john@example.com","age":null,"is_active":true}

# Create from dict
data = {"id": 2, "name": "Jane", "email": "jane@example.com", "age": 25}
user2 = User(**data)

# Create from JSON
json_str = '{"id": 3, "name": "Bob", "email": "bob@example.com"}'
user3 = User.parse_raw(json_str)
"""
        print(code)

    def demonstrate_field_types(self) -> None:
        """Demonstrate different field types."""
        print("\nFIELD TYPES")
        print("=" * 60)

        code = """
from pydantic import BaseModel, HttpUrl, EmailStr, SecretStr, UUID4
from typing import Optional, List, Dict, Set, Tuple
from datetime import datetime, date, time
from decimal import Decimal
from uuid import UUID

class CompleteModel(BaseModel):
    # Basic types
    integer: int
    floating: float
    string: str
    boolean: bool

    # Optional
    optional_str: Optional[str] = None

    # Collections
    list_of_ints: List[int]
    dict_str_int: Dict[str, int]
    set_of_strs: Set[str]
    tuple_mixed: Tuple[int, str, float]

    # Date and time
    datetime_field: datetime
    date_field: date
    time_field: time

    # Special types
    email: EmailStr  # Validates email format
    url: HttpUrl  # Validates URL format
    uuid: UUID4  # Validates UUID4 format
    secret: SecretStr  # Hides value when printed
    decimal_field: Decimal  # Precise decimal numbers

    # With defaults
    status: str = "active"
    created_at: datetime = datetime.now()
    tags: List[str] = []
    metadata: Dict[str, any] = {}

# Example usage
model = CompleteModel(
    integer=42,
    floating=3.14,
    string="hello",
    boolean=True,
    list_of_ints=[1, 2, 3],
    dict_str_int={"a": 1, "b": 2},
    set_of_strs={"x", "y", "z"},
    tuple_mixed=(1, "hello", 3.14),
    datetime_field=datetime.now(),
    date_field=date.today(),
    time_field=time(12, 30, 0),
    email="user@example.com",
    url="https://example.com",
    uuid="550e8400-e29b-41d4-a716-446655440000",
    secret="my_secret_password"
)

print(model.email)  # user@example.com
print(model.secret)  # **********
print(model.secret.get_secret_value())  # my_secret_password
"""
        print(code)

    def demonstrate_field_constraints(self) -> None:
        """Demonstrate Field with constraints."""
        print("\nFIELD CONSTRAINTS")
        print("=" * 60)

        code = """
from pydantic import BaseModel, Field
from typing import Optional, List

class Product(BaseModel):
    # String constraints
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    sku: str = Field(..., regex=r'^[A-Z]{3}-\\d{4}$')

    # Numeric constraints
    price: float = Field(..., gt=0, description="Price must be positive")
    quantity: int = Field(..., ge=0, le=10000)
    discount: Optional[float] = Field(None, ge=0, le=100)
    rating: float = Field(5.0, ge=0, le=5)

    # Collection constraints
    tags: List[str] = Field(default=[], max_items=10)
    images: List[str] = Field(..., min_items=1, max_items=5)

    # Const value
    version: str = Field("1.0", const=True)

    # Exclude from export
    internal_id: int = Field(..., exclude=True)

    # Add example for documentation
    class Config:
        schema_extra = {
            "example": {
                "name": "Laptop",
                "description": "High-performance laptop",
                "sku": "LAP-1234",
                "price": 999.99,
                "quantity": 50,
                "tags": ["electronics", "computers"],
                "images": ["laptop1.jpg"]
            }
        }

# Field parameters:
# - ... (Ellipsis): Required field
# - default: Default value
# - default_factory: Callable that returns default
# - alias: Alternative name for field
# - title: Title for field (in JSON schema)
# - description: Description for field
# - const: Field must have this exact value
# - gt: Greater than
# - ge: Greater than or equal
# - lt: Less than
# - le: Less than or equal
# - multiple_of: Must be multiple of this value
# - min_length: Minimum length (strings, collections)
# - max_length: Maximum length (strings, collections)
# - min_items: Minimum items (collections)
# - max_items: Maximum items (collections)
# - regex: Regex pattern (strings)
# - exclude: Exclude from dict/JSON export
"""
        print(code)

    def demonstrate_validators(self) -> None:
        """Demonstrate custom validators."""
        print("\nCUSTOM VALIDATORS")
        print("=" * 60)

        code = """
from pydantic import BaseModel, validator, root_validator
from datetime import datetime

class User(BaseModel):
    username: str
    password: str
    password_confirm: str
    email: str
    age: int
    joined_date: datetime

    # Field validator
    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v

    # Validator with transformation
    @validator('email')
    def email_lowercase(cls, v):
        return v.lower()

    # Validator that checks multiple conditions
    @validator('password')
    def password_strong(cls, v):
        if len(v) < 8:
            raise ValueError('must be at least 8 characters')
        if not any(char.isdigit() for char in v):
            raise ValueError('must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('must contain at least one uppercase letter')
        return v

    # Validator with access to other fields
    @validator('password_confirm')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v

    # Validator that runs before type coercion
    @validator('age', pre=True)
    def age_as_string(cls, v):
        if isinstance(v, str):
            return int(v)
        return v

    # Validate multiple fields
    @validator('username', 'password', 'email')
    def not_empty(cls, v):
        if not v:
            raise ValueError('cannot be empty')
        return v

    # Root validator - validate entire model
    @root_validator
    def check_age_and_date(cls, values):
        age = values.get('age')
        joined = values.get('joined_date')

        if age and age < 18:
            raise ValueError('must be 18 or older')

        if joined and joined > datetime.now():
            raise ValueError('joined_date cannot be in future')

        return values

    # Root validator with skip_on_failure
    @root_validator(skip_on_failure=True)
    def final_checks(cls, values):
        # Only runs if all field validators passed
        return values

# Usage
user = User(
    username="john123",
    password="SecurePass123",
    password_confirm="SecurePass123",
    email="JOHN@EXAMPLE.COM",
    age="25",
    joined_date=datetime.now()
)

print(user.email)  # john@example.com (lowercased)
"""
        print(code)

    def demonstrate_nested_models(self) -> None:
        """Demonstrate nested models."""
        print("\nNESTED MODELS")
        print("=" * 60)

        code = """
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Nested model
class Address(BaseModel):
    street: str
    city: str
    country: str
    postal_code: str

class User(BaseModel):
    name: str
    email: str
    address: Address  # Nested model

# Create with nested data
user = User(
    name="John",
    email="john@example.com",
    address={
        "street": "123 Main St",
        "city": "New York",
        "country": "USA",
        "postal_code": "10001"
    }
)

print(user.address.city)  # New York

# List of nested models
class Comment(BaseModel):
    text: str
    author: str
    created_at: datetime

class Post(BaseModel):
    title: str
    content: str
    author: User
    comments: List[Comment] = []

post = Post(
    title="My Post",
    content="Post content",
    author=user,
    comments=[
        {"text": "Great!", "author": "Alice", "created_at": datetime.now()},
        {"text": "Thanks", "author": "Bob", "created_at": datetime.now()}
    ]
)

# Deeply nested
class Tag(BaseModel):
    name: str

class Category(BaseModel):
    name: str
    tags: List[Tag]

class Article(BaseModel):
    title: str
    categories: List[Category]

article = Article(
    title="Article",
    categories=[
        {
            "name": "Tech",
            "tags": [{"name": "Python"}, {"name": "FastAPI"}]
        }
    ]
)

# Optional nested
class Profile(BaseModel):
    bio: str
    avatar: Optional[str] = None

class UserWithProfile(BaseModel):
    name: str
    profile: Optional[Profile] = None

# Self-referencing models
class TreeNode(BaseModel):
    value: int
    children: List['TreeNode'] = []

TreeNode.update_forward_refs()  # Required for self-reference

tree = TreeNode(
    value=1,
    children=[
        TreeNode(value=2),
        TreeNode(value=3, children=[TreeNode(value=4)])
    ]
)
"""
        print(code)

    def demonstrate_model_config(self) -> None:
        """Demonstrate model configuration."""
        print("\nMODEL CONFIGURATION")
        print("=" * 60)

        code = """
from pydantic import BaseModel, Field

class User(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        # Allow arbitrary types (not just Pydantic models)
        arbitrary_types_allowed = False

        # Validate on assignment (not just initialization)
        validate_assignment = True

        # Use enum values instead of enum instances
        use_enum_values = True

        # Allow population by field name
        allow_population_by_field_name = True

        # Extra fields behavior
        extra = 'forbid'  # 'allow', 'ignore', or 'forbid'

        # Customize JSON encoder
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

        # Case sensitivity for aliases
        case_sensitive = False

        # Frozen (immutable)
        # frozen = True

        # ORM mode (work with ORMs)
        orm_mode = True

        # Schema customization
        title = 'User Model'
        schema_extra = {
            "example": {
                "id": 1,
                "name": "John",
                "email": "john@example.com"
            }
        }

# Validate on assignment example
user = User(id=1, name="John", email="john@example.com")
user.email = "invalid"  # Validates on assignment

# Extra fields
class StrictUser(BaseModel):
    name: str

    class Config:
        extra = 'forbid'

try:
    user = StrictUser(name="John", age=25)  # Error: extra field
except ValueError as e:
    print(e)

# ORM mode example
class UserORM:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

class UserPydantic(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

orm_user = UserORM(1, "John", "john@example.com")
pydantic_user = UserPydantic.from_orm(orm_user)
"""
        print(code)

    def demonstrate_serialization(self) -> None:
        """Demonstrate serialization and deserialization."""
        print("\nSERIALIZATION")
        print("=" * 60)

        code = """
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: int
    name: str
    email: str
    password: str = Field(..., exclude=True)
    created_at: datetime
    metadata: dict = {}

user = User(
    id=1,
    name="John",
    email="john@example.com",
    password="secret",
    created_at=datetime.now(),
    metadata={"role": "admin"}
)

# To dict
print(user.dict())
# {'id': 1, 'name': 'John', ...}

# To dict excluding fields
print(user.dict(exclude={'password'}))
print(user.dict(exclude={'created_at', 'metadata'}))

# To dict including only specific fields
print(user.dict(include={'id', 'name', 'email'}))

# To dict excluding unset fields
print(user.dict(exclude_unset=True))

# To dict excluding defaults
print(user.dict(exclude_defaults=True))

# To dict excluding None values
print(user.dict(exclude_none=True))

# To JSON
json_str = user.json()
print(json_str)

# To JSON with custom options
json_str = user.json(
    exclude={'password'},
    indent=2,
    ensure_ascii=False
)

# From dict
data = {"id": 2, "name": "Jane", "email": "jane@example.com",
        "password": "secret", "created_at": "2024-01-01T12:00:00"}
user2 = User(**data)

# From JSON
json_str = '{"id": 3, "name": "Bob", "email": "bob@example.com",
             "password": "secret", "created_at": "2024-01-01T12:00:00"}'
user3 = User.parse_raw(json_str)

# From file
# user4 = User.parse_file('user.json')

# Schema generation
schema = User.schema()
print(schema)

# Schema as JSON
import json
print(json.dumps(User.schema(), indent=2))
"""
        print(code)

    def demonstrate_advanced_features(self) -> None:
        """Demonstrate advanced Pydantic features."""
        print("\nADVANCED FEATURES")
        print("=" * 60)

        print("\n1. Generics:")
        print("-" * 60)
        code = """
from pydantic import BaseModel
from pydantic.generics import GenericModel
from typing import Generic, TypeVar, List

T = TypeVar('T')

class Response(GenericModel, Generic[T]):
    data: T
    status: int
    message: str

class User(BaseModel):
    name: str
    email: str

# Use with different types
user_response = Response[User](
    data=User(name="John", email="john@example.com"),
    status=200,
    message="Success"
)

list_response = Response[List[str]](
    data=["a", "b", "c"],
    status=200,
    message="Success"
)
"""
        print(code)

        print("2. Dynamic Model Creation:")
        print("-" * 60)
        code = """
from pydantic import create_model

# Create model dynamically
DynamicUser = create_model(
    'DynamicUser',
    id=(int, ...),
    name=(str, ...),
    email=(str, ...)
)

user = DynamicUser(id=1, name="John", email="john@example.com")

# With Field
from pydantic import Field

DynamicProduct = create_model(
    'DynamicProduct',
    name=(str, Field(..., min_length=1)),
    price=(float, Field(..., gt=0))
)
"""
        print(code)

        print("3. Model Copy and Update:")
        print("-" * 60)
        code = """
user = User(id=1, name="John", email="john@example.com")

# Shallow copy
user_copy = user.copy()

# Copy with update
user_updated = user.copy(update={"name": "Jane"})

# Deep copy
user_deep = user.copy(deep=True)
"""
        print(code)


def main() -> None:
    """Main entry point demonstrating Pydantic models."""
    print("\n" + "=" * 60)
    print("PROGRAM 48: PYDANTIC MODELS")
    print("=" * 60 + "\n")

    demo = PydanticModelsDemo()

    demo.demonstrate_basic_models()
    demo.demonstrate_field_types()
    demo.demonstrate_field_constraints()
    demo.demonstrate_validators()
    demo.demonstrate_nested_models()
    demo.demonstrate_model_config()
    demo.demonstrate_serialization()
    demo.demonstrate_advanced_features()

    print("\n" + "=" * 60)
    print("PYDANTIC BEST PRACTICES")
    print("=" * 60)
    print("1. Use Field() for constraints and metadata")
    print("2. Add validators for complex business logic")
    print("3. Use proper type hints for auto-validation")
    print("4. Leverage nested models for structure")
    print("5. Use Config class for model behavior")
    print("6. Exclude sensitive fields from serialization")
    print("7. Use ORM mode for database models")
    print("8. Add examples in schema_extra for docs")
    print("9. Use root_validators for cross-field validation")
    print("10. Generate JSON schemas for documentation")
    print("=" * 60)


if __name__ == "__main__":
    main()
