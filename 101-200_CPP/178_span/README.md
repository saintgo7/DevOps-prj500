# Program 178: std::span

## Description
Explores std::span (C++20), a non-owning view over a contiguous sequence of objects, providing a safe and efficient alternative to pointer-and-length pairs.

## Learning Objectives
- Use std::span for array/vector views
- Understand span semantics and lifetime
- Work with dynamic and fixed-extent spans
- Apply span for function parameters
- Use span operations (subspan, first, last)

## Features
- Basic span usage
- Dynamic vs fixed extent
- Span from arrays and vectors
- Subspan operations
- Span in function parameters
- Span iterators

## Compilation
```bash
g++ -std=c++20 main.cpp -o span
./span
```

## Key Concepts
```cpp
void process(std::span<int> data) {  // Works with array or vector
    for (int& elem : data) { /* process */ }
}

int arr[] = {1, 2, 3, 4, 5};
std::span<int> s = arr;

auto first3 = s.first(3);
auto last2 = s.last(2);
auto sub = s.subspan(1, 3);
```

## Best Practices
1. Use span for contiguous data parameters
2. Prefer over pointer + size pairs
3. Be aware of lifetime - span doesn't own data
4. Use for both const and non-const access
5. Leverage for safer array access

## Navigation
- **Previous**: [177 - String View](/home/user/DevOps-prj500/101-200_CPP/177_string_view/README.md)
- **Next**: [179 - Filesystem](/home/user/DevOps-prj500/101-200_CPP/179_filesystem/README.md)
