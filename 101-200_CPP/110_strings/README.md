# Program 110: Strings in C++

## Description
Comprehensive exploration of string handling in C++ covering C-style strings, std::string class, string operations, string manipulation, string algorithms, and string conversions. This program demonstrates both traditional C-style and modern C++ string handling techniques.

## Learning Objectives
- Understand C-style strings (char arrays)
- Master std::string class operations
- Perform string manipulation and transformations
- Use string algorithms and iterators
- Convert between string types
- Work with string streams
- Apply string best practices

## Features
- C-style string operations
- std::string creation and initialization
- String concatenation and appending
- String searching and finding
- String comparison and sorting
- Substring operations
- String modification (insert, erase, replace)
- String conversions (to/from numbers)
- String algorithms (transform, reverse, etc.)
- String stream operations

## Compilation and Usage

### Compilation
```bash
cd /home/user/DevOps-prj500/101-200_CPP/110_strings
g++ -std=c++20 -Wall -Wextra -o strings main.cpp
```

### Execution
```bash
./strings
```

## Key Concepts

### 1. C-Style Strings
```cpp
#include <cstring>

// Declaration and initialization
char str1[] = "Hello";           // Null-terminated
char str2[20] = "World";         // Fixed size
char str3[] = {'H', 'i', '\0'};  // Manual termination

// String length
int len = strlen(str1);          // 5

// String copy
char dest[20];
strcpy(dest, str1);              // Copy str1 to dest
strncpy(dest, str1, 19);         // Safe copy (with limit)

// String concatenation
strcat(dest, " World");          // Append
strncat(dest, "!", 1);           // Safe append

// String comparison
int result = strcmp(str1, str2); // 0 if equal, <0 or >0

// String search
char* pos = strchr(str1, 'l');   // Find character
char* substr = strstr(str1, "ll"); // Find substring
```

### 2. std::string Basics
```cpp
#include <string>

// Creation and initialization
std::string s1;                  // Empty string
std::string s2 = "Hello";        // From C-string
std::string s3("World");         // Constructor
std::string s4(5, 'A');          // "AAAAA"
std::string s5{s2};              // Copy
std::string s6 = s2 + " " + s3;  // Concatenation

// Size operations
s2.length();                     // 5
s2.size();                       // 5 (same as length)
s2.empty();                      // false
s2.capacity();                   // Reserved space
s2.max_size();                   // Maximum possible size

// Access
char c1 = s2[0];                 // 'H' (no bounds check)
char c2 = s2.at(1);              // 'e' (with bounds check)
char first = s2.front();         // 'H'
char last = s2.back();           // 'o'
```

### 3. String Operations
```cpp
// Concatenation
std::string s1 = "Hello";
std::string s2 = "World";
std::string s3 = s1 + " " + s2;  // "Hello World"
s1 += " there";                  // "Hello there"
s1.append("!");                  // "Hello there!"

// Insertion
s1.insert(5, " C++");            // Insert at position
s1.insert(0, ">> ");             // Insert at beginning

// Erasing
s1.erase(0, 3);                  // Erase from position
s1.erase(s1.begin());            // Erase first character
s1.clear();                      // Empty string

// Replacement
s1 = "Hello World";
s1.replace(0, 5, "Hi");          // "Hi World"

// Substring
std::string sub = s1.substr(3, 5); // From pos 3, length 5
std::string rest = s1.substr(3);   // From pos 3 to end
```

### 4. String Searching
```cpp
std::string text = "The quick brown fox jumps over the lazy dog";

// Find substring
size_t pos = text.find("fox");              // 16
if (pos != std::string::npos) {
    std::cout << "Found at: " << pos;
}

// Find from position
pos = text.find("the", 10);                 // Find after pos 10

// Find character
pos = text.find('q');                       // 4

// Find last occurrence
pos = text.rfind("o");                      // Last 'o'

// Find first of any character
pos = text.find_first_of("aeiou");          // First vowel

// Find first not of
pos = text.find_first_not_of(" The");       // First non-matching

// Count occurrences
int count = 0;
pos = 0;
while ((pos = text.find("o", pos)) != std::string::npos) {
    count++;
    pos++;
}
```

### 5. String Comparison
```cpp
std::string s1 = "apple";
std::string s2 = "banana";

// Comparison operators
bool eq = (s1 == s2);                // false
bool neq = (s1 != s2);               // true
bool less = (s1 < s2);               // true (lexicographic)

// Compare method
int result = s1.compare(s2);         // <0 if s1 < s2
result = s1.compare(0, 3, s2);       // Compare substring
result = s1.compare(0, 3, "app");    // Compare with C-string

// Case-insensitive comparison (custom)
bool equalIgnoreCase(const std::string& a, const std::string& b) {
    return std::equal(a.begin(), a.end(), b.begin(), b.end(),
        [](char a, char b) {
            return tolower(a) == tolower(b);
        });
}
```

