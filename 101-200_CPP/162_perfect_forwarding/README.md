# Program 162: Perfect Forwarding

## Description
This program explores perfect forwarding in depth, showing how to write wrapper functions that preserve the value category (lvalue/rvalue) of arguments using universal references and std::forward.

## Learning Objectives
- Master perfect forwarding technique
- Understand universal/forwarding references (T&&)
- Implement wrapper functions correctly
- Use variadic templates with perfect forwarding
- Apply perfect forwarding in factory functions

## Features
- Universal reference patterns
- Perfect forwarding with std::forward
- Variadic template forwarding
- Factory function implementation (make_unique pattern)
- Wrapper function examples
- Value category preservation

## Compilation and Usage
```bash
g++ -std=c++17 main.cpp -o perfect_forwarding
./perfect_forwarding
```

## Key Concepts

### Universal References
```cpp
template<typename T>
void func(T&& param);  // T&& is universal reference, not rvalue reference
```

### Perfect Forwarding Pattern
```cpp
template<typename T, typename... Args>
unique_ptr<T> make_unique(Args&&... args) {
    return unique_ptr<T>(new T(std::forward<Args>(args)...));
}
```

## Best Practices
1. Use T&& in template context for universal references
2. Always std::forward universal references
3. Don't forward the same argument twice
4. Document forwarding functions clearly

## Resources
- [Perfect Forwarding](https://en.cppreference.com/w/cpp/utility/forward)
- [Universal References](https://isocpp.org/blog/2012/11/universal-references-in-c11-scott-meyers)

## Navigation
- **Previous**: [161 - Move Forward](/home/user/DevOps-prj500/101-200_CPP/161_move_forward/README.md)
- **Next**: [163 - Multithreading](/home/user/DevOps-prj500/101-200_CPP/163_multithreading/README.md)
