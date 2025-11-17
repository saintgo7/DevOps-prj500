/*
 * Program 112: Enumerations in C++
 *
 * Topics Covered:
 * - Classic enums (unscoped)
 * - Enum class (scoped enums, C++11)
 * - Underlying types
 * - Enum forward declarations
 * - Enum conversions
 * - Enum as flags (bit flags)
 * - Enum best practices
 *
 * Compilation:
 * g++ -std=c++20 -Wall -Wextra -o enums main.cpp
 */

#include <iostream>
#include <string>

// Classic enum (unscoped)
enum Color {
    RED,      // 0
    GREEN,    // 1
    BLUE      // 2
};

// Enum with explicit values
enum Status {
    OK = 0,
    WARNING = 1,
    ERROR = 2,
    CRITICAL = 10
};

// Enum class (scoped, C++11)
enum class Direction {
    North,
    South,
    East,
    West
};

// Enum class with underlying type
enum class Priority : unsigned char {
    Low = 1,
    Medium = 5,
    High = 10
};

// Enum as flags
enum FilePermissions {
    Read = 1 << 0,    // 0001 = 1
    Write = 1 << 1,   // 0010 = 2
    Execute = 1 << 2  // 0100 = 4
};

// Scoped enum for flags
enum class FileMode : unsigned int {
    None = 0,
    Read = 1 << 0,
    Write = 1 << 1,
    Execute = 1 << 2,
    ReadWrite = Read | Write,
    All = Read | Write | Execute
};

void demonstrateClassicEnums();
void demonstrateEnumClass();
void demonstrateEnumConversions();
void demonstrateEnumFlags();

int main() {
    std::cout << "=== C++ Enumerations ===" << std::endl << std::endl;

    demonstrateClassicEnums();
    demonstrateEnumClass();
    demonstrateEnumConversions();
    demonstrateEnumFlags();

    return 0;
}

void demonstrateClassicEnums() {
    std::cout << "--- Classic Enums (Unscoped) ---" << std::endl;

    // Using enum values
    Color favoriteColor = RED;
    std::cout << "Favorite color (numeric): " << favoriteColor << std::endl;

    // Enums can be used in switch
    switch (favoriteColor) {
        case RED:
            std::cout << "Color is RED" << std::endl;
            break;
        case GREEN:
            std::cout << "Color is GREEN" << std::endl;
            break;
        case BLUE:
            std::cout << "Color is BLUE" << std::endl;
            break;
    }

    // Implicit conversion to int
    int colorValue = GREEN;
    std::cout << "GREEN as int: " << colorValue << std::endl;

    // Enums with explicit values
    Status status = OK;
    std::cout << "\nStatus values:" << std::endl;
    std::cout << "OK: " << OK << std::endl;
    std::cout << "WARNING: " << WARNING << std::endl;
    std::cout << "ERROR: " << ERROR << std::endl;
    std::cout << "CRITICAL: " << CRITICAL << std::endl;

    // Problem with classic enums: name pollution
    // Color and Status share the global namespace
    // Can't have another enum with RED, GREEN, etc.

    std::cout << std::endl;
}

void demonstrateEnumClass() {
    std::cout << "--- Enum Class (Scoped Enums, C++11) ---" << std::endl;

    // Scoped enums require scope resolution
    Direction dir = Direction::North;

    // Cannot implicitly convert to int
    // int dirValue = dir;  // Error!

    // Must use switch or comparison
    if (dir == Direction::North) {
        std::cout << "Going North" << std::endl;
    }

    // Switch with enum class
    switch (dir) {
        case Direction::North:
            std::cout << "Direction: North" << std::endl;
            break;
        case Direction::South:
            std::cout << "Direction: South" << std::endl;
            break;
        case Direction::East:
            std::cout << "Direction: East" << std::endl;
            break;
        case Direction::West:
            std::cout << "Direction: West" << std::endl;
            break;
    }

    // Different enum classes can have same names
    enum class TrafficLight {
        Red,
        Yellow,
        Green
    };

    TrafficLight light = TrafficLight::Red;
    Color color = RED;
    // No conflict!

    std::cout << "\nTrafficLight and Color can both have Red/RED" << std::endl;

    // Explicit underlying type
    Priority p = Priority::High;
    std::cout << "Priority::High = " << static_cast<int>(p) << std::endl;

    std::cout << std::endl;
}