### 6. String Conversions
```cpp
#include <sstream>

// Number to string
int num = 42;
std::string s1 = std::to_string(num);        // "42"
double pi = 3.14159;
std::string s2 = std::to_string(pi);         // "3.141590"

// String to number
std::string numStr = "123";
int n = std::stoi(numStr);                   // 123
long l = std::stol(numStr);                  // 123L
double d = std::stod("3.14");                // 3.14
float f = std::stof("2.71");                 // 2.71f

// With base
int hex = std::stoi("FF", nullptr, 16);      // 255

// Error handling
try {
    int value = std::stoi("not_a_number");
} catch (const std::invalid_argument& e) {
    std::cerr << "Invalid argument\n";
} catch (const std::out_of_range& e) {
    std::cerr << "Out of range\n";
}
```

### 7. String Streams
```cpp
#include <sstream>

// String stream for formatting
std::ostringstream oss;
oss << "Value: " << 42 << ", Pi: " << 3.14;
std::string result = oss.str();

// Parsing strings
std::istringstream iss("10 20 30");
int a, b, c;
iss >> a >> b >> c;                          // Parse integers

// Token parsing
std::string data = "apple,banana,cherry";
std::istringstream tokenStream(data);
std::string token;
while (std::getline(tokenStream, token, ',')) {
    std::cout << token << '\n';
}

// String stream for conversions
template<typename T>
std::string toString(const T& value) {
    std::ostringstream oss;
    oss << value;
    return oss.str();
}
```

### 8. String Algorithms
```cpp
#include <algorithm>
#include <cctype>

std::string str = "Hello World";

// Transform to uppercase
std::transform(str.begin(), str.end(), str.begin(), ::toupper);
// "HELLO WORLD"

// Transform to lowercase
std::transform(str.begin(), str.end(), str.begin(), ::tolower);
// "hello world"

// Reverse
std::reverse(str.begin(), str.end());
// "dlrow olleh"

// Remove spaces
str.erase(std::remove(str.begin(), str.end(), ' '), str.end());

// Check if all digits
bool allDigits = std::all_of(str.begin(), str.end(), ::isdigit);

// Count character
int count = std::count(str.begin(), str.end(), 'l');

// Replace all occurrences
void replaceAll(std::string& str, const std::string& from,
                const std::string& to) {
    size_t pos = 0;
    while ((pos = str.find(from, pos)) != std::string::npos) {
        str.replace(pos, from.length(), to);
        pos += to.length();
    }
}
```

### 9. String Views (C++17)
```cpp
#include <string_view>

// Non-owning string reference
void process(std::string_view sv) {
    std::cout << sv;  // No copy
}

std::string s = "Hello";
process(s);           // Works with std::string
process("World");     // Works with literals

// Efficient substring viewing
std::string_view sv = "Hello World";
std::string_view sub = sv.substr(0, 5);  // No allocation
```

## Best Practices
1. **Prefer std::string over C-style strings**
2. **Use std::string_view (C++17)** for non-owning string references
3. **Reserve capacity** for known large strings
4. **Use const std::string&** for read-only parameters
5. **Check std::string::npos** when using find operations
6. **Use string literals efficiently** with ""sv suffix
7. **Avoid excessive concatenation** in loops (use string stream)
8. **Handle conversion exceptions** when parsing strings
9. **Use raw string literals** for complex strings with escapes
10. **Prefer std::to_string** over stringstream for simple conversions

## Common Patterns
```cpp
// Trim whitespace
std::string trim(const std::string& str) {
    auto start = str.find_first_not_of(" \t\n\r");
    auto end = str.find_last_not_of(" \t\n\r");
    return (start == std::string::npos) ? "" : str.substr(start, end - start + 1);
}

// Split string
std::vector<std::string> split(const std::string& str, char delimiter) {
    std::vector<std::string> tokens;
    std::string token;
    std::istringstream stream(str);
    while (std::getline(stream, token, delimiter)) {
        tokens.push_back(token);
    }
    return tokens;
}

// Join strings
std::string join(const std::vector<std::string>& strs, const std::string& delimiter) {
    std::ostringstream oss;
    for (size_t i = 0; i < strs.size(); ++i) {
        if (i > 0) oss << delimiter;
        oss << strs[i];
    }
    return oss.str();
}
```

## Resources and References
- [cppreference.com - std::string](https://en.cppreference.com/w/cpp/string/basic_string)
- [cppreference.com - std::string_view](https://en.cppreference.com/w/cpp/string/basic_string_view)
- [C++ Core Guidelines - Strings](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#SS-string)

## Navigation
- **Previous Program**: [109 - References](../109_references/README.md)
- **Next Program**: [111 - Structures](../111_structures/README.md)
- **Back to Main**: [C++ Programs 101-200](../README.md)
