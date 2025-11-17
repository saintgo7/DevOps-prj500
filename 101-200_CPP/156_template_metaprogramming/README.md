# Program 156: Template Metaprogramming

## Description
This program demonstrates template metaprogramming techniques in C++, showing how templates can be used for compile-time computation, type manipulation, and algorithmic problem-solving without runtime overhead.

## Learning Objectives
- Understand compile-time vs runtime computation
- Master recursive template techniques
- Implement type computations and transformations
- Use conditional types and type lists
- Compare constexpr with template metaprogramming
- Apply SFINAE and enable_if patterns
- Create compile-time algorithms

## Features
- Compile-time factorial and Fibonacci
- Type transformations (remove/add const, pointer, etc.)
- Conditional type selection
- Type list manipulation
- constexpr vs template metaprogramming comparison
- SFINAE and enable_if usage
- Compile-time algorithms (is_prime, string_length)
- Template metafunctions
- Static assertions
- Practical unit conversion example

## Compilation and Usage

```bash
g++ -std=c++17 main.cpp -o template_metaprogramming
cd /home/user/DevOps-prj500/101-200_CPP/156_template_metaprogramming
mkdir -p build && cd build && cmake .. && make
./template_metaprogramming
```

## Key Concepts

### Compile-Time Factorial
```cpp
template<int N>
struct Factorial {
    static constexpr int value = N * Factorial<N - 1>::value;
};

template<>
struct Factorial<0> {
    static constexpr int value = 1;
};
```

### Type Transformations
```cpp
template<typename T>
struct RemovePointer { using type = T; };

template<typename T>
struct RemovePointer<T*> { using type = T; };
```

### Conditional Types
```cpp
template<bool Condition, typename TrueType, typename FalseType>
struct Conditional {
    using type = TrueType;
};

template<typename TrueType, typename FalseType>
struct Conditional<false, TrueType, FalseType> {
    using type = FalseType;
};
```

## Best Practices
1. **Prefer constexpr in modern C++**: More readable than template metaprogramming
2. **Use static_assert**: Verify compile-time conditions
3. **Document metafunctions**: Complex template code needs clear documentation
4. **Consider compilation time**: Template metaprogramming can slow builds
5. **Use type traits library**: Don't reinvent the wheel

## Resources/References
- [Template Metaprogramming](https://en.wikibooks.org/wiki/More_C%2B%2B_Idioms/Template_Metaprogramming)
- [constexpr](https://en.cppreference.com/w/cpp/language/constexpr)
- [Type Traits](https://en.cppreference.com/w/cpp/header/type_traits)

## Navigation
- **Previous**: [155 - Variadic Templates](/home/user/DevOps-prj500/101-200_CPP/155_variadic_templates/README.md)
- **Next**: [157 - Concepts](/home/user/DevOps-prj500/101-200_CPP/157_concepts/README.md)
