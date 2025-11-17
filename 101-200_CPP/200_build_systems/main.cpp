/*
 * Program 200: Build Systems
 * Demonstrates CMake, Make, and build configuration concepts
 * This file includes examples and documentation for build systems
 */

#include <iostream>
#include <string>

void demonstrateMakefile() {
    std::cout << "\n=== Makefile ===" << std::endl;

    std::cout << "\nBasic Makefile structure:" << std::endl;
    std::cout << "# Makefile" << std::endl;
    std::cout << "CXX = g++" << std::endl;
    std::cout << "CXXFLAGS = -std=c++17 -Wall -O2" << std::endl;
    std::cout << "TARGET = program" << std::endl;
    std::cout << "" << std::endl;
    std::cout << "$(TARGET): main.o utils.o" << std::endl;
    std::cout << "\t$(CXX) $(CXXFLAGS) -o $(TARGET) main.o utils.o" << std::endl;
    std::cout << "" << std::endl;
    std::cout << "main.o: main.cpp" << std::endl;
    std::cout << "\t$(CXX) $(CXXFLAGS) -c main.cpp" << std::endl;
    std::cout << "" << std::endl;
    std::cout << "utils.o: utils.cpp utils.h" << std::endl;
    std::cout << "\t$(CXX) $(CXXFLAGS) -c utils.cpp" << std::endl;
    std::cout << "" << std::endl;
    std::cout << "clean:" << std::endl;
    std::cout << "\trm -f *.o $(TARGET)" << std::endl;

    std::cout << "\nUsage:" << std::endl;
    std::cout << "  make           # Build project" << std::endl;
    std::cout << "  make clean     # Remove build artifacts" << std::endl;
    std::cout << "  make -j4       # Parallel build with 4 jobs" << std::endl;
}

void demonstrateCMake() {
    std::cout << "\n=== CMake ===" << std::endl;

    std::cout << "\nMinimal CMakeLists.txt:" << std::endl;
    std::cout << "cmake_minimum_required(VERSION 3.10)" << std::endl;
    std::cout << "project(MyProject VERSION 1.0)" << std::endl;
    std::cout << "" << std::endl;
    std::cout << "set(CMAKE_CXX_STANDARD 17)" << std::endl;
    std::cout << "set(CMAKE_CXX_STANDARD_REQUIRED True)" << std::endl;
    std::cout << "" << std::endl;
    std::cout << "add_executable(program main.cpp utils.cpp)" << std::endl;

    std::cout << "\nBuilding with CMake:" << std::endl;
    std::cout << "  mkdir build && cd build" << std::endl;
    std::cout << "  cmake .." << std::endl;
    std::cout << "  cmake --build ." << std::endl;
    std::cout << "  # Or: make -j4" << std::endl;

    std::cout << "\nAdvanced CMakeLists.txt:" << std::endl;
    std::cout << "cmake_minimum_required(VERSION 3.10)" << std::endl;
    std::cout << "project(AdvancedProject VERSION 1.0 LANGUAGES CXX)" << std::endl;
    std::cout << "" << std::endl;
    std::cout << "# C++ standard" << std::endl;
    std::cout << "set(CMAKE_CXX_STANDARD 17)" << std::endl;
    std::cout << "set(CMAKE_CXX_STANDARD_REQUIRED True)" << std::endl;
    std::cout << "" << std::endl;
    std::cout << "# Build type" << std::endl;
    std::cout << "if(NOT CMAKE_BUILD_TYPE)" << std::endl;
    std::cout << "  set(CMAKE_BUILD_TYPE Release)" << std::endl;
    std::cout << "endif()" << std::endl;
    std::cout << "" << std::endl;
    std::cout << "# Compiler flags" << std::endl;
    std::cout << "set(CMAKE_CXX_FLAGS_DEBUG \"-g -O0\")" << std::endl;
    std::cout << "set(CMAKE_CXX_FLAGS_RELEASE \"-O3 -DNDEBUG\")" << std::endl;
    std::cout << "" << std::endl;
    std::cout << "# Source files" << std::endl;
    std::cout << "file(GLOB SOURCES \"src/*.cpp\")" << std::endl;
    std::cout << "" << std::endl;
    std::cout << "# Executable" << std::endl;
    std::cout << "add_executable(program ${SOURCES})" << std::endl;
    std::cout << "" << std::endl;
    std::cout << "# Include directories" << std::endl;
    std::cout << "target_include_directories(program PRIVATE include)" << std::endl;
    std::cout << "" << std::endl;
    std::cout << "# Link libraries" << std::endl;
    std::cout << "target_link_libraries(program pthread)" << std::endl;

    std::cout << "\nCMake build types:" << std::endl;
    std::cout << "  cmake -DCMAKE_BUILD_TYPE=Debug .." << std::endl;
    std::cout << "  cmake -DCMAKE_BUILD_TYPE=Release .." << std::endl;
    std::cout << "  cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo .." << std::endl;
    std::cout << "  cmake -DCMAKE_BUILD_TYPE=MinSizeRel .." << std::endl;
}

