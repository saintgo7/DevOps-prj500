# Program 179: Filesystem

## Description
Demonstrates the std::filesystem library (C++17) for portable file and directory manipulation, providing a modern alternative to platform-specific file operations.

## Learning Objectives
- Navigate directories with filesystem
- Check file/directory existence
- Create, copy, and delete files/directories
- Query file attributes
- Iterate through directory contents
- Work with paths portably

## Features
- Path operations
- Directory iteration
- File operations (create, remove, copy)
- File status queries
- File size and permissions
- Recursive directory operations

## Compilation
```bash
g++ -std=c++17 main.cpp -o filesystem -lstdc++fs
./filesystem
```

## Key Concepts
```cpp
namespace fs = std::filesystem;

fs::path p = "/home/user/file.txt";
if (fs::exists(p)) {
    cout << "Size: " << fs::file_size(p);
}

for (auto& entry : fs::directory_iterator("/path")) {
    cout << entry.path();
}

fs::create_directories("/path/to/dir");
fs::copy("src.txt", "dst.txt");
```

## Best Practices
1. Use filesystem for portable code
2. Check exists() before operations
3. Handle filesystem errors with try-catch
4. Use portable path separators
5. Be careful with recursive operations

## Navigation
- **Previous**: [178 - Span](/home/user/DevOps-prj500/101-200_CPP/178_span/README.md)
- **Next**: [180 - Chrono](/home/user/DevOps-prj500/101-200_CPP/180_chrono/README.md)
