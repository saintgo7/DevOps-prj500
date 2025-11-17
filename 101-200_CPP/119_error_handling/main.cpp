/*
 * Program 119: Error Handling with Exceptions
 *
 * Topics Covered:
 * - try-catch blocks
 * - throw statement
 * - Exception types (std::exception hierarchy)
 * - Custom exceptions
 * - Exception specifications (noexcept)
 * - RAII and exception safety
 * - Stack unwinding
 * - catch(...) for all exceptions
 * - Re-throwing exceptions
 * - std::exception_ptr
 *
 * Compilation:
 * g++ -std=c++20 -Wall -Wextra -o error_handling main.cpp
 */

#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
#include <memory>

void demonstrateBasicExceptions();
void demonstrateStandardExceptions();
void demonstrateCustomExceptions();
void demonstrateNoexcept();
void demonstrateExceptionSafety();
void demonstrateAdvancedFeatures();

int main() {
    std::cout << "=== C++ Error Handling with Exceptions ===" << std::endl << std::endl;

    demonstrateBasicExceptions();
    demonstrateStandardExceptions();
    demonstrateCustomExceptions();
    demonstrateNoexcept();
    demonstrateExceptionSafety();
    demonstrateAdvancedFeatures();

    return 0;
}

void demonstrateBasicExceptions() {
    std::cout << "--- Basic Exception Handling ---" << std::endl;

    // Simple try-catch
    try {
        std::cout << "Before throw" << std::endl;
        throw 42;  // Throwing an int
        std::cout << "This won't execute" << std::endl;
    } catch (int e) {
        std::cout << "Caught exception: " << e << std::endl;
    }

    // Catching different types
    try {
        // throw 3.14;  // Uncomment to test
        throw "Error message";
    } catch (int e) {
        std::cout << "Caught int: " << e << std::endl;
    } catch (const char* e) {
        std::cout << "Caught string: " << e << std::endl;
    } catch (...) {
        std::cout << "Caught unknown exception" << std::endl;
    }

    // Function that throws
    auto divide = [](int a, int b) -> double {
        if (b == 0) {
            throw std::runtime_error("Division by zero");
        }
        return static_cast<double>(a) / b;
    };

    try {
        std::cout << "\n10 / 2 = " << divide(10, 2) << std::endl;
        std::cout << "10 / 0 = " << divide(10, 0) << std::endl;
    } catch (const std::runtime_error& e) {
        std::cout << "Error: " << e.what() << std::endl;
    }

    std::cout << std::endl;
}

void demonstrateStandardExceptions() {
    std::cout << "--- Standard Exception Classes ---" << std::endl;

    // std::exception hierarchy:
    // std::exception
    //   ├── std::logic_error
    //   │   ├── std::invalid_argument
    //   │   ├── std::domain_error
    //   │   ├── std::length_error
    //   │   ├── std::out_of_range
    //   │   └── std::future_error
    //   └── std::runtime_error
    //       ├── std::range_error
    //       ├── std::overflow_error
    //       ├── std::underflow_error
    //       └── std::system_error

    // std::invalid_argument
    try {
        auto validateAge = [](int age) {
            if (age < 0 || age > 150) {
                throw std::invalid_argument("Invalid age");
            }
        };
        validateAge(200);
    } catch (const std::invalid_argument& e) {
        std::cout << "std::invalid_argument: " << e.what() << std::endl;
    }

    // std::out_of_range
    try {
        std::vector<int> vec = {1, 2, 3};
        int value = vec.at(10);  // Throws out_of_range
    } catch (const std::out_of_range& e) {
        std::cout << "std::out_of_range: " << e.what() << std::endl;
    }

    // std::runtime_error
    try {
        throw std::runtime_error("Runtime error occurred");
    } catch (const std::runtime_error& e) {
        std::cout << "std::runtime_error: " << e.what() << std::endl;
    }

    // std::logic_error
    try {
        throw std::logic_error("Logic error in program");
    } catch (const std::logic_error& e) {
        std::cout << "std::logic_error: " << e.what() << std::endl;
    }

    // Catching base class
    try {
        throw std::invalid_argument("Some error");
    } catch (const std::exception& e) {
        std::cout << "\nCaught via base class std::exception: " << e.what() << std::endl;
    }

    std::cout << std::endl;
}

// Custom exception class
class CustomException : public std::exception {
public:
    CustomException(const std::string& msg) : message(msg) {}

    const char* what() const noexcept override {
        return message.c_str();
    }

private:
    std::string message;
};

// Another custom exception
class FileException : public std::runtime_error {
public:
    FileException(const std::string& filename)
        : std::runtime_error("File error"), filename_(filename) {}

    const std::string& getFilename() const {
        return filename_;
    }

private:
    std::string filename_;
};

void demonstrateCustomExceptions() {
    std::cout << "--- Custom Exceptions ---" << std::endl;

    // Using custom exception
    try {
        throw CustomException("This is a custom exception");
    } catch (const CustomException& e) {
        std::cout << "CustomException: " << e.what() << std::endl;
    }

    // Custom exception with additional data
    try {
        throw FileException("data.txt");
    } catch (const FileException& e) {
        std::cout << "FileException: " << e.what()
                  << " (file: " << e.getFilename() << ")" << std::endl;
    }

    // Catching custom via base class
    try {
        throw FileException("config.ini");
    } catch (const std::exception& e) {
        std::cout << "Caught custom via std::exception: " << e.what() << std::endl;
    }

    std::cout << std::endl;
}