void demonstrateCMakeLibraries() {
    std::cout << "\n=== CMake with Libraries ===" << std::endl;

    std::cout << "\nCreating a library:" << std::endl;
    std::cout << "# Static library" << std::endl;
    std::cout << "add_library(mylib STATIC utils.cpp)" << std::endl;
    std::cout << "" << std::endl;
    std::cout << "# Shared library" << std::endl;
    std::cout << "add_library(mylib SHARED utils.cpp)" << std::endl;
    std::cout << "" << std::endl;
    std::cout << "# Header-only library" << std::endl;
    std::cout << "add_library(mylib INTERFACE)" << std::endl;
    std::cout << "target_include_directories(mylib INTERFACE include/)" << std::endl;

    std::cout << "\nUsing the library:" << std::endl;
    std::cout << "add_executable(program main.cpp)" << std::endl;
    std::cout << "target_link_libraries(program mylib)" << std::endl;

    std::cout << "\nFinding external libraries:" << std::endl;
    std::cout << "# Find Threads" << std::endl;
    std::cout << "find_package(Threads REQUIRED)" << std::endl;
    std::cout << "target_link_libraries(program Threads::Threads)" << std::endl;
    std::cout << "" << std::endl;
    std::cout << "# Find Boost" << std::endl;
    std::cout << "find_package(Boost 1.70 REQUIRED COMPONENTS filesystem)" << std::endl;
    std::cout << "target_link_libraries(program Boost::filesystem)" << std::endl;
}

void demonstrateCMakeOptions() {
    std::cout << "\n=== CMake Options and Configuration ===" << std::endl;

    std::cout << "\nDefining options:" << std::endl;
    std::cout << "option(BUILD_TESTS \"Build test programs\" ON)" << std::endl;
    std::cout << "option(ENABLE_LOGGING \"Enable logging\" OFF)" << std::endl;
    std::cout << "" << std::endl;
    std::cout << "if(BUILD_TESTS)" << std::endl;
    std::cout << "  add_subdirectory(tests)" << std::endl;
    std::cout << "endif()" << std::endl;
    std::cout << "" << std::endl;
    std::cout << "if(ENABLE_LOGGING)" << std::endl;
    std::cout << "  target_compile_definitions(program PRIVATE LOGGING_ENABLED)" << std::endl;
    std::cout << "endif()" << std::endl;

    std::cout << "\nUsing options:" << std::endl;
    std::cout << "  cmake -DBUILD_TESTS=OFF .." << std::endl;
    std::cout << "  cmake -DENABLE_LOGGING=ON .." << std::endl;

    std::cout << "\nConfiguration file:" << std::endl;
    std::cout << "# config.h.in" << std::endl;
    std::cout << "#define PROJECT_VERSION \"@PROJECT_VERSION@\"" << std::endl;
    std::cout << "#cmakedefine ENABLE_LOGGING" << std::endl;
    std::cout << "" << std::endl;
    std::cout << "# CMakeLists.txt" << std::endl;
    std::cout << "configure_file(config.h.in config.h)" << std::endl;
}

