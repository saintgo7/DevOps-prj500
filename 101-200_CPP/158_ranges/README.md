# Program 158: C++20 Ranges

## Description
This program explores the C++20 Ranges library, which provides a modern, composable approach to working with sequences through views, lazy evaluation, range algorithms, and functional-style transformations.

## Learning Objectives
- Understand the ranges library architecture
- Master range views (filter, transform, take, drop)
- Use lazy evaluation for efficiency
- Compose range operations with pipe operator
- Apply range algorithms with projections
- Utilize range factories (iota, empty, single)

## Features
- Basic ranges concepts
- Range views (filter, transform, take, drop, reverse)
- Range composition with pipe operator
- Lazy evaluation demonstration
- Range algorithms (sort, reverse, find, count)
- Projection support in algorithms
- Range factories (iota, views)
- Practical data processing pipeline

## Compilation and Usage

```bash
# Requires C++20
g++ -std=c++20 main.cpp -o ranges
cd /home/user/DevOps-prj500/101-200_CPP/158_ranges
mkdir -p build && cd build && cmake .. && make
./ranges
```

## Key Concepts

### Basic Range Views
```cpp
vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

// Filter evens
auto evens = v | views::filter([](int x) { return x % 2 == 0; });

// Transform (square)
auto squared = v | views::transform([](int x) { return x * x; });

// Take first 5
auto first_5 = v | views::take(5);
```

### Range Composition
```cpp
auto result = v
    | views::filter([](int x) { return x % 2 == 0; })
    | views::transform([](int x) { return x * x; })
    | views::take(3);
```

### Lazy Evaluation
```cpp
// Pipeline defined but not executed
auto pipeline = v | views::filter(...) | views::transform(...);

// Execution happens when iterated
for (auto elem : pipeline) {
    // Processing occurs here
}
```

### Range Algorithms with Projection
```cpp
struct Person { string name; int age; };
vector<Person> people = {...};

// Sort by age using projection
ranges::sort(people, {}, &Person::age);
```

## Best Practices
1. **Use views for non-owning transformations**: No data copying
2. **Leverage lazy evaluation**: Process only what's needed
3. **Compose operations**: Chain multiple views with |
4. **Use projections**: Avoid writing custom comparators
5. **Prefer ranges algorithms**: More expressive than iterator-based algorithms

## Resources/References
- [cppreference: Ranges](https://en.cppreference.com/w/cpp/ranges)
- [C++20 Ranges Tutorial](https://www.modernescpp.com/index.php/c-20-the-ranges-library)
- [Range-v3 Library](https://github.com/ericniebler/range-v3)

## Navigation
- **Previous**: [157 - Concepts](/home/user/DevOps-prj500/101-200_CPP/157_concepts/README.md)
- **Next**: [159 - Type Traits](/home/user/DevOps-prj500/101-200_CPP/159_type_traits/README.md)
