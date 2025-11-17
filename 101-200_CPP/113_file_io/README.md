# Program 113: File I/O in C++

## Description
Comprehensive exploration of file input/output operations in C++ covering file streams, reading and writing text files, binary files, file positioning, error handling, and modern filesystem operations. This program demonstrates various techniques for working with files in C++.

## Learning Objectives
- Master file stream operations (ifstream, ofstream, fstream)
- Read and write text files
- Work with binary files
- Handle file positioning and seeking
- Implement error handling for file operations
- Use file modes and flags
- Apply modern filesystem library (C++17)

## Features
- Text file reading and writing
- Binary file operations
- File opening modes
- File stream states and error handling
- File positioning (seekg, seekp, tellg, tellp)
- Line-by-line and word-by-word reading
- Formatted and unformatted I/O
- File existence and manipulation
- Directory operations with std::filesystem

## Compilation and Usage

### Compilation
```bash
cd /home/user/DevOps-prj500/101-200_CPP/113_file_io
g++ -std=c++20 -Wall -Wextra -o file_io main.cpp
```

### Execution
```bash
./file_io
```

## Key Concepts

### 1. Basic File Operations
```cpp
#include <fstream>
#include <iostream>
#include <string>

// Writing to a file
void writeFile() {
    std::ofstream outFile("output.txt");

    if (outFile.is_open()) {
        outFile << "Hello, World!" << std::endl;
        outFile << "Line 2" << std::endl;
        outFile.close();
    } else {
        std::cerr << "Unable to open file for writing\n";
    }
}

// Reading from a file
void readFile() {
    std::ifstream inFile("input.txt");

    if (inFile.is_open()) {
        std::string line;
        while (std::getline(inFile, line)) {
            std::cout << line << '\n';
        }
        inFile.close();
    } else {
        std::cerr << "Unable to open file for reading\n";
    }
}

// Using fstream for both reading and writing
void readWriteFile() {
    std::fstream file("data.txt", std::ios::in | std::ios::out);

    if (file.is_open()) {
        // Write
        file << "Data\n";

        // Read (need to seek back)
        file.seekg(0);
        std::string content;
        file >> content;

        file.close();
    }
}
```

### 2. File Opening Modes
```cpp
// Mode flags
std::ios::in      // Open for reading
std::ios::out     // Open for writing
std::ios::app     // Append to end of file
std::ios::ate     // Seek to end immediately after open
std::ios::trunc   // Truncate file if it exists
std::ios::binary  // Binary mode

// Examples
// Overwrite or create new
std::ofstream out1("file.txt");

// Append to existing file
std::ofstream out2("file.txt", std::ios::app);

// Read and write
std::fstream file1("file.txt", std::ios::in | std::ios::out);

// Binary write
std::ofstream binOut("data.bin", std::ios::binary);

// Read, write, and position at end
std::fstream file2("file.txt", std::ios::in | std::ios::out | std::ios::ate);
```

### 3. Reading Text Files
```cpp
// Read entire file at once
std::string readEntireFile(const std::string& filename) {
    std::ifstream file(filename);
    if (!file) return "";

    return std::string(
        (std::istreambuf_iterator<char>(file)),
        std::istreambuf_iterator<char>()
    );
}

// Read line by line
void readLineByLine(const std::string& filename) {
    std::ifstream file(filename);
    std::string line;
    int lineNum = 1;

    while (std::getline(file, line)) {
        std::cout << lineNum++ << ": " << line << '\n';
    }
}

// Read word by word
void readWordByWord(const std::string& filename) {
    std::ifstream file(filename);
    std::string word;

    while (file >> word) {
        std::cout << word << '\n';
    }
}

// Read character by character
void readCharByChar(const std::string& filename) {
    std::ifstream file(filename);
    char ch;

    while (file.get(ch)) {
        std::cout << ch;
    }
}

// Read with delimiter
void readWithDelimiter(const std::string& filename, char delim = ',') {
    std::ifstream file(filename);
    std::string token;

    while (std::getline(file, token, delim)) {
        std::cout << token << '\n';
    }
}
```