void demonstrateBuildTypes() {
    std::cout << "\n=== Build Types and Configurations ===" << std::endl;

    std::cout << "\n1. Debug:" << std::endl;
    std::cout << "   - No optimization (-O0)" << std::endl;
    std::cout << "   - Debug symbols (-g)" << std::endl;
    std::cout << "   - Assertions enabled" << std::endl;
    std::cout << "   - Slower, but debuggable" << std::endl;

    std::cout << "\n2. Release:" << std::endl;
    std::cout << "   - Full optimization (-O3)" << std::endl;
    std::cout << "   - No debug symbols" << std::endl;
    std::cout << "   - Assertions disabled (-DNDEBUG)" << std::endl;
    std::cout << "   - Fastest execution" << std::endl;

    std::cout << "\n3. RelWithDebInfo:" << std::endl;
    std::cout << "   - Optimized (-O2)" << std::endl;
    std::cout << "   - With debug symbols (-g)" << std::endl;
    std::cout << "   - Good compromise for profiling" << std::endl;

    std::cout << "\n4. MinSizeRel:" << std::endl;
    std::cout << "   - Optimize for size (-Os)" << std::endl;
    std::cout << "   - No debug symbols" << std::endl;
    std::cout << "   - For embedded systems" << std::endl;
}

void demonstrateModernCMake() {
    std::cout << "\n=== Modern CMake Best Practices ===" << std::endl;

    std::cout << "\n1. Target-based approach:" << std::endl;
    std::cout << "# Bad (global)" << std::endl;
    std::cout << "include_directories(include/)" << std::endl;
    std::cout << "link_libraries(pthread)" << std::endl;
    std::cout << "" << std::endl;
    std::cout << "# Good (target-specific)" << std::endl;
    std::cout << "target_include_directories(myapp PRIVATE include/)" << std::endl;
    std::cout << "target_link_libraries(myapp PRIVATE pthread)" << std::endl;

    std::cout << "\n2. Use PRIVATE/PUBLIC/INTERFACE:" << std::endl;
    std::cout << "# PRIVATE: Only this target uses it" << std::endl;
    std::cout << "# PUBLIC: This target and dependents use it" << std::endl;
    std::cout << "# INTERFACE: Only dependents use it" << std::endl;

    std::cout << "\n3. Generator expressions:" << std::endl;
    std::cout << "target_compile_options(myapp PRIVATE" << std::endl;
    std::cout << "  $<$<CONFIG:Debug>:-g -O0>" << std::endl;
    std::cout << "  $<$<CONFIG:Release>:-O3>" << std::endl;
    std::cout << ")" << std::endl;

    std::cout << "\n4. Export and install:" << std::endl;
    std::cout << "install(TARGETS mylib" << std::endl;
    std::cout << "  EXPORT mylibTargets" << std::endl;
    std::cout << "  LIBRARY DESTINATION lib" << std::endl;
    std::cout << "  ARCHIVE DESTINATION lib" << std::endl;
    std::cout << "  INCLUDES DESTINATION include" << std::endl;
    std::cout << ")" << std::endl;
}

