# Program 177: std::string_view

## Description
Demonstrates std::string_view (C++17), a non-owning reference to a string, providing efficient string access without copying or memory allocation.

## Learning Objectives
- Use string_view for efficient string passing
- Understand non-owning semantics
- Work with string_view operations
- Avoid dangling string_views
- Convert between string and string_view

## Features
- Basic string_view usage
- View operations (substr, remove_prefix, remove_suffix)
- Comparison and searching
- String_view in function parameters
- Literal suffix _sv
- Performance benefits

## Compilation
```bash
g++ -std=c++17 main.cpp -o string_view
./string_view
```

## Key Concepts
```cpp
void process(string_view sv) {  // No copy!
    cout << sv;
}

string s = "hello world";
string_view sv = s;
sv.remove_prefix(6);  // sv now "world"

using namespace std::literals;
auto sv2 = "hello"sv;  // string_view literal
```

## Best Practices
1. Use string_view for read-only string parameters
2. Be careful with lifetime - string_view doesn't own data
3. Don't return string_view from functions (usually)
4. Prefer over const string& for parameters
5. Watch for null terminators

## Navigation
- **Previous**: [176 - Std Any](/home/user/DevOps-prj500/101-200_CPP/176_std_any/README.md)
- **Next**: [178 - Span](/home/user/DevOps-prj500/101-200_CPP/178_span/README.md)
