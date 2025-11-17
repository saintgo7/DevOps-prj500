/*
 * Program 110: Strings in C++
 *
 * Topics Covered:
 * - C-strings (char arrays)
 * - std::string (C++ string class)
 * - String initialization and assignment
 * - String operations (concatenation, comparison, etc.)
 * - String access and modification
 * - String searching and manipulation
 * - String conversions
 * - std::string_view (C++17)
 * - Raw string literals (C++11)
 *
 * Compilation:
 * g++ -std=c++20 -Wall -Wextra -o strings main.cpp
 */

#include <iostream>
#include <string>
#include <string_view>
#include <cstring>  // For C-string functions
#include <sstream>  // String streams
#include <algorithm>

void demonstrateCStrings();
void demonstrateStdString();
void demonstrateStringOperations();
void demonstrateStringManipulation();
void demonstrateStringConversion();
void demonstrateStringView();

int main() {
    std::cout << "=== C++ Strings ===" << std::endl << std::endl;

    demonstrateCStrings();
    demonstrateStdString();
    demonstrateStringOperations();
    demonstrateStringManipulation();
    demonstrateStringConversion();
    demonstrateStringView();

    return 0;
}

void demonstrateCStrings() {
    std::cout << "--- C-Strings (char arrays) ---" << std::endl;

    // C-string declaration
    char str1[] = "Hello";
    char str2[20] = "World";
    const char* str3 = "C-Style";

    std::cout << "str1: " << str1 << std::endl;
    std::cout << "str2: " << str2 << std::endl;
    std::cout << "str3: " << str3 << std::endl;

    // C-string functions
    std::cout << "\nC-string functions:" << std::endl;
    std::cout << "strlen(str1): " << strlen(str1) << std::endl;

    char dest[20];
    strcpy(dest, str1);
    std::cout << "After strcpy: " << dest << std::endl;

    strcat(dest, " ");
    strcat(dest, str2);
    std::cout << "After strcat: " << dest << std::endl;

    std::cout << "strcmp(str1, str2): " << strcmp(str1, str2) << std::endl;

    std::cout << std::endl;
}

void demonstrateStdString() {
    std::cout << "--- std::string ---" << std::endl;

    // String initialization
    std::string s1;                      // Empty string
    std::string s2 = "Hello";           // From C-string
    std::string s3("World");            // Constructor
    std::string s4{s2};                 // Copy
    std::string s5(5, 'A');             // Repeat character
    std::string s6 = s2 + " " + s3;     // Concatenation

    std::cout << "s1: \"" << s1 << "\"" << std::endl;
    std::cout << "s2: \"" << s2 << "\"" << std::endl;
    std::cout << "s3: \"" << s3 << "\"" << std::endl;
    std::cout << "s4: \"" << s4 << "\"" << std::endl;
    std::cout << "s5: \"" << s5 << "\"" << std::endl;
    std::cout << "s6: \"" << s6 << "\"" << std::endl;

    // String properties
    std::cout << "\nString properties:" << std::endl;
    std::cout << "s2.size(): " << s2.size() << std::endl;
    std::cout << "s2.length(): " << s2.length() << std::endl;
    std::cout << "s2.empty(): " << std::boolalpha << s2.empty() << std::endl;
    std::cout << "s2.capacity(): " << s2.capacity() << std::endl;

    // Accessing characters
    std::cout << "\nAccessing characters:" << std::endl;
    std::cout << "s2[0]: " << s2[0] << std::endl;
    std::cout << "s2.at(1): " << s2.at(1) << std::endl;
    std::cout << "s2.front(): " << s2.front() << std::endl;
    std::cout << "s2.back(): " << s2.back() << std::endl;

    // Raw string literals (C++11)
    std::string raw = R"(This is a "raw" string with \n not escaped)";
    std::cout << "\nRaw string: " << raw << std::endl;

    std::cout << std::endl;
}

void demonstrateStringOperations() {
    std::cout << "--- String Operations ---" << std::endl;

    std::string s1 = "Hello";
    std::string s2 = "World";

    // Concatenation
    std::string s3 = s1 + " " + s2;
    std::cout << "Concatenation: " << s3 << std::endl;

    // Append
    s1 += " World";
    std::cout << "After +=: " << s1 << std::endl;

    s1.append("!!!");
    std::cout << "After append: " << s1 << std::endl;

    // Comparison
    std::cout << "\nComparison:" << std::endl;
    std::cout << "(s1 == s2): " << (s1 == s2) << std::endl;
    std::cout << "(s1 != s2): " << (s1 != s2) << std::endl;
    std::cout << "s1.compare(s2): " << s1.compare(s2) << std::endl;

    // Substring
    std::string text = "Hello, World!";
    std::string sub = text.substr(0, 5);
    std::cout << "\nSubstring(0, 5): " << sub << std::endl;
    std::cout << "Substring(7): " << text.substr(7) << std::endl;

    // Find
    std::cout << "\nFind operations:" << std::endl;
    size_t pos = text.find("World");
    std::cout << "Position of 'World': " << pos << std::endl;

    pos = text.find('o');
    std::cout << "First 'o': " << pos << std::endl;

    pos = text.rfind('o');
    std::cout << "Last 'o': " << pos << std::endl;

    // Replace
    std::string msg = "Hello, World!";
    msg.replace(7, 5, "C++");
    std::cout << "\nAfter replace: " << msg << std::endl;

    // Insert
    msg.insert(7, "Beautiful ");
    std::cout << "After insert: " << msg << std::endl;

    // Erase
    msg.erase(7, 10);
    std::cout << "After erase: " << msg << std::endl;

    std::cout << std::endl;
}