void demonstrateOtherBuildSystems() {
    std::cout << "\n=== Other Build Systems ===" << std::endl;

    std::cout << "\n1. Ninja:" << std::endl;
    std::cout << "   - Faster than Make" << std::endl;
    std::cout << "   - Use with CMake: cmake -G Ninja .." << std::endl;
    std::cout << "   - Build: ninja" << std::endl;

    std::cout << "\n2. Bazel:" << std::endl;
    std::cout << "   - Google's build system" << std::endl;
    std::cout << "   - Excellent for large projects" << std::endl;
    std::cout << "   - Hermetic builds" << std::endl;
    std::cout << "   - BUILD file instead of CMakeLists.txt" << std::endl;

    std::cout << "\n3. Meson:" << std::endl;
    std::cout << "   - Fast and user-friendly" << std::endl;
    std::cout << "   - Python-based" << std::endl;
    std::cout << "   - meson.build configuration" << std::endl;
    std::cout << "   - Uses Ninja as backend" << std::endl;

    std::cout << "\n4. SCons:" << std::endl;
    std::cout << "   - Python-based" << std::endl;
    std::cout << "   - SConstruct files" << std::endl;
    std::cout << "   - Used by MongoDB" << std::endl;

    std::cout << "\n5. Premake:" << std::endl;
    std::cout << "   - Generates project files" << std::endl;
    std::cout << "   - For Visual Studio, Xcode, Makefile" << std::endl;
    std::cout << "   - Lua-based configuration" << std::endl;
}

void demonstratePackageManagers() {
    std::cout << "\n=== Package Managers ===" << std::endl;

    std::cout << "\n1. vcpkg (Microsoft):" << std::endl;
    std::cout << "   vcpkg install boost" << std::endl;
    std::cout << "   cmake -DCMAKE_TOOLCHAIN_FILE=vcpkg.cmake .." << std::endl;

    std::cout << "\n2. Conan:" << std::endl;
    std::cout << "   # conanfile.txt" << std::endl;
    std::cout << "   [requires]" << std::endl;
    std::cout << "   boost/1.76.0" << std::endl;
    std::cout << "   " << std::endl;
    std::cout << "   conan install ." << std::endl;
    std::cout << "   cmake -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake .." << std::endl;

    std::cout << "\n3. CPM (CMake Package Manager):" << std::endl;
    std::cout << "   CPMAddPackage(\"gh:fmtlib/fmt#9.1.0\")" << std::endl;
    std::cout << "   target_link_libraries(myapp fmt::fmt)" << std::endl;

    std::cout << "\n4. Hunter:" << std::endl;
    std::cout << "   Hunter CMake integration" << std::endl;
    std::cout << "   hunter_add_package(Boost)" << std::endl;
}

void demonstrateContinuousIntegration() {
    std::cout << "\n=== Continuous Integration ===" << std::endl;

    std::cout << "\nGitHub Actions example (.github/workflows/build.yml):" << std::endl;
    std::cout << "name: Build" << std::endl;
    std::cout << "on: [push, pull_request]" << std::endl;
    std::cout << "" << std::endl;
    std::cout << "jobs:" << std::endl;
    std::cout << "  build:" << std::endl;
    std::cout << "    runs-on: ubuntu-latest" << std::endl;
    std::cout << "    steps:" << std::endl;
    std::cout << "    - uses: actions/checkout@v2" << std::endl;
    std::cout << "    - name: Configure" << std::endl;
    std::cout << "      run: cmake -B build -DCMAKE_BUILD_TYPE=Release" << std::endl;
    std::cout << "    - name: Build" << std::endl;
    std::cout << "      run: cmake --build build --parallel" << std::endl;
    std::cout << "    - name: Test" << std::endl;
    std::cout << "      run: cd build && ctest --output-on-failure" << std::endl;
}

