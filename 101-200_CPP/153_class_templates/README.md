# Program 153: Class Templates

## Description
This program explores class templates in depth, demonstrating how to create generic, reusable classes that work with any type. It covers template member functions, static members, nested classes, friend functions, inheritance, and practical template class patterns.

## Learning Objectives
- Master class template syntax and instantiation
- Work with multiple template parameters (type and non-type)
- Implement template member functions
- Understand static members in template classes
- Use nested classes within templates
- Apply friend functions with templates
- Implement template class inheritance
- Utilize template aliases for cleaner code

## Features
- Basic class template syntax
- Multiple template parameters
- Non-type template parameters
- Template member functions (including template members)
- Static members in template classes
- Nested classes demonstration
- Friend function declarations in templates
- Template inheritance patterns
- Template aliases (C++11)
- Smart vector implementation example

## Compilation and Usage

### Compilation
```bash
# Using g++
g++ -std=c++17 main.cpp -o class_templates

# Using CMake
cd /home/user/DevOps-prj500/101-200_CPP/153_class_templates
mkdir -p build && cd build
cmake ..
make
```

### Execution
```bash
./class_templates
```

## Key Concepts

### 1. Basic Class Template
```cpp
template<typename T>
class Box {
private:
    T value;
public:
    Box(T v) : value(v) {}
    T getValue() const { return value; }
    void setValue(T v) { value = v; }
};

// Usage
Box<int> intBox(42);
Box<string> stringBox("Hello");
```

### 2. Multiple Template Parameters
```cpp
template<typename T, typename U>
class Pair {
private:
    T first;
    U second;
public:
    Pair(T f, U s) : first(f), second(s) {}
    T getFirst() const { return first; }
    U getSecond() const { return second; }
};

Pair<int, string> p(1, "one");
```

### 3. Non-Type Template Parameters
```cpp
template<typename T, int Size>
class StaticArray {
private:
    T data[Size];
public:
    int size() const { return Size; }
    T& operator[](int index) { return data[index]; }
};

StaticArray<int, 10> arr;  // Fixed-size array
```

### 4. Template Member Functions
```cpp
template<typename T>
class Container {
public:
    void add(const T& item);

    // Template member function
    template<typename U>
    void addConverted(const U& item) {
        add(static_cast<T>(item));
    }
};
```

### 5. Static Members in Templates
```cpp
template<typename T>
class Counter {
private:
    static int count;  // Separate for each T
public:
    Counter() { count++; }
    static int getCount() { return count; }
};

// Definition required
template<typename T>
int Counter<T>::count = 0;

// Each type has its own counter
Counter<int>::getCount();    // Separate from
Counter<double>::getCount(); // this count
```

### 6. Template Inheritance
```cpp
template<typename T>
class Base {
protected:
    T value;
public:
    Base(T v) : value(v) {}
};

template<typename T>
class Derived : public Base<T> {
public:
    Derived(T v) : Base<T>(v) {}
    void print() {
        cout << this->value;  // Need 'this->' for dependent names
    }
};
```

### 7. Template Aliases (C++11)
```cpp
template<typename T>
using Vec = vector<T>;

template<typename T>
using Ptr = shared_ptr<T>;

Vec<int> numbers;     // Clearer than vector<int>
Ptr<Data> dataPtr;    // Clearer than shared_ptr<Data>
```

## Best Practices
1. **Use initialization lists**: Especially important for template classes
   ```cpp
   template<typename T>
   Box(T v) : value(v) {}  // Good
   ```

2. **Define static members outside class**:
   ```cpp
   template<typename T>
   int Counter<T>::count = 0;
   ```

3. **Use `this->` for dependent names in derived templates**:
   ```cpp
   template<typename T>
   class Derived : public Base<T> {
       void func() { this->base_member; }
   };
   ```

4. **Prefer template aliases over typedef**:
   ```cpp
   template<typename T>
   using Vec = vector<T>;  // Better than typedef
   ```

5. **Consider copy and move semantics**: Implement Rule of Five when managing resources

6. **Use const correctness**: Provide const and non-const overloads

7. **Document template constraints**: Use static_assert or concepts

8. **Keep templates in headers**: Full definition needed at instantiation point

## Resources/References
- [cppreference: Class Templates](https://en.cppreference.com/w/cpp/language/class_template)
- [Template Aliases](https://en.cppreference.com/w/cpp/language/type_alias)
- [Static Members in Templates](https://en.cppreference.com/w/cpp/language/static)
- [C++ Templates Book](http://www.tmplbook.com/)

## Navigation
- **Previous Program**: [152 - Function Templates](/home/user/DevOps-prj500/101-200_CPP/152_function_templates/README.md)
- **Next Program**: [154 - Template Specialization](/home/user/DevOps-prj500/101-200_CPP/154_template_specialization/README.md)
- **Back to Main Index**: [README](/home/user/DevOps-prj500/README.md)
