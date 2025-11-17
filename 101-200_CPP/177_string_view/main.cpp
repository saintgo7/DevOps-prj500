/*
 * Program 177: std::string_view - Non-Owning String References
 *
 * This program demonstrates:
 * - std::string_view basics (C++17)
 * - Non-owning string references
 * - Performance benefits over std::string
 * - String operations and slicing
 * - Common pitfalls and best practices
 */

#include <iostream>
#include <string>
#include <string_view>
#include <vector>
#include <algorithm>
#include <chrono>

// ==============================================
// 1. string_view Basics
// ==============================================

void printString(std::string_view sv) {
    std::cout << "String: " << sv << "\n";
    std::cout << "Length: " << sv.length() << "\n";
}

void stringViewBasicsDemo() {
    std::cout << "\n=== 1. string_view Basics ===\n";

    // From string literal
    std::string_view sv1 = "Hello, World!";
    printString(sv1);

    // From std::string
    std::string str = "C++17";
    std::string_view sv2 = str;
    printString(sv2);

    // From C-string
    const char* cstr = "C-string";
    std::string_view sv3 = cstr;
    printString(sv3);

    // From pointer and length
    std::string_view sv4(cstr, 3); // "C-s"
    std::cout << "Substring: " << sv4 << "\n";
}

// ==============================================
// 2. No Ownership, No Copying
// ==============================================

void noOwnershipDemo() {
    std::cout << "\n=== 2. No Ownership, No Copying ===\n";

    // string_view does NOT own the string
    const char* data = "Original data";
    std::string_view sv = data;

    std::cout << "string_view: " << sv << "\n";
    std::cout << "Pointer: " << static_cast<const void*>(sv.data()) << "\n";
    std::cout << "Original: " << static_cast<const void*>(data) << "\n";

    // Same pointer - no copy!
    std::cout << "Points to same data: "
              << std::boolalpha << (sv.data() == data) << "\n";
}

// ==============================================
// 3. Performance Benefits
// ==============================================

// Old style - copies string
std::string oldExtractWord(const std::string& text, size_t pos) {
    size_t end = text.find(' ', pos);
    if (end == std::string::npos) {
        return text.substr(pos);
    }
    return text.substr(pos, end - pos);
}

// New style - no copy
std::string_view newExtractWord(std::string_view text, size_t pos) {
    size_t end = text.find(' ', pos);
    if (end == std::string_view::npos) {
        return text.substr(pos);
    }
    return text.substr(pos, end - pos);
}

void performanceDemo() {
    std::cout << "\n=== 3. Performance Benefits ===\n";

    std::string text = "The quick brown fox jumps over the lazy dog";

    // Benchmark old style
    auto start1 = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < 100000; ++i) {
        auto word = oldExtractWord(text, 4);
    }
    auto end1 = std::chrono::high_resolution_clock::now();
    auto duration1 = std::chrono::duration_cast<std::chrono::microseconds>(end1 - start1);

    // Benchmark new style
    auto start2 = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < 100000; ++i) {
        auto word = newExtractWord(text, 4);
    }
    auto end2 = std::chrono::high_resolution_clock::now();
    auto duration2 = std::chrono::duration_cast<std::chrono::microseconds>(end2 - start2);

    std::cout << "Old style (string): " << duration1.count() << " μs\n";
    std::cout << "New style (string_view): " << duration2.count() << " μs\n";
    std::cout << "Speedup: " << (duration1.count() / (double)duration2.count()) << "x\n";
}

// ==============================================
// 4. String Operations
// ==============================================

void operationsDemo() {
    std::cout << "\n=== 4. String Operations ===\n";

    std::string_view sv = "Hello, World!";

    // Substring
    std::string_view sub = sv.substr(7, 5); // "World"
    std::cout << "Substring: " << sub << "\n";

    // Remove prefix/suffix
    std::string_view sv2 = "prefix_content_suffix";
    sv2.remove_prefix(7); // Remove "prefix_"
    std::cout << "After remove_prefix: " << sv2 << "\n";

    sv2.remove_suffix(7); // Remove "_suffix"
    std::cout << "After remove_suffix: " << sv2 << "\n";

    // Find
    std::string_view text = "The quick brown fox";
    size_t pos = text.find("quick");
    if (pos != std::string_view::npos) {
        std::cout << "Found 'quick' at position: " << pos << "\n";
    }

    // Starts with / ends with (C++20)
    std::string_view filename = "document.txt";
    // C++20: filename.starts_with("doc") && filename.ends_with(".txt")
    bool starts = filename.substr(0, 3) == "doc";
    bool ends = filename.substr(filename.size() - 4) == ".txt";
    std::cout << "Starts with 'doc': " << std::boolalpha << starts << "\n";
    std::cout << "Ends with '.txt': " << ends << "\n";
}

// ==============================================
// 5. Iteration and Access
// ==============================================