void demonstrateBestPractices() {
    std::cout << "\n=== Build System Best Practices ===" << std::endl;

    std::cout << "\n1. Out-of-source builds:" << std::endl;
    std::cout << "   mkdir build && cd build && cmake .." << std::endl;
    std::cout << "   Keeps source tree clean" << std::endl;

    std::cout << "\n2. Use version control for build files:" << std::endl;
    std::cout << "   Commit: CMakeLists.txt, Makefile" << std::endl;
    std::cout << "   .gitignore: build/, *.o, executables" << std::endl;

    std::cout << "\n3. Make builds reproducible:" << std::endl;
    std::cout << "   - Pin dependency versions" << std::endl;
    std::cout << "   - Document build requirements" << std::endl;
    std::cout << "   - Use toolchain files" << std::endl;

    std::cout << "\n4. Parallel builds:" << std::endl;
    std::cout << "   make -j$(nproc)" << std::endl;
    std::cout << "   cmake --build . --parallel" << std::endl;

    std::cout << "\n5. Separate debug and release builds:" << std::endl;
    std::cout << "   mkdir build-debug build-release" << std::endl;
    std::cout << "   cd build-debug && cmake -DCMAKE_BUILD_TYPE=Debug .." << std::endl;
    std::cout << "   cd build-release && cmake -DCMAKE_BUILD_TYPE=Release .." << std::endl;

    std::cout << "\n6. Testing integration:" << std::endl;
    std::cout << "   enable_testing()" << std::endl;
    std::cout << "   add_test(NAME test1 COMMAND test_program)" << std::endl;
    std::cout << "   Run: ctest or make test" << std::endl;

    std::cout << "\n7. Installation:" << std::endl;
    std::cout << "   install(TARGETS program DESTINATION bin)" << std::endl;
    std::cout << "   Run: make install or cmake --install ." << std::endl;
}

void demonstrateProjectStructure() {
    std::cout << "\n=== Recommended Project Structure ===" << std::endl;

    std::cout << "\nTypical C++ project layout:" << std::endl;
    std::cout << "project/" << std::endl;
    std::cout << "├── CMakeLists.txt          # Main build file" << std::endl;
    std::cout << "├── README.md               # Project documentation" << std::endl;
    std::cout << "├── .gitignore              # Git ignore file" << std::endl;
    std::cout << "├── include/                # Public headers" << std::endl;
    std::cout << "│   └── mylib/              # Library namespace" << std::endl;
    std::cout << "│       └── mylib.h" << std::endl;
    std::cout << "├── src/                    # Source files" << std::endl;
    std::cout << "│   ├── CMakeLists.txt" << std::endl;
    std::cout << "│   ├── main.cpp" << std::endl;
    std::cout << "│   └── mylib.cpp" << std::endl;
    std::cout << "├── tests/                  # Test files" << std::endl;
    std::cout << "│   ├── CMakeLists.txt" << std::endl;
    std::cout << "│   └── test_mylib.cpp" << std::endl;
    std::cout << "├── third_party/            # External dependencies" << std::endl;
    std::cout << "├── docs/                   # Documentation" << std::endl;
    std::cout << "├── scripts/                # Build scripts" << std::endl;
    std::cout << "└── build/                  # Build directory (not in git)" << std::endl;
}

int main() {
    std::cout << "Build Systems Demonstration" << std::endl;
    std::cout << "============================" << std::endl;

    std::cout << "\nThis program demonstrates build system concepts." << std::endl;
    std::cout << "Actual build files would be created separately." << std::endl;

    demonstrateProjectStructure();
    demonstrateMakefile();
    demonstrateCMake();
    demonstrateCMakeLibraries();
    demonstrateCMakeOptions();
    demonstrateBuildTypes();
    demonstrateModernCMake();
    demonstrateOtherBuildSystems();
    demonstratePackageManagers();
    demonstrateContinuousIntegration();
    demonstrateBestPractices();

    std::cout << "\n=== Build Systems Complete ===" << std::endl;
    std::cout << "\nQuick start with CMake:" << std::endl;
    std::cout << "  1. Create CMakeLists.txt" << std::endl;
    std::cout << "  2. mkdir build && cd build" << std::endl;
    std::cout << "  3. cmake -DCMAKE_BUILD_TYPE=Release .." << std::endl;
    std::cout << "  4. cmake --build . --parallel" << std::endl;

    std::cout << "\nRecommendation: Use CMake for modern C++ projects!" << std::endl;

    return 0;
}