void demonstrateStringManipulation() {
    std::cout << "--- String Manipulation ---" << std::endl;

    std::string str = "  Hello, World!  ";
    std::cout << "Original: \"" << str << "\"" << std::endl;

    // Trim (manual implementation)
    auto trim = [](std::string& s) {
        s.erase(0, s.find_first_not_of(" \t\n\r"));
        s.erase(s.find_last_not_of(" \t\n\r") + 1);
    };

    trim(str);
    std::cout << "After trim: \"" << str << "\"" << std::endl;

    // To uppercase
    std::string upper = "hello";
    std::transform(upper.begin(), upper.end(), upper.begin(), ::toupper);
    std::cout << "\nUppercase: " << upper << std::endl;

    // To lowercase
    std::string lower = "WORLD";
    std::transform(lower.begin(), lower.end(), lower.begin(), ::tolower);
    std::cout << "Lowercase: " << lower << std::endl;

    // Reverse
    std::string rev = "Hello";
    std::reverse(rev.begin(), rev.end());
    std::cout << "\nReverse: " << rev << std::endl;

    // Split string
    std::cout << "\nSplit string:" << std::endl;
    std::string data = "apple,banana,cherry";
    std::istringstream ss(data);
    std::string token;
    while (std::getline(ss, token, ',')) {
        std::cout << "  " << token << std::endl;
    }

    // Join strings
    std::vector<std::string> words = {"C++", "is", "awesome"};
    std::string joined;
    for (size_t i = 0; i < words.size(); i++) {
        joined += words[i];
        if (i < words.size() - 1) joined += " ";
    }
    std::cout << "\nJoined: " << joined << std::endl;

    std::cout << std::endl;
}

void demonstrateStringConversion() {
    std::cout << "--- String Conversion ---" << std::endl;

    // Number to string
    int num = 42;
    double pi = 3.14159;

    std::string str1 = std::to_string(num);
    std::string str2 = std::to_string(pi);

    std::cout << "to_string(42): " << str1 << std::endl;
    std::cout << "to_string(3.14159): " << str2 << std::endl;

    // String to number
    std::string numStr = "123";
    std::string floatStr = "45.67";
    std::string hexStr = "0x1A";

    int i = std::stoi(numStr);
    double d = std::stod(floatStr);
    int hex = std::stoi(hexStr, nullptr, 16);

    std::cout << "\nstoi(\"123\"): " << i << std::endl;
    std::cout << "stod(\"45.67\"): " << d << std::endl;
    std::cout << "stoi(\"0x1A\", 16): " << hex << std::endl;

    // Using stringstream
    std::stringstream ss;
    ss << "Value: " << 100 << ", PI: " << 3.14;
    std::cout << "\nStringstream: " << ss.str() << std::endl;

    // C-string conversion
    std::string cppStr = "Hello";
    const char* cStr = cppStr.c_str();
    std::cout << "\nc_str(): " << cStr << std::endl;

    std::cout << std::endl;
}

void demonstrateStringView() {
    std::cout << "--- std::string_view (C++17) ---" << std::endl;

    // string_view: non-owning reference to string
    std::string str = "Hello, World!";
    std::string_view sv = str;

    std::cout << "string_view: " << sv << std::endl;
    std::cout << "Size: " << sv.size() << std::endl;

    // Substring without copying
    std::string_view sub = sv.substr(0, 5);
    std::cout << "Substring: " << sub << std::endl;

    // From C-string
    std::string_view csv = "C-string";
    std::cout << "From C-string: " << csv << std::endl;

    // Efficient function parameter
    auto printStringView = [](std::string_view sv) {
        std::cout << "Received: " << sv << std::endl;
    };

    printStringView("Literal");
    printStringView(str);
    printStringView(sv);

    // WARNING: Dangling reference
    // std::string_view dangling;
    // {
    //     std::string temp = "temporary";
    //     dangling = temp;  // Dangerous!
    // }
    // std::cout << dangling << std::endl;  // Undefined behavior!

    std::cout << std::endl;
}

/*
 * Best Practices:
 *
 * 1. Prefer std::string over C-strings
 * 2. Use std::string_view for read-only string parameters
 * 3. Use raw string literals for regex, paths, etc.
 * 4. Reserve space if you know the final size
 * 5. Use const std::string& for function parameters
 * 6. Be careful with string_view lifetime
 * 7. Use operator+ for simple concatenation
 * 8. Use append() or += for multiple concatenations
 * 9. Use std::to_string for number conversion
 * 10. Handle std::stoi exceptions for invalid input
 */
