/*
 * Program 179: std::filesystem - File and Directory Operations
 *
 * This program demonstrates:
 * - std::filesystem library (C++17)
 * - Path manipulation
 * - Directory iteration
 * - File operations and queries
 * - Practical filesystem tasks
 */

#include <iostream>
#include <filesystem>
#include <fstream>
#include <string>
#include <vector>
#include <chrono>

namespace fs = std::filesystem;

// ==============================================
// 1. Path Basics
// ==============================================

void pathBasicsDemo() {
    std::cout << "\n=== 1. Path Basics ===\n";

    // Create paths
    fs::path p1 = "/home/user/documents/file.txt";
    fs::path p2("C:\\Windows\\System32\\");
    fs::path p3 = fs::current_path();

    std::cout << "Path 1: " << p1 << "\n";
    std::cout << "Path 2: " << p2 << "\n";
    std::cout << "Current path: " << p3 << "\n";

    // Path components
    std::cout << "\nPath components of " << p1 << ":\n";
    std::cout << "  root_name: " << p1.root_name() << "\n";
    std::cout << "  root_directory: " << p1.root_directory() << "\n";
    std::cout << "  root_path: " << p1.root_path() << "\n";
    std::cout << "  relative_path: " << p1.relative_path() << "\n";
    std::cout << "  parent_path: " << p1.parent_path() << "\n";
    std::cout << "  filename: " << p1.filename() << "\n";
    std::cout << "  stem: " << p1.stem() << "\n";
    std::cout << "  extension: " << p1.extension() << "\n";
}

// ==============================================
// 2. Path Manipulation
// ==============================================

void pathManipulationDemo() {
    std::cout << "\n=== 2. Path Manipulation ===\n";

    fs::path base = "/home/user";

    // Append paths with /
    fs::path p1 = base / "documents" / "file.txt";
    std::cout << "Appended: " << p1 << "\n";

    // Concatenate strings
    fs::path p2 = base;
    p2 += "/downloads";
    std::cout << "Concatenated: " << p2 << "\n";

    // Replace filename
    fs::path p3 = p1;
    p3.replace_filename("newfile.txt");
    std::cout << "Replace filename: " << p3 << "\n";

    // Replace extension
    fs::path p4 = p1;
    p4.replace_extension(".md");
    std::cout << "Replace extension: " << p4 << "\n";

    // Remove filename
    fs::path p5 = p1;
    p5.remove_filename();
    std::cout << "Remove filename: " << p5 << "\n";

    // Make preferred (platform-specific separators)
    fs::path p6 = "dir1/dir2\\dir3/file.txt";
    std::cout << "Make preferred: " << p6.make_preferred() << "\n";
}

// ==============================================
// 3. Path Queries
// ==============================================

void pathQueriesDemo() {
    std::cout << "\n=== 3. Path Queries ===\n";

    fs::path p = "/home/user/documents/report.pdf";

    std::cout << std::boolalpha;
    std::cout << "Path: " << p << "\n";
    std::cout << "  has_root_path: " << p.has_root_path() << "\n";
    std::cout << "  has_root_name: " << p.has_root_name() << "\n";
    std::cout << "  has_root_directory: " << p.has_root_directory() << "\n";
    std::cout << "  has_relative_path: " << p.has_relative_path() << "\n";
    std::cout << "  has_parent_path: " << p.has_parent_path() << "\n";
    std::cout << "  has_filename: " << p.has_filename() << "\n";
    std::cout << "  has_stem: " << p.has_stem() << "\n";
    std::cout << "  has_extension: " << p.has_extension() << "\n";
    std::cout << "  is_absolute: " << p.is_absolute() << "\n";
    std::cout << "  is_relative: " << p.is_relative() << "\n";
}

// ==============================================
// 4. Filesystem Status
// ==============================================

void filesystemStatusDemo() {
    std::cout << "\n=== 4. Filesystem Status ===\n";

    // Create test file
    fs::path testFile = "test_file.txt";
    {
        std::ofstream out(testFile);
        out << "Test content";
    }

    // Check existence
    std::cout << std::boolalpha;
    std::cout << "File '" << testFile << "' exists: "
              << fs::exists(testFile) << "\n";

    // File type checks
    std::cout << "  is_regular_file: " << fs::is_regular_file(testFile) << "\n";
    std::cout << "  is_directory: " << fs::is_directory(testFile) << "\n";
    std::cout << "  is_symlink: " << fs::is_symlink(testFile) << "\n";

    // File size
    std::cout << "  file_size: " << fs::file_size(testFile) << " bytes\n";

    // Last write time
    auto ftime = fs::last_write_time(testFile);
    std::cout << "  has last_write_time\n";

    // Cleanup
    fs::remove(testFile);
}

// ==============================================
// 5. Directory Operations
// ==============================================

