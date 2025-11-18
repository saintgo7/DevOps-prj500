/*
 * Program 113: File I/O in C++
 *
 * Topics Covered:
 * - ifstream (input file stream)
 * - ofstream (output file stream)
 * - fstream (input/output file stream)
 * - File opening modes
 * - Reading from files (line by line, word by word, character by character)
 * - Writing to files
 * - File position and seeking
 * - Binary file I/O
 * - Error handling with files
 * - File existence checking
 *
 * Compilation:
 * g++ -std=c++20 -Wall -Wextra -o file_io main.cpp
 */

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <filesystem>  // C++17

void demonstrateWritingFiles();
void demonstrateReadingFiles();
void demonstrateFileAppend();
void demonstrateBinaryFiles();
void demonstrateErrorHandling();

int main() {
    std::cout << "=== C++ File I/O ===" << std::endl << std::endl;

    demonstrateWritingFiles();
    demonstrateReadingFiles();
    demonstrateFileAppend();
    demonstrateBinaryFiles();
    demonstrateErrorHandling();

    // Cleanup test files - safely check existence first
    if (std::filesystem::exists("output.txt")) std::filesystem::remove("output.txt");
    if (std::filesystem::exists("data.txt")) std::filesystem::remove("data.txt");
    if (std::filesystem::exists("append.txt")) std::filesystem::remove("append.txt");
    if (std::filesystem::exists("binary.dat")) std::filesystem::remove("binary.dat");

    return 0;
}

void demonstrateWritingFiles() {
    std::cout << "--- Writing to Files ---" << std::endl;

    // Create and write to file
    std::ofstream outFile("output.txt");

    if (outFile.is_open()) {
        outFile << "Hello, File I/O!" << std::endl;
        outFile << "Line 2" << std::endl;
        outFile << "Number: " << 42 << std::endl;

        outFile.close();
        std::cout << "File 'output.txt' created and written successfully" << std::endl;
    } else {
        std::cerr << "Unable to open file for writing" << std::endl;
    }

    // RAII approach (automatic close)
    {
        std::ofstream file("data.txt");
        file << "RAII automatically closes the file" << std::endl;
        file << "when it goes out of scope" << std::endl;
    }  // File automatically closed here

    std::cout << "File 'data.txt' created with RAII" << std::endl;

    std::cout << std::endl;
}

void demonstrateReadingFiles() {
    std::cout << "--- Reading from Files ---" << std::endl;

    // Reading line by line
    std::ifstream inFile("output.txt");

    if (inFile.is_open()) {
        std::cout << "Reading line by line:" << std::endl;
        std::string line;
        while (std::getline(inFile, line)) {
            std::cout << "  " << line << std::endl;
        }
        inFile.close();
    }

    // Reading word by word
    inFile.open("data.txt");
    if (inFile.is_open()) {
        std::cout << "\nReading word by word:" << std::endl;
        std::string word;
        while (inFile >> word) {
            std::cout << "  Word: " << word << std::endl;
        }
        inFile.close();
    }

    // Reading character by character
    inFile.open("output.txt");
    if (inFile.is_open()) {
        std::cout << "\nFirst 20 characters:" << std::endl;
        char ch;
        int count = 0;
        while (inFile.get(ch) && count < 20) {
            std::cout << ch;
            count++;
        }
        std::cout << std::endl;
        inFile.close();
    }

    // Reading entire file into string
    inFile.open("output.txt");
    if (inFile.is_open()) {
        std::string content((std::istreambuf_iterator<char>(inFile)),
                           std::istreambuf_iterator<char>());
        std::cout << "\nEntire file content:" << std::endl;
        std::cout << content;
        inFile.close();
    }

    std::cout << std::endl;
}

void demonstrateFileAppend() {
    std::cout << "--- Appending to Files ---" << std::endl;

    // Create initial file
    std::ofstream file("append.txt");
    file << "Initial line" << std::endl;
    file.close();

    // Append to file
    file.open("append.txt", std::ios::app);
    if (file.is_open()) {
        file << "Appended line 1" << std::endl;
        file << "Appended line 2" << std::endl;
        file.close();
        std::cout << "Lines appended successfully" << std::endl;
    }

    // Read and display
    std::ifstream inFile("append.txt");
    if (inFile.is_open()) {
        std::cout << "File contents:" << std::endl;
        std::string line;
        while (std::getline(inFile, line)) {
            std::cout << "  " << line << std::endl;
        }
        inFile.close();
    }

    std::cout << std::endl;
}

