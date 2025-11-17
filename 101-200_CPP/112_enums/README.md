# Program 112: Enumerations in C++

## Description
Comprehensive exploration of enumerations in C++ covering traditional enums, scoped enums (enum class), enum underlying types, enum operations, and best practices. This program demonstrates how enumerations provide type-safe named constants and improve code readability.

## Learning Objectives
- Understand enumeration basics and syntax
- Master scoped enumerations (enum class) - C++11
- Work with enum underlying types
- Use enums in switch statements
- Convert between enums and integers
- Apply enum best practices
- Understand enum vs enum class differences

## Features
- Traditional unscoped enumerations
- Scoped enumerations (enum class) - C++11
- Custom underlying types for enums
- Enum forward declarations
- Enum arithmetic and comparison
- Enum to string conversions
- Switch statements with enums
- Bitwise flags with enums

## Compilation and Usage

### Compilation
```bash
cd /home/user/DevOps-prj500/101-200_CPP/112_enums
g++ -std=c++20 -Wall -Wextra -o enums main.cpp
```

### Execution
```bash
./enums
```

## Key Concepts

### 1. Traditional Unscoped Enums
```cpp
// Basic enum declaration
enum Color {
    RED,      // 0
    GREEN,    // 1
    BLUE      // 2
};

// With explicit values
enum Status {
    INACTIVE = 0,
    ACTIVE = 1,
    PENDING = 2,
    ERROR = -1
};

// Usage
Color myColor = RED;
Status status = ACTIVE;

// Implicit conversion to int
int colorValue = GREEN;  // 1

// Cannot implicit convert from int (requires cast)
// Color c = 1;  // Error!
Color c = static_cast<Color>(1);  // OK

// Switch statement
switch (myColor) {
    case RED:
        std::cout << "Red\n";
        break;
    case GREEN:
        std::cout << "Green\n";
        break;
    case BLUE:
        std::cout << "Blue\n";
        break;
}
```

### 2. Scoped Enumerations (enum class) - C++11
```cpp
// Scoped enum (strongly typed)
enum class TrafficLight {
    Red,
    Yellow,
    Green
};

// Must use scope
TrafficLight light = TrafficLight::Red;
// TrafficLight light = Red;  // Error!

// No implicit conversion to int
// int value = TrafficLight::Red;  // Error!
int value = static_cast<int>(TrafficLight::Red);  // OK

// No name pollution
enum class Signal { Red, Yellow, Green };  // OK, no conflict with TrafficLight

// Can't compare different enum types
TrafficLight t = TrafficLight::Red;
Signal s = Signal::Red;
// if (t == s) {}  // Error!

// Switch statement (requires full qualification)
switch (light) {
    case TrafficLight::Red:
        std::cout << "Stop\n";
        break;
    case TrafficLight::Yellow:
        std::cout << "Caution\n";
        break;
    case TrafficLight::Green:
        std::cout << "Go\n";
        break;
}
```

### 3. Custom Underlying Types
```cpp
// Specify underlying type
enum class SmallEnum : uint8_t {
    First,
    Second,
    Third
};  // Size = 1 byte

enum class LargeEnum : uint64_t {
    BigValue = 1000000000000
};  // Size = 8 bytes

// Check size
std::cout << sizeof(SmallEnum) << '\n';  // 1
std::cout << sizeof(LargeEnum) << '\n';  // 8

// Traditional enum with underlying type (C++11)
enum ByteEnum : unsigned char {
    A, B, C
};
```

### 4. Forward Declarations
```cpp
// Forward declaration (requires underlying type for unscoped)
enum ByteFlags : unsigned char;

// Forward declaration (enum class doesn't require type)
enum class ErrorCode;
enum class ErrorCode : int;  // Can specify optionally

// Later definition
enum class ErrorCode {
    Success = 0,
    FileNotFound = 1,
    PermissionDenied = 2,
    InvalidInput = 3
};
```

### 5. Enum Operations
```cpp
enum class Priority {
    Low = 1,
    Medium = 2,
    High = 3,
    Critical = 4
};

// Comparison
Priority p1 = Priority::Low;
Priority p2 = Priority::High;
bool lessThan = (p1 < p2);  // true

// Increment (requires explicit cast)
p1 = static_cast<Priority>(static_cast<int>(p1) + 1);

// Helper function for increment
Priority operator++(Priority& p) {
    p = static_cast<Priority>(static_cast<int>(p) + 1);
    return p;
}

// Helper function to get underlying value
template<typename E>
constexpr auto toUnderlying(E e) noexcept {
    return static_cast<std::underlying_type_t<E>>(e);
}

int value = toUnderlying(Priority::High);  // 3
```