void directoryOperationsDemo() {
    std::cout << "\n=== 5. Directory Operations ===\n";

    fs::path testDir = "test_directory";

    // Create directory
    if (fs::create_directory(testDir)) {
        std::cout << "Created directory: " << testDir << "\n";
    }

    // Create nested directories
    fs::path nested = testDir / "level1" / "level2" / "level3";
    if (fs::create_directories(nested)) {
        std::cout << "Created nested directories: " << nested << "\n";
    }

    // Check directory
    std::cout << std::boolalpha;
    std::cout << "Is directory: " << fs::is_directory(testDir) << "\n";

    // Current directory
    std::cout << "Current directory: " << fs::current_path() << "\n";

    // Cleanup
    fs::remove_all(testDir);
    std::cout << "Removed directory tree\n";
}

// ==============================================
// 6. Directory Iteration
// ==============================================

void directoryIterationDemo() {
    std::cout << "\n=== 6. Directory Iteration ===\n";

    // Create test structure
    fs::path testDir = "iteration_test";
    fs::create_directory(testDir);

    // Create some files
    for (int i = 1; i <= 3; ++i) {
        std::ofstream out(testDir / ("file" + std::to_string(i) + ".txt"));
        out << "Content " << i;
    }

    // Create subdirectory with files
    fs::path subdir = testDir / "subdir";
    fs::create_directory(subdir);
    std::ofstream(subdir / "nested.txt") << "Nested";

    // Iterate directory (non-recursive)
    std::cout << "\nNon-recursive iteration:\n";
    for (const auto& entry : fs::directory_iterator(testDir)) {
        std::cout << "  " << entry.path().filename();
        if (entry.is_directory()) {
            std::cout << " [DIR]";
        }
        std::cout << "\n";
    }

    // Recursive iteration
    std::cout << "\nRecursive iteration:\n";
    for (const auto& entry : fs::recursive_directory_iterator(testDir)) {
        // Indentation based on depth
        std::string indent(entry.depth() * 2, ' ');
        std::cout << indent << entry.path().filename();
        if (entry.is_directory()) {
            std::cout << " [DIR]";
        }
        std::cout << "\n";
    }

    // Cleanup
    fs::remove_all(testDir);
}

// ==============================================
// 7. File Operations
// ==============================================

void fileOperationsDemo() {
    std::cout << "\n=== 7. File Operations ===\n";

    fs::path source = "source.txt";
    fs::path dest = "destination.txt";

    // Create source file
    {
        std::ofstream out(source);
        out << "Original content";
    }

    // Copy file
    fs::copy_file(source, dest, fs::copy_options::overwrite_existing);
    std::cout << "Copied file: " << source << " -> " << dest << "\n";

    // Rename/move file
    fs::path renamed = "renamed.txt";
    fs::rename(dest, renamed);
    std::cout << "Renamed file: " << dest << " -> " << renamed << "\n";

    // File size
    std::cout << "File size: " << fs::file_size(renamed) << " bytes\n";

    // Remove file
    fs::remove(source);
    fs::remove(renamed);
    std::cout << "Files removed\n";
}

// ==============================================
// 8. Permissions
// ==============================================

void permissionsDemo() {
    std::cout << "\n=== 8. Permissions ===\n";

    fs::path testFile = "permissions_test.txt";
    {
        std::ofstream out(testFile);
        out << "Test";
    }

    // Get current permissions
    auto perms = fs::status(testFile).permissions();

    std::cout << "File permissions: ";
    std::cout << ((perms & fs::perms::owner_read) != fs::perms::none ? "r" : "-");
    std::cout << ((perms & fs::perms::owner_write) != fs::perms::none ? "w" : "-");
    std::cout << ((perms & fs::perms::owner_exec) != fs::perms::none ? "x" : "-");
    std::cout << "\n";

    // Modify permissions (Unix-like systems)
    try {
        fs::permissions(testFile,
                       fs::perms::owner_read | fs::perms::owner_write,
                       fs::perm_options::replace);
        std::cout << "Permissions modified\n";
    } catch (const fs::filesystem_error& e) {
        std::cout << "Permission modification not supported or failed\n";
    }

    // Cleanup
    fs::remove(testFile);
}

// ==============================================
// 9. Space Information
// ==============================================

void spaceInfoDemo() {
    std::cout << "\n=== 9. Space Information ===\n";

    try {
        fs::space_info info = fs::space(fs::current_path());

        std::cout << "Filesystem space:\n";
        std::cout << "  Capacity: " << (info.capacity / 1024 / 1024 / 1024) << " GB\n";
        std::cout << "  Free: " << (info.free / 1024 / 1024 / 1024) << " GB\n";
        std::cout << "  Available: " << (info.available / 1024 / 1024 / 1024) << " GB\n";
    } catch (const fs::filesystem_error& e) {
        std::cout << "Could not get space info: " << e.what() << "\n";
    }
}

// ==============================================
// 10. Error Handling
// ==============================================

