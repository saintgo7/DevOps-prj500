# Program 151: Templates Basics

## Description
This program provides a comprehensive introduction to C++ templates, covering the fundamental concepts of generic programming, template syntax, template parameters, instantiation, and common template patterns.

## Learning Objectives
- Understand template syntax and the generic programming paradigm
- Master type and non-type template parameters
- Learn template argument deduction mechanisms
- Work with default template arguments
- Understand the template compilation model
- Distinguish between `typename` and `class` keywords
- Apply common template design patterns

## Features
- Basic function and class templates
- Multiple template parameters demonstration
- Non-type template parameters (compile-time constants)
- Default template arguments
- Template argument deduction examples
- Template specialization preview
- Template template parameters
- RAII wrapper pattern
- Type traits integration
- Compile-time computation examples

## Compilation and Usage

### Compilation
```bash
# Using g++
g++ -std=c++17 main.cpp -o templates_basics

# Using CMake
cd /home/user/DevOps-prj500/101-200_CPP/151_templates_basics
mkdir -p build && cd build
cmake ..
make
```

### Execution
```bash
./templates_basics
```

## Key Concepts

### 1. Basic Template Syntax
```cpp
// Function template
template<typename T>
T maximum(T a, T b) {
    return (a > b) ? a : b;
}

// Class template
template<typename T>
class Box {
private:
    T value;
public:
    Box(T v) : value(v) {}
    T getValue() const { return value; }
};
```

### 2. Non-Type Template Parameters
```cpp
template<typename T, int Size>
class Array {
private:
    T data[Size];
public:
    int size() const { return Size; }
};

// Compile-time computation
template<int N>
int factorial() {
    return N * factorial<N-1>();
}
```

### 3. Template Argument Deduction
```cpp
template<typename T>
void printType(T value) {
    // T automatically deduced from argument
}

printType(42);      // T = int
printType(3.14);    // T = double
printType("hello"); // T = const char*
```

### 4. Default Template Arguments
```cpp
template<typename T = int, int Size = 10>
class Container {
    // Implementation
};

Container<> c1;           // Uses int, size 10
Container<double> c2;      // Uses double, size 10
Container<string, 5> c3;   // Uses string, size 5
```

## Best Practices
1. **Use `typename` over `class`**: More clear that you're referring to a type
2. **Define templates in headers**: Template definitions must be visible at instantiation
3. **Use const references**: Avoid unnecessary copying
   ```cpp
   template<typename T>
   void func(const T& value);
   ```
4. **Provide meaningful constraints**: Use static_assert for compile-time checks
5. **Document template requirements**: Clearly specify what operations T must support
6. **Consider template aliases**: Simplify complex template instantiations
   ```cpp
   template<typename T>
   using Vec = vector<T>;
   ```
7. **Use explicit instantiation when appropriate**: Control which types are supported and reduce compile time
8. **Leverage type traits**: Use `<type_traits>` for compile-time type checking

## Resources/References
- [C++ Templates - The Complete Guide](https://www.cplusplus.com/doc/oldtutorial/templates/)
- [cppreference: Templates](https://en.cppreference.com/w/cpp/language/templates)
- [Modern C++ Design](https://www.amazon.com/Modern-Design-Generic-Programming-Patterns/dp/0201704315)
- [Template Metaprogramming Guide](https://en.wikibooks.org/wiki/More_C%2B%2B_Idioms/Template_Metaprogramming)

## Navigation
- **Previous Program**: [150 - Lambda Expressions](/home/user/DevOps-prj500/101-200_CPP/150_lambda_expressions/README.md)
- **Next Program**: [152 - Function Templates](/home/user/DevOps-prj500/101-200_CPP/152_function_templates/README.md)
- **Back to Main Index**: [README](/home/user/DevOps-prj500/README.md)