### 6. Bitwise Flags with Enums
```cpp
// Unscoped enum for flags
enum FilePermissions {
    READ    = 1 << 0,  // 0001 = 1
    WRITE   = 1 << 1,  // 0010 = 2
    EXECUTE = 1 << 2,  // 0100 = 4
    DELETE  = 1 << 3   // 1000 = 8
};

// Combine flags
int permissions = READ | WRITE | EXECUTE;

// Check flag
if (permissions & READ) {
    std::cout << "Can read\n";
}

// Add flag
permissions |= DELETE;

// Remove flag
permissions &= ~WRITE;

// Scoped enum for flags (requires operator overloading)
enum class Flags : unsigned int {
    None   = 0,
    Flag1  = 1 << 0,
    Flag2  = 1 << 1,
    Flag3  = 1 << 2,
    Flag4  = 1 << 3
};

// Operator overloading for bitwise operations
Flags operator|(Flags a, Flags b) {
    return static_cast<Flags>(
        static_cast<unsigned int>(a) | static_cast<unsigned int>(b)
    );
}

Flags operator&(Flags a, Flags b) {
    return static_cast<Flags>(
        static_cast<unsigned int>(a) & static_cast<unsigned int>(b)
    );
}

// Usage
Flags f = Flags::Flag1 | Flags::Flag2;
if ((f & Flags::Flag1) != Flags::None) {
    std::cout << "Flag1 is set\n";
}
```

### 7. Enum to String Conversions
```cpp
// Manual conversion
std::string colorToString(Color c) {
    switch (c) {
        case RED:   return "Red";
        case GREEN: return "Green";
        case BLUE:  return "Blue";
        default:    return "Unknown";
    }
}

// Using array (only for sequential enums starting at 0)
const char* colorNames[] = {"Red", "Green", "Blue"};
std::string toString(Color c) {
    return colorNames[c];
}

// Scoped enum to string
std::string toString(TrafficLight t) {
    switch (t) {
        case TrafficLight::Red:    return "Red";
        case TrafficLight::Yellow: return "Yellow";
        case TrafficLight::Green:  return "Green";
        default:                   return "Unknown";
    }
}

// String to enum
std::optional<Color> stringToColor(const std::string& str) {
    if (str == "Red")   return RED;
    if (str == "Green") return GREEN;
    if (str == "Blue")  return BLUE;
    return std::nullopt;
}
```

### 8. Enum Ranges and Iteration
```cpp
// Enum with known range
enum class Day {
    Monday,
    Tuesday,
    Wednesday,
    Thursday,
    Friday,
    Saturday,
    Sunday,
    Count  // Sentinel value
};

// Iterate through enum
for (int i = 0; i < static_cast<int>(Day::Count); ++i) {
    Day day = static_cast<Day>(i);
    std::cout << "Day " << i << '\n';
}

// Using traits
template<typename E>
struct EnumTraits;

template<>
struct EnumTraits<Day> {
    static constexpr Day first = Day::Monday;
    static constexpr Day last = Day::Sunday;
};

// Range-based helper
template<typename E>
class EnumRange {
    int current;
public:
    EnumRange(E start) : current(static_cast<int>(start)) {}

    bool operator!=(EnumRange other) const {
        return current != other.current;
    }

    E operator*() const {
        return static_cast<E>(current);
    }

    EnumRange& operator++() {
        ++current;
        return *this;
    }
};

template<typename E>
EnumRange<E> begin(EnumTraits<E>) {
    return EnumRange<E>(EnumTraits<E>::first);
}

template<typename E>
EnumRange<E> end(EnumTraits<E>) {
    return EnumRange<E>(static_cast<E>(
        static_cast<int>(EnumTraits<E>::last) + 1
    ));
}
```

## Best Practices
1. **Prefer enum class** over traditional enums for type safety
2. **Use explicit underlying types** for specific size requirements
3. **Provide to-string conversion** functions for debugging
4. **Use enums in switch statements** without default (for exhaustiveness checking)
5. **Name enum values clearly** (PascalCase or UPPER_CASE)
6. **Group related constants** using enums
7. **Use bitwise flags** for combinations of options
8. **Forward declare enums** to reduce compilation dependencies
9. **Document enum value meanings** especially for non-obvious values
10. **Use constexpr** for enum-to-string conversions when possible

## Common Patterns
```cpp
// 1. State machine
enum class State {
    Idle,
    Running,
    Paused,
    Stopped
};

class StateMachine {
    State currentState = State::Idle;
public:
    void transition(State newState) {
        currentState = newState;
    }
};

// 2. Error codes
enum class ErrorCode {
    Success = 0,
    InvalidArgument = 1,
    OutOfMemory = 2,
    IOError = 3
};

// 3. Configuration options
enum class LogLevel {
    Debug,
    Info,
    Warning,
    Error,
    Critical
};

// 4. Type tags
enum class ShapeType {
    Circle,
    Rectangle,
    Triangle
};
```

## Resources and References
- [cppreference.com - Enumeration](https://en.cppreference.com/w/cpp/language/enum)
- [cppreference.com - Scoped enums](https://en.cppreference.com/w/cpp/language/enum#Scoped_enumerations)
- [C++ Core Guidelines - Enums](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Renum-class)

## Navigation
- **Previous Program**: [111 - Structures](../111_structures/README.md)
- **Next Program**: [113 - File I/O](../113_file_io/README.md)
- **Back to Main**: [C++ Programs 101-200](../README.md)
