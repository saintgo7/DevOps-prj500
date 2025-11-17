# Program 155: Variadic Templates

## Description
This program explores variadic templates, a powerful C++ feature that allows templates to accept any number of arguments. It demonstrates parameter packs, pack expansion, recursive templates, fold expressions (C++17), and practical applications of variadic templates.

## Learning Objectives
- Understand variadic template syntax and parameter packs
- Master pack expansion techniques
- Implement recursive variadic templates
- Use C++17 fold expressions
- Apply perfect forwarding with variadic templates
- Create variadic class templates
- Work with index sequences
- Build type-safe variadic functions

## Features
- Basic variadic template syntax
- Parameter pack expansion patterns
- Recursive variadic template implementation
- C++17 fold expressions (unary and binary)
- Perfect forwarding with variadic arguments
- Variadic class templates
- Index sequence generation and usage
- Type traits with variadic templates
- Practical logger implementation

## Compilation and Usage

```bash
# Using g++ (requires C++17 for fold expressions)
g++ -std=c++17 main.cpp -o variadic_templates

# Using CMake
cd /home/user/DevOps-prj500/101-200_CPP/155_variadic_templates
mkdir -p build && cd build
cmake && make
./variadic_templates
```

## Key Concepts

### 1. Basic Variadic Template
```cpp
template<typename... Args>
void print_all(Args... args) {
    ((cout << args << " "), ...);  // Fold expression
}

print_all(1, 2, 3, "hello", 3.14);
```

### 2. Recursive Variadic Templates
```cpp
template<typename T>
T sum(T value) {
    return value;
}

template<typename T, typename... Args>
T sum(T first, Args... rest) {
    return first + sum(rest...);
}
```

### 3. Fold Expressions (C++17)
```cpp
template<typename... Args>
auto sum_fold(Args... args) {
    return (args + ...);  // Unary right fold
}

template<typename... Args>
bool all_true(Args... args) {
    return (args && ...);
}
```

### 4. Perfect Forwarding
```cpp
template<typename... Args>
void forward_to_print(Args&&... args) {
    print_all(forward<Args>(args)...);
}

template<typename T, typename... Args>
unique_ptr<T> make_unique_variadic(Args&&... args) {
    return unique_ptr<T>(new T(forward<Args>(args)...));
}
```

### 5. Variadic Class Templates
```cpp
template<typename... Types>
class Tuple;

template<typename Head, typename... Tail>
class Tuple<Head, Tail...> : private Tuple<Tail...> {
    Head head;
public:
    Tuple(Head h, Tail... t) : Tuple<Tail...>(t...), head(h) {}
};
```

### 6. sizeof... Operator
```cpp
template<typename... Args>
void print_count() {
    cout << "Arguments: " << sizeof...(Args);
}
```

## Best Practices
1. **Use fold expressions when possible**: Simpler than recursion (C++17+)
2. **Perfect forward variadic arguments**: Preserve value categories
3. **Provide base cases for recursion**: Essential for compile termination
4. **Use `sizeof...` for parameter count**: Compile-time information
5. **Combine with SFINAE/concepts**: Constrain template parameters
6. **Document variadic interfaces**: Explain expected argument types

## Resources/References
- [cppreference: Parameter Pack](https://en.cppreference.com/w/cpp/language/parameter_pack)
- [Fold Expressions](https://en.cppreference.com/w/cpp/language/fold)
- [Variadic Templates Tutorial](https://eli.thegreenplace.net/2014/variadic-templates-in-c/)

## Navigation
- **Previous Program**: [154 - Template Specialization](/home/user/DevOps-prj500/101-200_CPP/154_template_specialization/README.md)
- **Next Program**: [156 - Template Metaprogramming](/home/user/DevOps-prj500/101-200_CPP/156_template_metaprogramming/README.md)
- **Back to Main Index**: [README](/home/user/DevOps-prj500/README.md)
