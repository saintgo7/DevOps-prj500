# Program 152: Function Templates

## Description
This program demonstrates advanced function template concepts in C++, including template argument deduction, function template overloading, specialization, perfect forwarding, and auto return type deduction. It shows how function templates enable generic, type-safe algorithms.

## Learning Objectives
- Master function template syntax and usage patterns
- Understand template argument deduction rules
- Learn function template overloading resolution
- Implement function template specialization
- Apply perfect forwarding techniques
- Use auto return type deduction effectively
- Work with constexpr function templates

## Features
- Basic function template definitions
- Multiple type parameter templates
- Template argument deduction (automatic and explicit)
- Function template overloading with priority rules
- Full function template specialization
- Perfect forwarding with `std::forward`
- Auto return type deduction
- Constexpr function templates
- SFINAE with `enable_if` (preview)
- Variadic function templates (preview)

## Compilation and Usage

### Compilation
```bash
# Using g++
g++ -std=c++17 main.cpp -o function_templates

# Using CMake
cd /home/user/DevOps-prj500/101-200_CPP/152_function_templates
mkdir -p build && cd build
cmake ..
make
```

### Execution
```bash
./function_templates
```

## Key Concepts

### 1. Basic Function Templates
```cpp
template<typename T>
T maximum(T a, T b) {
    return (a > b) ? a : b;
}

template<typename T>
void swap_values(T& a, T& b) {
    T temp = a;
    a = b;
    b = temp;
}
```

### 2. Multiple Type Parameters
```cpp
template<typename T, typename U>
auto add(T a, U b) -> decltype(a + b) {
    return a + b;
}

template<typename T, typename U>
pair<T, U> make_ordered_pair(T first, U second) {
    return pair<T, U>(first, second);
}
```

### 3. Function Template Overloading
```cpp
template<typename T>
void print(T value);          // Generic version

template<typename T>
void print(T* ptr);           // Pointer specialization

void print(int value);        // Non-template (preferred for exact match)

template<typename T, typename U>
void print(T first, U second); // Two-parameter version
```

**Overload Priority**:
1. Non-template functions (exact match)
2. Template specializations
3. Generic templates

### 4. Function Template Specialization
```cpp
template<typename T>
T absolute(T value) {
    return value < 0 ? -value : value;
}

template<>
string absolute<string>(string value) {
    return "String has no absolute value: " + value;
}
```

### 5. Perfect Forwarding
```cpp
template<typename Func, typename... Args>
auto call_function(Func&& func, Args&&... args)
    -> decltype(func(forward<Args>(args)...)) {
    return func(forward<Args>(args)...);
}
```

### 6. Auto Return Type Deduction
```cpp
// C++14 style
template<typename T, typename U>
auto multiply(T a, U b) {
    return a * b;  // Return type deduced
}

// Trailing return type (C++11)
template<typename Container>
auto getFirst(const Container& c) -> decltype(c.front()) {
    return c.front();
}
```

### 7. Constexpr Function Templates
```cpp
template<typename T>
constexpr T square(T value) {
    return value * value;
}

constexpr int result = square(5);  // Computed at compile-time
int arr[square(3)];                // Array of size 9
```

## Best Practices
1. **Use explicit template arguments when needed**:
   ```cpp
   maximum<double>(10, 20);  // Forces double arithmetic
   ```

2. **Prefer auto return type deduction** (C++14+):
   ```cpp
   template<typename T, typename U>
   auto add(T a, U b) { return a + b; }
   ```

3. **Use perfect forwarding for wrapper functions**:
   ```cpp
   template<typename Func, typename... Args>
   auto wrapper(Func&& f, Args&&... args) {
       return f(forward<Args>(args)...);
   }
   ```

4. **Leverage constexpr for compile-time computation**:
   ```cpp
   template<typename T>
   constexpr T factorial(T n) {
       return n <= 1 ? 1 : n * factorial(n - 1);
   }
   ```

5. **Use SFINAE/concepts for constraints**:
   ```cpp
   template<typename T>
   enable_if_t<is_integral<T>::value, T>
   safe_divide(T a, T b);
   ```

6. **Document template requirements**: Clearly specify what operations T must support

7. **Prefer function templates over macros**: Type-safe and debuggable

## Resources/References
- [cppreference: Function Templates](https://en.cppreference.com/w/cpp/language/function_template)
- [Perfect Forwarding Guide](https://www.cplusplus.com/articles/EN3hAqkS/)
- [C++ Template Specialization](https://en.cppreference.com/w/cpp/language/template_specialization)
- [Auto Type Deduction](https://en.cppreference.com/w/cpp/language/auto)

## Navigation
- **Previous Program**: [151 - Templates Basics](/home/user/DevOps-prj500/101-200_CPP/151_templates_basics/README.md)
- **Next Program**: [153 - Class Templates](/home/user/DevOps-prj500/101-200_CPP/153_class_templates/README.md)
- **Back to Main Index**: [README](/home/user/DevOps-prj500/README.md)