### 4. Writing Text Files
```cpp
// Write strings
void writeStrings(const std::string& filename) {
    std::ofstream file(filename);

    file << "First line" << std::endl;
    file << "Second line" << std::endl;
    file << "Number: " << 42 << '\n';
}

// Write formatted data
void writeFormatted(const std::string& filename) {
    std::ofstream file(filename);

    file << std::setw(10) << "Name"
         << std::setw(10) << "Age"
         << std::setw(10) << "Score" << '\n';

    file << std::setw(10) << "Alice"
         << std::setw(10) << 25
         << std::setw(10) << 95.5 << '\n';
}

// Append to file
void appendToFile(const std::string& filename, const std::string& text) {
    std::ofstream file(filename, std::ios::app);
    file << text << '\n';
}

// Write vector to file
void writeVector(const std::string& filename, const std::vector<int>& vec) {
    std::ofstream file(filename);
    for (const auto& val : vec) {
        file << val << '\n';
    }
}
```

### 5. Binary File Operations
```cpp
// Write binary data
void writeBinary(const std::string& filename) {
    std::ofstream file(filename, std::ios::binary);

    int num = 42;
    double pi = 3.14159;

    file.write(reinterpret_cast<char*>(&num), sizeof(num));
    file.write(reinterpret_cast<char*>(&pi), sizeof(pi));
}

// Read binary data
void readBinary(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary);

    int num;
    double pi;

    file.read(reinterpret_cast<char*>(&num), sizeof(num));
    file.read(reinterpret_cast<char*>(&pi), sizeof(pi));

    std::cout << "Number: " << num << ", Pi: " << pi << '\n';
}

// Write structure to binary file
struct Person {
    char name[50];
    int age;
    double height;
};

void writePersonBinary(const std::string& filename, const Person& p) {
    std::ofstream file(filename, std::ios::binary);
    file.write(reinterpret_cast<const char*>(&p), sizeof(Person));
}

void readPersonBinary(const std::string& filename, Person& p) {
    std::ifstream file(filename, std::ios::binary);
    file.read(reinterpret_cast<char*>(&p), sizeof(Person));
}

// Write array of objects
void writeArrayBinary(const std::string& filename,
                      const std::vector<Person>& people) {
    std::ofstream file(filename, std::ios::binary);

    size_t count = people.size();
    file.write(reinterpret_cast<const char*>(&count), sizeof(count));

    for (const auto& person : people) {
        file.write(reinterpret_cast<const char*>(&person), sizeof(Person));
    }
}
```

### 6. File Positioning
```cpp
void demonstrateFilePositioning() {
    std::fstream file("data.txt", std::ios::in | std::ios::out);

    // Write some data
    file << "0123456789";

    // Get current position
    std::streampos pos = file.tellp();  // Write position
    std::cout << "Write position: " << pos << '\n';

    // Seek to beginning
    file.seekg(0);  // Seek get (read) pointer

    // Seek to end
    file.seekg(0, std::ios::end);

    // Seek relative to current position
    file.seekg(-5, std::ios::cur);

    // Read from specific position
    file.seekg(3);
    char ch;
    file.get(ch);
    std::cout << "Character at position 3: " << ch << '\n';

    // Get file size
    file.seekg(0, std::ios::end);
    std::streampos fileSize = file.tellg();
    std::cout << "File size: " << fileSize << " bytes\n";

    // Seek back to beginning
    file.seekg(0, std::ios::beg);
}
```