// noexcept function (guaranteed not to throw)
int safeAdd(int a, int b) noexcept {
    return a + b;
}

// Conditionally noexcept
template<typename T>
void swap(T& a, T& b) noexcept(std::is_nothrow_move_constructible_v<T>) {
    T temp = std::move(a);
    a = std::move(b);
    b = std::move(temp);
}

void demonstrateNoexcept() {
    std::cout << "--- noexcept Specification ---" << std::endl;

    // noexcept function
    int result = safeAdd(5, 3);
    std::cout << "Result from noexcept function: " << result << std::endl;

    // Checking if function is noexcept
    std::cout << "safeAdd is noexcept: " << std::boolalpha
              << noexcept(safeAdd(1, 2)) << std::endl;

    // Breaking noexcept (calls std::terminate)
    auto badNoexcept = []() noexcept {
        // throw std::runtime_error("Oops!");  // Calls std::terminate!
    };

    std::cout << "\nnoexcept functions should never throw" << std::endl;
    std::cout << "If they do, std::terminate is called" << std::endl;

    // Move constructors should be noexcept
    class Resource {
    public:
        Resource() = default;
        Resource(Resource&& other) noexcept {
            // Move implementation
        }
        Resource& operator=(Resource&& other) noexcept {
            // Move assignment
            return *this;
        }
    };

    std::cout << "Move constructors should be marked noexcept" << std::endl;

    std::cout << std::endl;
}

class SmartResource {
public:
    SmartResource(const std::string& name) : name_(name) {
        std::cout << "Acquiring resource: " << name_ << std::endl;
    }

    ~SmartResource() {
        std::cout << "Releasing resource: " << name_ << std::endl;
    }

private:
    std::string name_;
};

void demonstrateExceptionSafety() {
    std::cout << "--- Exception Safety and RAII ---" << std::endl;

    // RAII ensures cleanup even with exceptions
    try {
        SmartResource res1("Database");
        SmartResource res2("Network");

        std::cout << "Working with resources..." << std::endl;
        throw std::runtime_error("Something went wrong");

        std::cout << "This won't execute" << std::endl;
    } catch (const std::exception& e) {
        std::cout << "Exception: " << e.what() << std::endl;
    }
    std::cout << "Resources automatically cleaned up\n" << std::endl;

    // Smart pointers and exception safety
    try {
        auto ptr1 = std::make_unique<int>(42);
        auto ptr2 = std::make_unique<int>(100);

        // If exception here, smart pointers still cleaned up
        throw std::runtime_error("Error");
    } catch (const std::exception& e) {
        std::cout << "Smart pointers cleaned up automatically" << std::endl;
    }

    // Exception safety levels:
    // 1. Basic guarantee: No leaks, valid state
    // 2. Strong guarantee: Commit or rollback (no change if exception)
    // 3. Nothrow guarantee: Never throws

    std::cout << std::endl;
}

void demonstrateAdvancedFeatures() {
    std::cout << "--- Advanced Exception Features ---" << std::endl;

    // Re-throwing exceptions
    try {
        try {
            throw std::runtime_error("Original error");
        } catch (const std::exception& e) {
            std::cout << "Caught: " << e.what() << std::endl;
            std::cout << "Re-throwing..." << std::endl;
            throw;  // Re-throw same exception
        }
    } catch (const std::exception& e) {
        std::cout << "Caught re-thrown: " << e.what() << std::endl;
    }

    // Stack unwinding
    std::cout << "\n--- Stack Unwinding ---" << std::endl;
    auto func3 = []() {
        SmartResource res("func3");
        throw std::runtime_error("Error in func3");
    };

    auto func2 = [&]() {
        SmartResource res("func2");
        func3();
    };

    auto func1 = [&]() {
        SmartResource res("func1");
        func2();
    };

    try {
        func1();
    } catch (const std::exception& e) {
        std::cout << "Stack unwound: " << e.what() << std::endl;
    }

    // Nested try-catch
    std::cout << "\n--- Nested try-catch ---" << std::endl;
    try {
        try {
            throw std::runtime_error("Inner exception");
        } catch (const std::invalid_argument& e) {
            // Won't catch runtime_error
            std::cout << "Inner catch" << std::endl;
        }
    } catch (const std::exception& e) {
        std::cout << "Outer catch: " << e.what() << std::endl;
    }

    std::cout << std::endl;
}

/*
 * Exception Handling Best Practices:
 *
 * 1. Use exceptions for exceptional situations, not control flow
 * 2. Throw by value, catch by const reference
 * 3. Derive custom exceptions from std::exception
 * 4. Use RAII to ensure cleanup
 * 5. Make destructors noexcept
 * 6. Make move operations noexcept when possible
 * 7. Catch specific exceptions before general ones
 * 8. Document which exceptions functions can throw
 * 9. Don't throw in destructors
 * 10. Use smart pointers for exception safety
 *
 * When to Use Exceptions:
 * ✓ Resource acquisition failures
 * ✓ Unexpected runtime conditions
 * ✓ Violations of preconditions
 * ✓ Errors that cross abstraction boundaries
 *
 * When NOT to Use Exceptions:
 * ✗ Normal control flow
 * ✗ Performance-critical code paths
 * ✗ In real-time systems
 * ✗ Simple validation (use return codes)
 *
 * Exception Safety Guarantees:
 * 1. Basic: No leaks, object in valid state
 * 2. Strong: Commit or rollback semantics
 * 3. Nothrow: Operation never fails
 */
