# Program 161: Move and Forward

## Description
This program demonstrates std::move and std::forward, two essential utilities in modern C++ for working with rvalue references, move semantics, and perfect forwarding.

## Learning Objectives
- Understand std::move and its purpose
- Master std::forward for perfect forwarding
- Distinguish between lvalue and rvalue references
- Implement move constructors and move assignment
- Apply universal references (forwarding references)
- Optimize code with move semantics

## Features
- std::move demonstration
- std::forward usage
- Move constructor and move assignment implementation
- Lvalue vs rvalue reference examples
- Universal references
- Perfect forwarding patterns
- Performance comparisons

## Compilation and Usage
```bash
g++ -std=c++17 main.cpp -o move_forward
cd /home/user/DevOps-prj500/101-200_CPP/161_move_forward
mkdir -p build && cd build && cmake .. && make
./move_forward
```

## Key Concepts

### std::move
```cpp
string s1 = "Hello";
string s2 = std::move(s1);  // s1 is now in valid but unspecified state
```

### std::forward
```cpp
template<typename T>
void wrapper(T&& arg) {
    func(std::forward<T>(arg));  // Preserves value category
}
```

## Best Practices
1. Use std::move when transferring ownership
2. Apply std::forward in forwarding functions
3. Don't use moved-from objects except to destroy or reassign
4. Return by value, let compiler optimize
5. Implement move operations for resource-owning classes

## Resources
- [cppreference: std::move](https://en.cppreference.com/w/cpp/utility/move)
- [cppreference: std::forward](https://en.cppreference.com/w/cpp/utility/forward)

## Navigation
- **Previous**: [160 - SFINAE](/home/user/DevOps-prj500/101-200_CPP/160_sfinae/README.md)
- **Next**: [162 - Perfect Forwarding](/home/user/DevOps-prj500/101-200_CPP/162_perfect_forwarding/README.md)
