/*
 * Program 174: std::optional - Optional Values and Monadic Operations
 *
 * This program demonstrates:
 * - std::optional basics (C++17)
 * - Creating, accessing, and checking optional values
 * - Monadic operations: and_then, or_else, transform (C++23)
 * - Error handling patterns
 * - Practical use cases
 */

#include <iostream>
#include <optional>
#include <string>
#include <vector>
#include <map>
#include <cmath>

// ==============================================
// 1. std::optional Basics
// ==============================================

void optionalBasicsDemo() {
    std::cout << "\n=== 1. std::optional Basics ===\n";

    // Create optional with value
    std::optional<int> opt1 = 42;
    std::optional<int> opt2{100};
    std::optional<int> opt3 = std::make_optional(200);

    // Create empty optional
    std::optional<int> opt4; // std::nullopt
    std::optional<int> opt5 = std::nullopt;

    std::cout << "opt1 has value: " << std::boolalpha << opt1.has_value() << "\n";
    std::cout << "opt4 has value: " << opt4.has_value() << "\n";

    // Accessing values
    if (opt1.has_value()) {
        std::cout << "opt1 value: " << opt1.value() << "\n";
        std::cout << "opt1 value (operator*): " << *opt1 << "\n";
    }

    // value_or provides default
    std::cout << "opt4 value_or(999): " << opt4.value_or(999) << "\n";
}

// ==============================================
// 2. Optional as Return Type
// ==============================================

std::optional<int> safeDivide(int a, int b) {
    if (b == 0) {
        return std::nullopt; // Indicate failure
    }
    return a / b;
}

std::optional<std::string> findUser(int id) {
    static std::map<int, std::string> users = {
        {1, "Alice"},
        {2, "Bob"},
        {3, "Charlie"}
    };

    auto it = users.find(id);
    if (it != users.end()) {
        return it->second;
    }
    return std::nullopt;
}

void optionalReturnDemo() {
    std::cout << "\n=== 2. Optional as Return Type ===\n";

    // Safe division
    if (auto result = safeDivide(10, 2)) {
        std::cout << "10 / 2 = " << *result << "\n";
    } else {
        std::cout << "Division failed\n";
    }

    if (auto result = safeDivide(10, 0)) {
        std::cout << "10 / 0 = " << *result << "\n";
    } else {
        std::cout << "Division by zero!\n";
    }

    // Find user
    if (auto user = findUser(2)) {
        std::cout << "Found user: " << *user << "\n";
    } else {
        std::cout << "User not found\n";
    }

    if (auto user = findUser(99)) {
        std::cout << "Found user: " << *user << "\n";
    } else {
        std::cout << "User not found\n";
    }
}

// ==============================================
// 3. Optional with Complex Types
// ==============================================

struct Config {
    std::string host;
    int port;
    std::optional<std::string> username; // Optional field
    std::optional<std::string> password; // Optional field
};

void complexTypesDemo() {
    std::cout << "\n=== 3. Optional with Complex Types ===\n";

    Config cfg1{
        "localhost",
        8080,
        "admin",
        "secret123"
    };

    Config cfg2{
        "example.com",
        443,
        std::nullopt,
        std::nullopt
    };

    auto printConfig = [](const Config& cfg) {
        std::cout << "  Host: " << cfg.host << ":" << cfg.port << "\n";
        std::cout << "  Username: " << cfg.username.value_or("(none)") << "\n";
        std::cout << "  Password: " << (cfg.password.has_value() ? "****" : "(none)") << "\n";
    };

    std::cout << "Config 1:\n";
    printConfig(cfg1);

    std::cout << "\nConfig 2:\n";
    printConfig(cfg2);
}

// ==============================================
// 4. Chaining Optional Operations
// ==============================================

std::optional<std::string> getInput() {
    return "42"; // Simulate user input
}

std::optional<int> parseInt(const std::string& s) {
    try {
        return std::stoi(s);
    } catch (...) {
        return std::nullopt;
    }
}

std::optional<int> doubleValue(int x) {
    return x * 2;
}

void chainingDemo() {
    std::cout << "\n=== 4. Chaining Optional Operations ===\n";

    // Manual chaining
    auto input = getInput();
    if (input) {
        auto number = parseInt(*input);
        if (number) {
            auto doubled = doubleValue(*number);
            if (doubled) {
                std::cout << "Result: " << *doubled << "\n";
            }
        }
    }

    // Better pattern with early returns
    auto processInput = []() -> std::optional<int> {
        auto input = getInput();
        if (!input) return std::nullopt;

        auto number = parseInt(*input);
        if (!number) return std::nullopt;

        return doubleValue(*number);
    };

    if (auto result = processInput()) {
        std::cout << "Processed result: " << *result << "\n";
    }
}

