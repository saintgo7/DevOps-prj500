# Program 154: Template Specialization

## Description
This program demonstrates template specialization techniques in C++, including full (explicit) specialization, partial specialization for classes, pointer specializations, member function specialization, tag dispatch patterns, and SFINAE basics.

## Learning Objectives
- Master full template specialization for functions and classes
- Understand partial template specialization (classes only)
- Implement specializations for pointer types
- Use member function specialization
- Apply tag dispatch patterns for optimization
- Learn SFINAE (Substitution Failure Is Not An Error) basics
- Understand when to use each specialization technique

## Features
- Function template full specialization
- Class template full specialization
- Partial class template specialization
- Pointer type specializations
- Member function specialization
- Tag dispatch pattern implementation
- SFINAE with `enable_if`
- Type-specific optimizations
- Practical type-safe examples

## Compilation and Usage

```bash
# Using g++
g++ -std=c++17 main.cpp -o template_specialization

# Using CMake
cd /home/user/DevOps-prj500/101-200_CPP/154_template_specialization
mkdir -p build && cd build
cmake && make
./template_specialization
```

## Key Concepts

### 1. Function Template Specialization
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

### 2. Class Template Specialization
```cpp
template<typename T>
class Storage {
    T data;
};

template<>
class Storage<bool> {
    bool data;
    void toggle() { data = !data; }
};
```

### 3. Partial Specialization (Classes Only)
```cpp
template<typename T, typename U>
class Pair { /* generic */ };

template<typename T>
class Pair<T, T> { /* both types same */ };

template<typename T, typename U>
class Pair<T, U*> { /* second is pointer */ };
```

### 4. Tag Dispatch
```cpp
struct int_tag {};
struct float_tag {};

template<typename T>
void process_impl(T value, int_tag);

template<typename T>
void process_impl(T value, float_tag);

template<typename T>
void process(T value) {
    process_impl(value, typename type_tag<T>::type());
}
```

## Best Practices
1. **Use specialization for truly different behavior**: Not for minor variations
2. **Prefer partial specialization**: More flexible than full specialization
3. **Consider tag dispatch**: Often cleaner than multiple specializations
4. **Document specialized behavior**: Clearly explain why specialization is needed
5. **Test all specializations**: Each specialization is a separate implementation
6. **In modern C++, prefer concepts**: More expressive than SFINAE

## Resources/References
- [cppreference: Template Specialization](https://en.cppreference.com/w/cpp/language/template_specialization)
- [Partial Specialization](https://en.cppreference.com/w/cpp/language/partial_specialization)
- [SFINAE](https://en.cppreference.com/w/cpp/language/sfinae)

## Navigation
- **Previous Program**: [153 - Class Templates](/home/user/DevOps-prj500/101-200_CPP/153_class_templates/README.md)
- **Next Program**: [155 - Variadic Templates](/home/user/DevOps-prj500/101-200_CPP/155_variadic_templates/README.md)
- **Back to Main Index**: [README](/home/user/DevOps-prj500/README.md)
