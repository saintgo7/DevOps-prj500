# Program 157: C++20 Concepts

## Description
This program demonstrates C++20 Concepts, a revolutionary feature that provides named constraints on template parameters, making generic programming more accessible with clearer syntax and better error messages than SFINAE.

## Learning Objectives
- Understand C++20 concept syntax and definition
- Use requires clauses and requires expressions
- Apply standard library concepts
- Create custom concepts
- Compose concepts with logical operators
- Use abbreviated function templates
- Compare concepts with SFINAE

## Features
- Basic concept definitions
- requires clause (three syntaxes)
- requires expression components
- Standard library concepts (integral, copyable, etc.)
- Custom concept creation
- Concept composition (&&, ||, !)
- Abbreviated function templates
- Concepts with class templates
- Practical type-safe examples

## Compilation and Usage

```bash
# Requires C++20
g++ -std=c++20 main.cpp -o concepts
cd /home/user/DevOps-prj500/101-200_CPP/157_concepts
mkdir -p build && cd build && cmake .. && make
./concepts
```

## Key Concepts

### Basic Concept Definition
```cpp
template<typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

template<typename T>
concept Addable = requires(T a, T b) {
    { a + b } -> std::same_as<T>;
};
```

### Three Syntax Styles
```cpp
// 1. Concept as template parameter
template<Numeric T>
T add(T a, T b);

// 2. requires clause after template
template<typename T> requires Numeric<T>
T multiply(T a, T b);

// 3. requires clause after parameters
template<typename T>
T subtract(T a, T b) requires Numeric<T>;
```

### Abbreviated Function Templates
```cpp
void print(Printable auto value) {
    std::cout << value;
}

auto square(Numeric auto x) {
    return x * x;
}
```

### Custom Concepts
```cpp
template<typename T>
concept Container = requires(T t) {
    typename T::value_type;
    typename T::iterator;
    { t.begin() } -> std::same_as<typename T::iterator>;
    { t.end() } -> std::same_as<typename T::iterator>;
    { t.size() } -> std::convertible_to<size_t>;
};
```

## Best Practices
1. **Prefer concepts over SFINAE**: Clearer and better error messages
2. **Use standard concepts when available**: Don't reinvent common constraints
3. **Name concepts clearly**: Self-documenting code
4. **Compose concepts**: Build complex constraints from simple ones
5. **Use abbreviated syntax**: More concise for simple cases

## Resources/References
- [cppreference: Concepts](https://en.cppreference.com/w/cpp/language/constraints)
- [C++20 Concepts Tutorial](https://www.modernescpp.com/index.php/c-20-concepts-the-details)
- [Standard Library Concepts](https://en.cppreference.com/w/cpp/concepts)

## Navigation
- **Previous**: [156 - Template Metaprogramming](/home/user/DevOps-prj500/101-200_CPP/156_template_metaprogramming/README.md)
- **Next**: [158 - Ranges](/home/user/DevOps-prj500/101-200_CPP/158_ranges/README.md)
