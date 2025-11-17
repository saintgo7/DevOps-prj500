# Program 159: Type Traits

## Description
This program demonstrates the type traits library in C++, which provides compile-time type information and transformations. Type traits enable powerful template metaprogramming and are foundational to modern C++ generic programming.

## Learning Objectives
- Understand primary type categories (is_integral, is_floating_point, etc.)
- Use composite type categories (is_arithmetic, is_fundamental)
- Query type properties (is_const, is_reference, is_signed)
- Check type relationships (is_same, is_base_of, is_convertible)
- Apply type transformations (remove_const, add_pointer, decay)
- Use SFINAE helpers (enable_if, conditional)
- Create custom type traits

## Features
- Primary type categories
- Composite type categories
- Type properties checking
- Type relationship queries
- Type transformations (removing/adding qualifiers)
- enable_if and conditional usage
- decay type trait
- Custom type traits implementation
- Practical type-safe function overloading

## Compilation and Usage

```bash
g++ -std=c++17 main.cpp -o type_traits
cd /home/user/DevOps-prj500/101-200_CPP/159_type_traits
mkdir -p build && cd build && cmake .. && make
./type_traits
```

## Key Concepts

### Primary Type Categories
```cpp
is_integral<int>::value        // true
is_floating_point<double>::value  // true
is_array<int[10]>::value       // true
is_pointer<int*>::value        // true
is_class<string>::value        // true
```

### Type Transformations
```cpp
remove_const<const int>::type       // int
remove_reference<int&>::type        // int
remove_pointer<int*>::type          // int
add_const<int>::type                // const int
add_pointer<int>::type              // int*
decay<int&>::type                   // int
```

### enable_if for SFINAE
```cpp
template<typename T>
enable_if_t<is_integral<T>::value, T>
safe_divide(T a, T b) {
    return b != 0 ? a / b : 0;
}
```

### Custom Type Traits
```cpp
template<typename T>
struct is_container {
private:
    template<typename U>
    static auto test(int) -> decltype(
        declval<U>().begin(),
        declval<U>().end(),
        true_type{}
    );
    
    template<typename>
    static false_type test(...);
    
public:
    static constexpr bool value = decltype(test<T>(0))::value;
};
```

## Best Practices
1. **Use _v and _t suffixes** (C++17): `is_integral_v<T>` instead of `is_integral<T>::value`
2. **Prefer concepts in C++20**: More readable than type traits + SFINAE
3. **Combine traits for complex conditions**: Build sophisticated compile-time checks
4. **Use decay for generic code**: Handles references, arrays, and functions
5. **Document trait requirements**: Make template constraints clear

## Resources/References
- [cppreference: Type Traits](https://en.cppreference.com/w/cpp/header/type_traits)
- [Type Traits Tutorial](https://www.modernescpp.com/index.php/type-traits-performance-matters)

## Navigation
- **Previous**: [158 - Ranges](/home/user/DevOps-prj500/101-200_CPP/158_ranges/README.md)
- **Next**: [160 - SFINAE](/home/user/DevOps-prj500/101-200_CPP/160_sfinae/README.md)