void errorHandlingDemo() {
    std::cout << "\n=== 10. Error Handling ===\n";

    // Method 1: Exception-based
    try {
        fs::remove("nonexistent_file.txt");
    } catch (const fs::filesystem_error& e) {
        std::cout << "Exception: " << e.what() << "\n";
        std::cout << "  path1: " << e.path1() << "\n";
    }

    // Method 2: Error code-based
    std::error_code ec;
    fs::remove("nonexistent_file.txt", ec);
    if (ec) {
        std::cout << "Error code: " << ec.message() << "\n";
    } else {
        std::cout << "Success (no error)\n";
    }
}

// ==============================================
// 11. Practical Example: Find Files
// ==============================================

std::vector<fs::path> findFiles(const fs::path& root,
                                 const std::string& extension) {
    std::vector<fs::path> result;

    if (!fs::exists(root) || !fs::is_directory(root)) {
        return result;
    }

    for (const auto& entry : fs::recursive_directory_iterator(root)) {
        if (entry.is_regular_file() && entry.path().extension() == extension) {
            result.push_back(entry.path());
        }
    }

    return result;
}

void findFilesDemo() {
    std::cout << "\n=== 11. Find Files Example ===\n";

    // Create test structure
    fs::path testDir = "find_test";
    fs::create_directories(testDir / "subdir");

    std::ofstream(testDir / "file1.txt") << "1";
    std::ofstream(testDir / "file2.cpp") << "2";
    std::ofstream(testDir / "file3.txt") << "3";
    std::ofstream(testDir / "subdir" / "file4.txt") << "4";
    std::ofstream(testDir / "subdir" / "file5.cpp") << "5";

    // Find all .txt files
    auto txtFiles = findFiles(testDir, ".txt");

    std::cout << "Found " << txtFiles.size() << " .txt files:\n";
    for (const auto& file : txtFiles) {
        std::cout << "  " << file << "\n";
    }

    // Cleanup
    fs::remove_all(testDir);
}

// ==============================================
// 12. Practical Example: Directory Size
// ==============================================

std::uintmax_t calculateDirSize(const fs::path& directory) {
    std::uintmax_t size = 0;

    if (!fs::exists(directory) || !fs::is_directory(directory)) {
        return size;
    }

    for (const auto& entry : fs::recursive_directory_iterator(directory)) {
        if (entry.is_regular_file()) {
            std::error_code ec;
            size += fs::file_size(entry.path(), ec);
        }
    }

    return size;
}

void directorySizeDemo() {
    std::cout << "\n=== 12. Directory Size Example ===\n";

    // Create test directory
    fs::path testDir = "size_test";
    fs::create_directory(testDir);

    // Create files of known sizes
    {
        std::ofstream f1(testDir / "file1.txt");
        f1 << std::string(1024, 'A'); // 1 KB
    }
    {
        std::ofstream f2(testDir / "file2.txt");
        f2 << std::string(2048, 'B'); // 2 KB
    }

    std::uintmax_t size = calculateDirSize(testDir);
    std::cout << "Directory size: " << size << " bytes ("
              << (size / 1024) << " KB)\n";

    // Cleanup
    fs::remove_all(testDir);
}

// ==============================================
// 13. Temporary Directories
// ==============================================

void temporaryDirDemo() {
    std::cout << "\n=== 13. Temporary Directory ===\n";

    // Get temp directory path
    fs::path tempDir = fs::temp_directory_path();
    std::cout << "System temp directory: " << tempDir << "\n";

    // Create unique temp subdirectory
    fs::path uniqueTemp = tempDir / "myapp_XXXXXX";
    // Note: C++17 doesn't have create_temp_directory, you'd need to implement it
    std::cout << "Would create temp directory in: " << tempDir << "\n";
}

int main() {
    std::cout << "=== C++17 std::filesystem ===\n";

    // 1. Path basics
    pathBasicsDemo();

    // 2. Path manipulation
    pathManipulationDemo();

    // 3. Path queries
    pathQueriesDemo();

    // 4. Filesystem status
    filesystemStatusDemo();

    // 5. Directory operations
    directoryOperationsDemo();

    // 6. Directory iteration
    directoryIterationDemo();

    // 7. File operations
    fileOperationsDemo();

    // 8. Permissions
    permissionsDemo();

    // 9. Space info
    spaceInfoDemo();

    // 10. Error handling
    errorHandlingDemo();

    // 11. Find files
    findFilesDemo();

    // 12. Directory size
    directorySizeDemo();

    // 13. Temporary directory
    temporaryDirDemo();

    std::cout << "\n=== Key Takeaways ===\n";
    std::cout << "1. std::filesystem provides portable file operations (C++17)\n";
    std::cout << "2. fs::path handles platform-specific path separators\n";
    std::cout << "3. directory_iterator for listing directory contents\n";
    std::cout << "4. recursive_directory_iterator for tree traversal\n";
    std::cout << "5. Rich set of file operations: copy, move, remove, etc.\n";
    std::cout << "6. Query file status, size, permissions, timestamps\n";
    std::cout << "7. Error handling via exceptions or error codes\n";

    return 0;
}