void demonstrateEnumConversions() {
    std::cout << "--- Enum Conversions ---" << std::endl;

    // Classic enum: implicit conversion to int
    Color color = GREEN;
    int value = color;  // OK
    std::cout << "Classic enum to int: " << value << std::endl;

    // int to classic enum requires cast
    Color color2 = static_cast<Color>(1);
    std::cout << "int to classic enum: " << color2 << std::endl;

    // Enum class: requires explicit cast
    Direction dir = Direction::East;
    int dirValue = static_cast<int>(dir);
    std::cout << "\nEnum class to int (explicit): " << dirValue << std::endl;

    // int to enum class
    Direction dir2 = static_cast<Direction>(0);
    if (dir2 == Direction::North) {
        std::cout << "Converted 0 to Direction::North" << std::endl;
    }

    // Underlying type cast
    Priority priority = Priority::Medium;
    unsigned char byteValue = static_cast<unsigned char>(priority);
    std::cout << "\nPriority::Medium as byte: " << static_cast<int>(byteValue) << std::endl;

    std::cout << std::endl;
}

// Helper function to check flags
bool hasPermission(int permissions, FilePermissions permission) {
    return (permissions & permission) != 0;
}

// Helper for scoped enum flags
bool hasModeFlag(FileMode mode, FileMode flag) {
    return (static_cast<int>(mode) & static_cast<int>(flag)) != 0;
}

void demonstrateEnumFlags() {
    std::cout << "--- Enum as Bit Flags ---" << std::endl;

    // Using classic enum for flags
    int permissions = Read | Write;
    std::cout << "Permissions value: " << permissions << std::endl;

    std::cout << "Has Read: " << std::boolalpha << hasPermission(permissions, Read) << std::endl;
    std::cout << "Has Write: " << hasPermission(permissions, Write) << std::endl;
    std::cout << "Has Execute: " << hasPermission(permissions, Execute) << std::endl;

    // Add Execute permission
    permissions |= Execute;
    std::cout << "\nAfter adding Execute:" << std::endl;
    std::cout << "Has Execute: " << hasPermission(permissions, Execute) << std::endl;
    std::cout << "Permissions value: " << permissions << std::endl;

    // Remove Write permission
    permissions &= ~Write;
    std::cout << "\nAfter removing Write:" << std::endl;
    std::cout << "Has Write: " << hasPermission(permissions, Write) << std::endl;
    std::cout << "Permissions value: " << permissions << std::endl;

    // Using enum class for flags
    std::cout << "\n--- Scoped Enum Flags ---" << std::endl;
    FileMode mode = FileMode::ReadWrite;
    std::cout << "Mode value: " << static_cast<int>(mode) << std::endl;

    // Printing individual flags
    std::cout << "Read flag: " << static_cast<int>(FileMode::Read) << std::endl;
    std::cout << "Write flag: " << static_cast<int>(FileMode::Write) << std::endl;
    std::cout << "Execute flag: " << static_cast<int>(FileMode::Execute) << std::endl;
    std::cout << "All flags: " << static_cast<int>(FileMode::All) << std::endl;

    std::cout << std::endl;
}

/*
 * Classic Enum vs Enum Class Comparison:
 *
 * Classic Enum:
 * - Enumerators in enclosing scope
 * - Implicit conversion to int
 * - Can cause name collisions
 * - Backward compatible with C
 *
 * Enum Class:
 * - Enumerators scoped to enum
 * - No implicit conversion
 * - Type-safe
 * - Can specify underlying type
 * - Preferred in modern C++
 *
 * Best Practices:
 * 1. Prefer enum class over classic enums
 * 2. Use meaningful names for enumerators
 * 3. Specify underlying type when needed
 * 4. Use enums for flags with bit operations
 * 5. Don't mix enum classes with operators without defining them
 * 6. Use switch statements exhaustively (cover all cases)
 * 7. Consider using constexpr variables instead of enums for constants
 * 8. Forward declare enum classes when possible
 * 9. Use static_cast for conversions
 * 10. Document the meaning of enum values
 */