void iterationDemo() {
    std::cout << "\n=== 5. Iteration and Access ===\n";

    std::string_view sv = "C++17";

    // Range-based for loop
    std::cout << "Characters: ";
    for (char c : sv) {
        std::cout << c << " ";
    }
    std::cout << "\n";

    // Iterator access
    std::cout << "Using iterators: ";
    for (auto it = sv.begin(); it != sv.end(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << "\n";

    // Index access
    std::cout << "First char: " << sv[0] << "\n";
    std::cout << "Last char: " << sv[sv.size() - 1] << "\n";

    // at() with bounds checking
    try {
        char c = sv.at(10); // Out of bounds
        std::cout << c;
    } catch (const std::out_of_range& e) {
        std::cout << "Exception: " << e.what() << "\n";
    }
}

// ==============================================
// 6. Comparison
// ==============================================

void comparisonDemo() {
    std::cout << "\n=== 6. Comparison ===\n";

    std::string_view sv1 = "apple";
    std::string_view sv2 = "banana";
    std::string_view sv3 = "apple";

    std::cout << std::boolalpha;
    std::cout << "sv1 == sv2: " << (sv1 == sv2) << "\n";
    std::cout << "sv1 == sv3: " << (sv1 == sv3) << "\n";
    std::cout << "sv1 < sv2: " << (sv1 < sv2) << "\n";

    // Compare with string
    std::string str = "apple";
    std::cout << "sv1 == str: " << (sv1 == str) << "\n";

    // Compare with C-string
    std::cout << "sv1 == \"apple\": " << (sv1 == "apple") << "\n";
}

// ==============================================
// 7. Splitting Strings
// ==============================================

std::vector<std::string_view> split(std::string_view str, char delimiter) {
    std::vector<std::string_view> result;
    size_t start = 0;
    size_t end = str.find(delimiter);

    while (end != std::string_view::npos) {
        result.push_back(str.substr(start, end - start));
        start = end + 1;
        end = str.find(delimiter, start);
    }

    result.push_back(str.substr(start));
    return result;
}

void splittingDemo() {
    std::cout << "\n=== 7. Splitting Strings ===\n";

    std::string text = "one,two,three,four,five";
    auto parts = split(text, ',');

    std::cout << "Split '" << text << "' by comma:\n";
    for (size_t i = 0; i < parts.size(); ++i) {
        std::cout << "  [" << i << "] " << parts[i] << "\n";
    }

    std::cout << "\nNo string copies were made during split!\n";
}

// ==============================================
// 8. Trimming Whitespace
// ==============================================

std::string_view trim(std::string_view sv) {
    const char* whitespace = " \t\n\r";

    // Trim left
    size_t start = sv.find_first_not_of(whitespace);
    if (start == std::string_view::npos) {
        return "";
    }
    sv.remove_prefix(start);

    // Trim right
    size_t end = sv.find_last_not_of(whitespace);
    sv.remove_suffix(sv.size() - end - 1);

    return sv;
}

void trimmingDemo() {
    std::cout << "\n=== 8. Trimming Whitespace ===\n";

    std::string_view sv = "   Hello, World!   \t\n";

    std::cout << "Original: '" << sv << "'\n";
    std::cout << "Trimmed: '" << trim(sv) << "'\n";
}

// ==============================================
// 9. Common Pitfalls - Dangling References
// ==============================================

std::string_view danglingExample() {
    std::string temp = "Temporary string";
    return temp; // DANGER: Returns view to temporary!
}

void pitfallsDemo() {
    std::cout << "\n=== 9. Common Pitfalls ===\n";

    std::cout << "DANGER: string_view doesn't own data!\n\n";

    // Pitfall 1: Temporary strings
    std::cout << "Pitfall 1 - Temporary string:\n";
    // std::string_view sv = std::string("Temp"); // DANGER!
    // std::cout << sv << "\n"; // Undefined behavior

    std::string str = std::string("Safe");
    std::string_view sv = str; // OK: string outlives string_view
    std::cout << "  Safe: " << sv << "\n";

    // Pitfall 2: Modified underlying string
    std::cout << "\nPitfall 2 - Modified string:\n";
    std::string text = "Original";
    std::string_view view = text;
    std::cout << "  Before: " << view << "\n";

    text = "Modified"; // view now points to different data!
    // std::cout << "  After: " << view << "\n"; // May be invalid!

    // Pitfall 3: Null termination
    std::cout << "\nPitfall 3 - Not null-terminated:\n";
    std::string_view sv3 = "Hello, World!";
    sv3.remove_suffix(7); // "Hello"
    // sv3.data() is NOT null-terminated!
    std::cout << "  Length: " << sv3.length() << "\n";
    std::cout << "  Use .data() + .size(), not as C-string!\n";
}

// ==============================================
// 10. Converting to std::string
// ==============================================

void conversionDemo() {
    std::cout << "\n=== 10. Converting to std::string ===\n";

    std::string_view sv = "string_view content";

    // Explicit conversion to string
    std::string str1(sv); // Constructor
    std::string str2 = std::string(sv); // Explicit cast
    std::string str3(sv.data(), sv.size()); // From data and size

    std::cout << "string 1: " << str1 << "\n";
    std::cout << "string 2: " << str2 << "\n";
    std::cout << "string 3: " << str3 << "\n";

    // Note: No implicit conversion
    // std::string str4 = sv; // Error!
}

// ==============================================
// 11. Use Cases and Best Practices
// ==============================================

// Good: Read-only string parameter
void processText(std::string_view text) {
    std::cout << "Processing: " << text << "\n";
}

// Good: Return substring without copying
std::string_view getFileExtension(std::string_view filename) {
    size_t pos = filename.find_last_of('.');
    if (pos != std::string_view::npos) {
        return filename.substr(pos);
    }
    return "";
}

// Good: Tokenization without allocation
std::vector<std::string_view> tokenize(std::string_view text) {
    std::vector<std::string_view> tokens;
    size_t pos = 0;

    while (pos < text.size()) {
        // Skip whitespace
        while (pos < text.size() && text[pos] == ' ') ++pos;

        // Find word end
        size_t start = pos;
        while (pos < text.size() && text[pos] != ' ') ++pos;

        if (start < pos) {
            tokens.push_back(text.substr(start, pos - start));
        }
    }

    return tokens;
}

void bestPracticesDemo() {
    std::cout << "\n=== 11. Use Cases and Best Practices ===\n";

    // Works with any string type - no conversion
    processText("literal");
    processText(std::string("std::string"));

    std::string filename = "document.pdf";
    std::string_view ext = getFileExtension(filename);
    std::cout << "Extension: " << ext << "\n";

    std::string text = "The quick brown fox jumps";
    auto tokens = tokenize(text);

    std::cout << "Tokens: ";
    for (const auto& token : tokens) {
        std::cout << token << " ";
    }
    std::cout << "\n";

    std::cout << "\nBest practices:\n";
    std::cout << "  1. Use for read-only string parameters\n";
    std::cout << "  2. Great for string parsing and tokenization\n";
    std::cout << "  3. Avoid storing in containers long-term\n";
    std::cout << "  4. Don't return string_view from temporaries\n";
    std::cout << "  5. Remember: not null-terminated!\n";
}

// ==============================================
// 12. std::string vs std::string_view
// ==============================================

void comparisonTableDemo() {
    std::cout << "\n=== 12. std::string vs std::string_view ===\n\n";

    std::cout << "std::string:\n";
    std::cout << "  + Owns the string data\n";
    std::cout << "  + Always null-terminated\n";
    std::cout << "  + Safe for storage\n";
    std::cout << "  + Can be modified\n";
    std::cout << "  - Allocates memory\n";
    std::cout << "  - Copies on substring\n\n";

    std::cout << "std::string_view:\n";
    std::cout << "  + Non-owning (lightweight)\n";
    std::cout << "  + No allocations or copies\n";
    std::cout << "  + Fast substring operations\n";
    std::cout << "  + Works with any string source\n";
    std::cout << "  - Not null-terminated\n";
    std::cout << "  - Dangling reference risk\n";
    std::cout << "  - Read-only\n\n";

    std::cout << "Use string_view for:\n";
    std::cout << "  - Function parameters (read-only)\n";
    std::cout << "  - Temporary string operations\n";
    std::cout << "  - Performance-critical parsing\n\n";

    std::cout << "Use string for:\n";
    std::cout << "  - Storing strings\n";
    std::cout << "  - String modification\n";
    std::cout << "  - Return values (ownership)\n";
}

int main() {
    std::cout << "=== C++17 std::string_view ===\n";

    // 1. Basics
    stringViewBasicsDemo();

    // 2. No ownership
    noOwnershipDemo();

    // 3. Performance
    performanceDemo();

    // 4. Operations
    operationsDemo();

    // 5. Iteration
    iterationDemo();

    // 6. Comparison
    comparisonDemo();

    // 7. Splitting
    splittingDemo();

    // 8. Trimming
    trimmingDemo();

    // 9. Pitfalls
    pitfallsDemo();

    // 10. Conversion
    conversionDemo();

    // 11. Best practices
    bestPracticesDemo();

    // 12. Comparison table
    comparisonTableDemo();

    std::cout << "\n=== Key Takeaways ===\n";
    std::cout << "1. string_view is non-owning reference to string (C++17)\n";
    std::cout << "2. No copies, no allocations - very efficient\n";
    std::cout << "3. Perfect for read-only string parameters\n";
    std::cout << "4. Supports substring without copying\n";
    std::cout << "5. NOT null-terminated - use .data() + .size()\n";
    std::cout << "6. Beware dangling references to temporaries\n";
    std::cout << "7. Great for parsing, tokenization, string analysis\n";

    return 0;
}
