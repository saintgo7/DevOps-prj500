# Program 160: SFINAE

## Description
This program demonstrates SFINAE (Substitution Failure Is Not An Error), a core C++ template metaprogramming technique that enables conditional template instantiation and sophisticated compile-time dispatch mechanisms.

## Learning Objectives
- Understand the SFINAE principle
- Master enable_if patterns for function overloading
- Use SFINAE with class templates
- Apply decltype and declval for SFINAE
- Utilize void_t idiom (C++17)
- Implement detection idiom
- Apply tag dispatching patterns
- Compare SFINAE with C++20 Concepts

## Features
- SFINAE principle explanation
- enable_if patterns (return type, template param, function param)
- Function overloading with SFINAE
- Class template SFINAE
- decltype and declval usage
- void_t idiom for detection
- Detection idiom pattern
- Tag dispatching for optimization
- SFINAE vs Concepts comparison
- Practical generic programming examples

## Compilation and Usage

```bash
g++ -std=c++17 main.cpp -o sfinae
cd /home/user/DevOps-prj500/101-200_CPP/160_sfinae
mkdir -p build && cd build && cmake .. && make
./sfinae
```

## Key Concepts

### Basic SFINAE with enable_if
```cpp
template<typename T>
typename enable_if<is_integral<T>::value, T>::type
safe_divide(T a, T b) {
    return b != 0 ? a / b : 0;
}

// C++14 shorthand
template<typename T>
enable_if_t<is_floating_point<T>::value, T>
safe_divide(T a, T b) {
    return b != 0.0 ? a / b : 0.0;
}
```

### void_t Idiom (C++17)
```cpp
template<typename, typename = void>
struct has_size : false_type {};

template<typename T>
struct has_size<T, void_t<decltype(declval<T>().size())>> : true_type {};
```

### Detection Idiom
```cpp
template<typename T>
using size_type_t = typename T::size_type;

template<typename T, typename = void>
struct has_size_type : false_type {};

template<typename T>
struct has_size_type<T, void_t<size_type_t<T>>> : true_type {};
```

### Tag Dispatching
```cpp
struct has_fast_size {};
struct no_fast_size {};

template<typename T>
size_t get_size_impl(const T& container, has_fast_size) {
    return container.size();
}

template<typename T>
size_t get_size_impl(const T& container, no_fast_size) {
    return distance(container.begin(), container.end());
}
```

## Best Practices
1. **Prefer C++20 concepts**: Cleaner than SFINAE for new code
2. **Use void_t for detection**: Simpler than older SFINAE patterns
3. **Tag dispatch for performance**: Better than multiple SFINAE overloads
4. **Document SFINAE constraints**: Complex template code needs explanation
5. **Test edge cases**: SFINAE can have subtle behaviors

## Resources/References
- [cppreference: SFINAE](https://en.cppreference.com/w/cpp/language/sfinae)
- [Detection Idiom](https://en.cppreference.com/w/cpp/experimental/is_detected)
- [Modern C++ SFINAE](https://www.modernescpp.com/index.php/c-insights-SFINAE)

## Navigation
- **Previous**: [159 - Type Traits](/home/user/DevOps-prj500/101-200_CPP/159_type_traits/README.md)
- **Next**: [161 - Move Forward](/home/user/DevOps-prj500/101-200_CPP/161_move_forward/README.md)