// ==============================================
// 5. std::optional vs Pointers
// ==============================================

// Old style with pointers (error-prone)
int* findValuePtr(std::vector<int>& vec, int target) {
    for (auto& val : vec) {
        if (val == target) {
            return &val;
        }
    }
    return nullptr; // Indicates not found
}

// Modern style with optional
std::optional<int> findValueOpt(const std::vector<int>& vec, int target) {
    for (const auto& val : vec) {
        if (val == target) {
            return val;
        }
    }
    return std::nullopt;
}

void vsPointersDemo() {
    std::cout << "\n=== 5. std::optional vs Pointers ===\n";

    std::vector<int> numbers = {1, 2, 3, 4, 5};

    // Using pointer (old style)
    if (int* ptr = findValuePtr(numbers, 3)) {
        std::cout << "Found (pointer): " << *ptr << "\n";
    } else {
        std::cout << "Not found (pointer)\n";
    }

    // Using optional (modern style)
    if (auto opt = findValueOpt(numbers, 3)) {
        std::cout << "Found (optional): " << *opt << "\n";
    } else {
        std::cout << "Not found (optional)\n";
    }

    std::cout << "\noptional is safer and more expressive than nullable pointers\n";
}

// ==============================================
// 6. Emplace and Reset
// ==============================================

void emplaceResetDemo() {
    std::cout << "\n=== 6. Emplace and Reset ===\n";

    std::optional<std::string> opt;

    std::cout << "Initial: has_value = " << std::boolalpha << opt.has_value() << "\n";

    // Emplace constructs in-place
    opt.emplace("Hello");
    std::cout << "After emplace: " << *opt << "\n";

    // Assignment
    opt = "World";
    std::cout << "After assignment: " << *opt << "\n";

    // Reset clears the value
    opt.reset();
    std::cout << "After reset: has_value = " << opt.has_value() << "\n";

    // Can also assign nullopt
    opt = "Test";
    opt = std::nullopt;
    std::cout << "After nullopt assignment: has_value = " << opt.has_value() << "\n";
}

// ==============================================
// 7. Optional Comparison
// ==============================================

void comparisonDemo() {
    std::cout << "\n=== 7. Optional Comparison ===\n";

    std::optional<int> opt1 = 10;
    std::optional<int> opt2 = 20;
    std::optional<int> opt3 = 10;
    std::optional<int> opt4; // nullopt

    std::cout << std::boolalpha;
    std::cout << "opt1 (10) == opt2 (20): " << (opt1 == opt2) << "\n";
    std::cout << "opt1 (10) == opt3 (10): " << (opt1 == opt3) << "\n";
    std::cout << "opt1 (10) < opt2 (20): " << (opt1 < opt2) << "\n";

    // Compare with value
    std::cout << "opt1 == 10: " << (opt1 == 10) << "\n";
    std::cout << "opt1 > 5: " << (opt1 > 5) << "\n";

    // Compare with nullopt
    std::cout << "opt4 == nullopt: " << (opt4 == std::nullopt) << "\n";
    std::cout << "opt1 == nullopt: " << (opt1 == std::nullopt) << "\n";

    // nullopt is less than any value
    std::cout << "opt4 (nullopt) < opt1 (10): " << (opt4 < opt1) << "\n";
}

// ==============================================
// 8. Optional with Move Semantics
// ==============================================

void moveSemanticsDemo() {
    std::cout << "\n=== 8. Optional with Move Semantics ===\n";

    std::optional<std::vector<int>> opt1 = std::vector<int>{1, 2, 3, 4, 5};

    std::cout << "opt1 size: " << opt1->size() << "\n";

    // Move from optional
    std::vector<int> vec = std::move(*opt1);
    std::cout << "After move, vec size: " << vec.size() << "\n";
    std::cout << "After move, opt1 size: " << opt1->size() << " (moved-from state)\n";

    // Move entire optional
    std::optional<std::vector<int>> opt2 = std::vector<int>{10, 20, 30};
    std::optional<std::vector<int>> opt3 = std::move(opt2);

    std::cout << "opt3 size: " << opt3->size() << "\n";
}

// ==============================================
// 9. Error Handling Patterns
// ==============================================

enum class ErrorCode {
    Success,
    NotFound,
    InvalidInput,
    PermissionDenied
};

struct Result {
    std::optional<std::string> data;
    ErrorCode error;
};