### 7. Error Handling
```cpp
void demonstrateErrorHandling() {
    std::ifstream file("nonexistent.txt");

    // Check if file opened successfully
    if (!file.is_open()) {
        std::cerr << "Failed to open file\n";
        return;
    }

    // Check stream state
    if (file.good())    std::cout << "All good\n";
    if (file.eof())     std::cout << "End of file\n";
    if (file.fail())    std::cout << "Logical error\n";
    if (file.bad())     std::cout << "Read/write error\n";

    // Clear error flags
    file.clear();

    // Check after operations
    std::string line;
    while (std::getline(file, line)) {
        if (file.bad()) {
            std::cerr << "Fatal error\n";
            break;
        }
        if (file.fail()) {
            file.clear();
            continue;
        }
        std::cout << line << '\n';
    }
}

// RAII wrapper for file handling
class FileGuard {
    std::fstream file;
public:
    FileGuard(const std::string& filename, std::ios::openmode mode)
        : file(filename, mode) {
        if (!file.is_open()) {
            throw std::runtime_error("Failed to open file: " + filename);
        }
    }

    ~FileGuard() {
        if (file.is_open()) {
            file.close();
        }
    }

    std::fstream& get() { return file; }
};
```

### 8. Filesystem Operations (C++17)
```cpp
#include <filesystem>
namespace fs = std::filesystem;

void demonstrateFilesystem() {
    // Check if file exists
    if (fs::exists("file.txt")) {
        std::cout << "File exists\n";
    }

    // Get file size
    auto size = fs::file_size("file.txt");
    std::cout << "File size: " << size << " bytes\n";

    // Copy file
    fs::copy("source.txt", "destination.txt");

    // Rename file
    fs::rename("old.txt", "new.txt");

    // Remove file
    fs::remove("unwanted.txt");

    // Create directory
    fs::create_directory("mydir");

    // Create directories recursively
    fs::create_directories("path/to/nested/dir");

    // Iterate through directory
    for (const auto& entry : fs::directory_iterator(".")) {
        std::cout << entry.path() << '\n';
    }

    // Recursive directory iteration
    for (const auto& entry : fs::recursive_directory_iterator(".")) {
        if (fs::is_regular_file(entry)) {
            std::cout << entry.path() << " - "
                      << fs::file_size(entry) << " bytes\n";
        }
    }

    // Get current path
    fs::path currentPath = fs::current_path();

    // Path operations
    fs::path p = "dir/subdir/file.txt";
    std::cout << "Parent: " << p.parent_path() << '\n';
    std::cout << "Filename: " << p.filename() << '\n';
    std::cout << "Extension: " << p.extension() << '\n';
    std::cout << "Stem: " << p.stem() << '\n';
}
```

## Best Practices
1. **Always check if file opened successfully**
2. **Use RAII** - files auto-close when going out of scope
3. **Handle errors gracefully** with proper error messages
4. **Use binary mode** for non-text files
5. **Prefer std::filesystem** (C++17) for file operations
6. **Close files explicitly** when done (or let RAII do it)
7. **Use buffered I/O** for better performance
8. **Check stream state** after critical operations
9. **Use appropriate file modes** to prevent data loss
10. **Consider portability** with path separators

## Common Patterns
```cpp
// Read CSV file
std::vector<std::vector<std::string>> readCSV(const std::string& filename) {
    std::vector<std::vector<std::string>> data;
    std::ifstream file(filename);
    std::string line;

    while (std::getline(file, line)) {
        std::vector<std::string> row;
        std::stringstream ss(line);
        std::string cell;

        while (std::getline(ss, cell, ',')) {
            row.push_back(cell);
        }
        data.push_back(row);
    }

    return data;
}

// Write log file
class Logger {
    std::ofstream logFile;
public:
    Logger(const std::string& filename)
        : logFile(filename, std::ios::app) {}

    void log(const std::string& message) {
        auto now = std::chrono::system_clock::now();
        logFile << "[" << std::chrono::system_clock::to_time_t(now)
                << "] " << message << std::endl;
    }
};
```

## Resources and References
- [cppreference.com - File I/O](https://en.cppreference.com/w/cpp/io)
- [cppreference.com - Filesystem](https://en.cppreference.com/w/cpp/filesystem)
- [C++ Core Guidelines - I/O](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rio-iostream)

## Navigation
- **Previous Program**: [112 - Enums](../112_enums/README.md)
- **Next Program**: [114 - Preprocessor](../114_preprocessor/README.md)
- **Back to Main**: [C++ Programs 101-200](../README.md)
