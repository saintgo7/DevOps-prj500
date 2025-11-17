# Program 200: Build Systems

## Description
Explores modern build systems for C++ projects, including CMake, Make, and build system best practices for scalable project organization.

## Learning Objectives
- Use CMake for cross-platform builds
- Write effective CMakeLists.txt files
- Manage dependencies
- Configure build types (Debug, Release)
- Organize multi-target projects

## Features
- CMake basics and advanced features
- Make and Makefiles
- Dependency management
- Build configuration
- Install targets
- Package generation

## Compilation
```bash
cd /home/user/DevOps-prj500/101-200_CPP/200_build_systems
mkdir -p build && cd build
cmake ..
make
./build_systems
```

## Key Concepts
```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 3.10)
project(MyProject)

set(CMAKE_CXX_STANDARD 17)

add_executable(myapp main.cpp)
target_link_libraries(myapp pthread)

# Build types
cmake -DCMAKE_BUILD_TYPE=Release ..

# Install
install(TARGETS myapp DESTINATION bin)
```

## Best Practices
1. Use CMake for new projects
2. Organize code into libraries
3. Set CMAKE_CXX_STANDARD explicitly
4. Use target-based commands
5. Support out-of-source builds
6. Document build requirements

## Navigation
- **Previous**: [199 - Debugging Tools](/home/user/DevOps-prj500/101-200_CPP/199_debugging_tools/README.md)
- **Back to Main Index**: [README](/home/user/DevOps-prj500/README.md)