Result readFile(const std::string& filename) {
    if (filename.empty()) {
        return {std::nullopt, ErrorCode::InvalidInput};
    }
    if (filename == "private.txt") {
        return {std::nullopt, ErrorCode::PermissionDenied};
    }
    if (filename == "nonexistent.txt") {
        return {std::nullopt, ErrorCode::NotFound};
    }
    return {"File contents...", ErrorCode::Success};
}

void errorHandlingDemo() {
    std::cout << "\n=== 9. Error Handling Patterns ===\n";

    auto processFile = [](const std::string& filename) {
        auto [data, error] = readFile(filename);

        if (data) {
            std::cout << "Success: " << *data << "\n";
        } else {
            std::cout << "Error reading '" << filename << "': ";
            switch (error) {
                case ErrorCode::NotFound:
                    std::cout << "File not found\n";
                    break;
                case ErrorCode::InvalidInput:
                    std::cout << "Invalid filename\n";
                    break;
                case ErrorCode::PermissionDenied:
                    std::cout << "Permission denied\n";
                    break;
                default:
                    break;
            }
        }
    };

    processFile("data.txt");
    processFile("");
    processFile("private.txt");
    processFile("nonexistent.txt");
}

// ==============================================
// 10. Practical Use Cases
// ==============================================

class Cache {
private:
    std::map<std::string, std::string> data;

public:
    void put(const std::string& key, const std::string& value) {
        data[key] = value;
    }

    std::optional<std::string> get(const std::string& key) const {
        auto it = data.find(key);
        if (it != data.end()) {
            return it->second;
        }
        return std::nullopt;
    }
};

struct UserProfile {
    std::string name;
    std::optional<std::string> email;
    std::optional<int> age;
    std::optional<std::string> phone;
};

void practicalUseCasesDemo() {
    std::cout << "\n=== 10. Practical Use Cases ===\n";

    // 1. Cache lookup
    std::cout << "\n1. Cache lookup:\n";
    Cache cache;
    cache.put("api_key", "abc123");

    if (auto key = cache.get("api_key")) {
        std::cout << "  API Key: " << *key << "\n";
    } else {
        std::cout << "  API Key not found\n";
    }

    // 2. User profile with optional fields
    std::cout << "\n2. User profiles:\n";
    UserProfile user1{
        "Alice",
        "alice@example.com",
        25,
        std::nullopt
    };

    UserProfile user2{
        "Bob",
        std::nullopt,
        std::nullopt,
        "+1234567890"
    };

    auto printProfile = [](const UserProfile& user) {
        std::cout << "  Name: " << user.name << "\n";
        std::cout << "  Email: " << user.email.value_or("(not provided)") << "\n";
        std::cout << "  Age: " << (user.age ? std::to_string(*user.age) : "(not provided)") << "\n";
        std::cout << "  Phone: " << user.phone.value_or("(not provided)") << "\n";
    };

    std::cout << "User 1:\n";
    printProfile(user1);

    std::cout << "\nUser 2:\n";
    printProfile(user2);

    // 3. Configuration with defaults
    std::cout << "\n3. Configuration:\n";
    std::optional<int> timeout_config = std::nullopt;
    std::optional<std::string> host_config = "localhost";

    int timeout = timeout_config.value_or(3000); // Default: 3000ms
    std::string host = host_config.value_or("127.0.0.1");

    std::cout << "  Timeout: " << timeout << "ms\n";
    std::cout << "  Host: " << host << "\n";
}

int main() {
    std::cout << "=== C++17 std::optional ===\n";

    // 1. Basics
    optionalBasicsDemo();

    // 2. Return type
    optionalReturnDemo();

    // 3. Complex types
    complexTypesDemo();

    // 4. Chaining
    chainingDemo();

    // 5. vs Pointers
    vsPointersDemo();

    // 6. Emplace and reset
    emplaceResetDemo();

    // 7. Comparison
    comparisonDemo();

    // 8. Move semantics
    moveSemanticsDemo();

    // 9. Error handling
    errorHandlingDemo();

    // 10. Practical use cases
    practicalUseCasesDemo();

    std::cout << "\n=== Key Takeaways ===\n";
    std::cout << "1. std::optional represents optional values (C++17)\n";
    std::cout << "2. Use instead of pointers or magic values for 'no value'\n";
    std::cout << "3. has_value() checks, value() accesses (throws if empty)\n";
    std::cout << "4. value_or() provides default for empty optional\n";
    std::cout << "5. operator* and operator-> for direct access\n";
    std::cout << "6. Great for function returns and optional struct fields\n";
    std::cout << "7. More type-safe and expressive than nullable pointers\n";

    return 0;
}