void demonstrateBinaryFiles() {
    std::cout << "--- Binary File I/O ---" << std::endl;

    // Writing binary data
    std::ofstream binFile("binary.dat", std::ios::binary);
    if (binFile.is_open()) {
        int numbers[] = {10, 20, 30, 40, 50};
        binFile.write(reinterpret_cast<char*>(numbers), sizeof(numbers));
        binFile.close();
        std::cout << "Binary data written" << std::endl;
    }

    // Reading binary data
    std::ifstream binInFile("binary.dat", std::ios::binary);
    if (binInFile.is_open()) {
        int readNumbers[5];
        binInFile.read(reinterpret_cast<char*>(readNumbers), sizeof(readNumbers));
        binInFile.close();

        std::cout << "Binary data read: ";
        for (int num : readNumbers) {
            std::cout << num << " ";
        }
        std::cout << std::endl;
    }

    // File position and seeking
    std::fstream file("output.txt", std::ios::in);
    if (file.is_open()) {
        // Get current position
        std::streampos pos = file.tellg();
        std::cout << "\nCurrent position: " << pos << std::endl;

        // Seek to position 5
        file.seekg(5);
        char ch;
        file.get(ch);
        std::cout << "Character at position 5: " << ch << std::endl;

        // Seek to end
        file.seekg(0, std::ios::end);
        std::streampos fileSize = file.tellg();
        std::cout << "File size: " << fileSize << " bytes" << std::endl;

        file.close();
    }

    std::cout << std::endl;
}

void demonstrateErrorHandling() {
    std::cout << "--- Error Handling ---" << std::endl;

    // Check if file exists (C++17)
    if (std::filesystem::exists("output.txt")) {
        std::cout << "File 'output.txt' exists" << std::endl;
    }

    // Try to open non-existent file
    std::ifstream file("nonexistent.txt");
    if (!file.is_open()) {
        std::cout << "Failed to open 'nonexistent.txt'" << std::endl;
    }

    // Check error state
    file.open("output.txt");
    if (file.is_open()) {
        std::cout << "\nFile opened successfully" << std::endl;
        std::cout << "good(): " << file.good() << std::endl;
        std::cout << "eof(): " << file.eof() << std::endl;
        std::cout << "fail(): " << file.fail() << std::endl;
        std::cout << "bad(): " << file.bad() << std::endl;

        // Read entire file
        std::string line;
        while (std::getline(file, line)) {
            // Reading...
        }

        std::cout << "\nAfter reading to EOF:" << std::endl;
        std::cout << "eof(): " << file.eof() << std::endl;

        // Clear error state
        file.clear();
        file.seekg(0);  // Go back to beginning
        std::cout << "After clear() and seekg(0):" << std::endl;
        std::cout << "good(): " << file.good() << std::endl;

        file.close();
    }

    std::cout << std::endl;
}

/*
 * File Opening Modes:
 * - std::ios::in     - Open for reading
 * - std::ios::out    - Open for writing
 * - std::ios::app    - Append to end of file
 * - std::ios::ate    - Seek to end immediately after open
 * - std::ios::trunc  - Truncate file if it exists
 * - std::ios::binary - Open in binary mode
 *
 * Modes can be combined with |:
 * std::ios::out | std::ios::binary
 *
 * Best Practices:
 * 1. Always check if file opened successfully
 * 2. Use RAII (file closes automatically when out of scope)
 * 3. Use std::filesystem for file operations (C++17)
 * 4. Close files explicitly when done if needed early
 * 5. Handle errors appropriately
 * 6. Use binary mode for non-text files
 * 7. Prefer std::getline for reading lines
 * 8. Check error states after I/O operations
 * 9. Use exceptions for error handling in production code
 * 10. Be mindful of file encoding (UTF-8, etc.)
 */
