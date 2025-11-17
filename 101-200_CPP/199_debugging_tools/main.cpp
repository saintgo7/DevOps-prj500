/*
 * Program 199: Debugging Tools
 * Demonstrates gdb, valgrind, sanitizers, and debugging techniques
 * Compile for debugging: g++ -std=c++17 -g -O0 -o debugging_tools main.cpp
 * Compile with sanitizers: g++ -std=c++17 -g -fsanitize=address -o debugging_tools main.cpp
 */

#include <iostream>
#include <vector>
#include <string>
#include <memory>
#include <cstring>

void demonstrateGDB() {
    std::cout << "\n=== GDB (GNU Debugger) ===" << std::endl;

    std::cout << "\nBasic GDB commands:" << std::endl;
    std::cout << "  gdb ./program              Start GDB" << std::endl;
    std::cout << "  run [args]                 Run program" << std::endl;
    std::cout << "  break main                 Set breakpoint at main" << std::endl;
    std::cout << "  break file.cpp:42          Set breakpoint at line" << std::endl;
    std::cout << "  break function_name        Set breakpoint at function" << std::endl;

    std::cout << "\nStepping through code:" << std::endl;
    std::cout << "  step (s)                   Step into functions" << std::endl;
    std::cout << "  next (n)                   Step over functions" << std::endl;
    std::cout << "  continue (c)               Continue to next breakpoint" << std::endl;
    std::cout << "  finish                     Run until function returns" << std::endl;

    std::cout << "\nInspecting variables:" << std::endl;
    std::cout << "  print variable             Print variable value" << std::endl;
    std::cout << "  print *pointer             Dereference pointer" << std::endl;
    std::cout << "  print array[5]             Print array element" << std::endl;
    std::cout << "  display variable           Auto-print on each step" << std::endl;
    std::cout << "  info locals                Show local variables" << std::endl;

    std::cout << "\nStack inspection:" << std::endl;
    std::cout << "  backtrace (bt)             Show call stack" << std::endl;
    std::cout << "  frame 2                    Switch to frame 2" << std::endl;
    std::cout << "  up/down                    Move up/down stack" << std::endl;

    std::cout << "\nAdvanced features:" << std::endl;
    std::cout << "  watch variable             Break when variable changes" << std::endl;
    std::cout << "  condition 1 x > 10         Conditional breakpoint" << std::endl;
    std::cout << "  info breakpoints           List all breakpoints" << std::endl;
    std::cout << "  delete 1                   Delete breakpoint 1" << std::endl;

    std::cout << "\nCore dump analysis:" << std::endl;
    std::cout << "  ulimit -c unlimited        Enable core dumps" << std::endl;
    std::cout << "  gdb ./program core         Debug core dump" << std::endl;
}

void demonstrateValgrind() {
    std::cout << "\n=== Valgrind ===" << std::endl;

    std::cout << "\n1. Memcheck (Memory Debugger):" << std::endl;
    std::cout << "   valgrind --leak-check=full ./program" << std::endl;
    std::cout << "   Detects:" << std::endl;
    std::cout << "     - Memory leaks" << std::endl;
    std::cout << "     - Invalid memory access" << std::endl;
    std::cout << "     - Use of uninitialized memory" << std::endl;
    std::cout << "     - Double free" << std::endl;

    std::cout << "\n2. Cachegrind (Cache Profiler):" << std::endl;
    std::cout << "   valgrind --tool=cachegrind ./program" << std::endl;
    std::cout << "   cg_annotate cachegrind.out.*" << std::endl;
    std::cout << "   Analyzes:" << std::endl;
    std::cout << "     - Cache misses" << std::endl;
    std::cout << "     - Branch mispredictions" << std::endl;

    std::cout << "\n3. Callgrind (Call Graph Profiler):" << std::endl;
    std::cout << "   valgrind --tool=callgrind ./program" << std::endl;
    std::cout << "   kcachegrind callgrind.out.*" << std::endl;
    std::cout << "   Provides:" << std::endl;
    std::cout << "     - Function call graph" << std::endl;
    std::cout << "     - Time spent per function" << std::endl;

    std::cout << "\n4. Massif (Heap Profiler):" << std::endl;
    std::cout << "   valgrind --tool=massif ./program" << std::endl;
    std::cout << "   ms_print massif.out.*" << std::endl;
    std::cout << "   Tracks:" << std::endl;
    std::cout << "     - Heap memory usage over time" << std::endl;
    std::cout << "     - Memory allocation sources" << std::endl;

    std::cout << "\n5. Helgrind (Thread Debugger):" << std::endl;
    std::cout << "   valgrind --tool=helgrind ./program" << std::endl;
    std::cout << "   Detects:" << std::endl;
    std::cout << "     - Data races" << std::endl;
    std::cout << "     - Deadlocks" << std::endl;
    std::cout << "     - Lock order violations" << std::endl;
}

void demonstrateSanitizers() {
    std::cout << "\n=== Sanitizers (Compile-Time Instrumentation) ===" << std::endl;

    std::cout << "\n1. AddressSanitizer (ASan):" << std::endl;
    std::cout << "   Compile: g++ -fsanitize=address -g main.cpp" << std::endl;
    std::cout << "   Detects:" << std::endl;
    std::cout << "     - Heap buffer overflow" << std::endl;
    std::cout << "     - Stack buffer overflow" << std::endl;
    std::cout << "     - Use after free" << std::endl;
    std::cout << "     - Use after return" << std::endl;
    std::cout << "     - Double free" << std::endl;
    std::cout << "     - Memory leaks (with ASAN_OPTIONS=detect_leaks=1)" << std::endl;

    std::cout << "\n2. ThreadSanitizer (TSan):" << std::endl;
    std::cout << "   Compile: g++ -fsanitize=thread -g main.cpp" << std::endl;
    std::cout << "   Detects:" << std::endl;
    std::cout << "     - Data races" << std::endl;
    std::cout << "     - Thread synchronization issues" << std::endl;

    std::cout << "\n3. UndefinedBehaviorSanitizer (UBSan):" << std::endl;
    std::cout << "   Compile: g++ -fsanitize=undefined -g main.cpp" << std::endl;
    std::cout << "   Detects:" << std::endl;
    std::cout << "     - Signed integer overflow" << std::endl;
    std::cout << "     - Division by zero" << std::endl;
    std::cout << "     - Null pointer dereference" << std::endl;
    std::cout << "     - Array bounds" << std::endl;

    std::cout << "\n4. MemorySanitizer (MSan):" << std::endl;
    std::cout << "   Compile: clang++ -fsanitize=memory -g main.cpp" << std::endl;
    std::cout << "   Detects:" << std::endl;
    std::cout << "     - Uninitialized memory reads" << std::endl;

    std::cout << "\nNote: Cannot combine ASan with TSan or MSan" << std::endl;
}

// Intentional bugs for demonstration
void demonstrateMemoryLeaks() {
    std::cout << "\n=== Memory Leak Example ===" << std::endl;

    std::cout << "Creating intentional memory leak..." << std::endl;

    // Memory leak - never deleted
    int* leaked = new int[100];
    leaked[0] = 42;

    std::cout << "Leak created (100 ints not freed)" << std::endl;
    std::cout << "Run with valgrind to detect: valgrind --leak-check=full ./program" << std::endl;

    // Clean up (comment out to see leak)
    delete[] leaked;
    std::cout << "Memory freed (no leak)" << std::endl;
}

void demonstrateBufferOverflow() {
    std::cout << "\n=== Buffer Overflow Example ===" << std::endl;

    std::cout << "This demonstrates buffer overflow (safely)..." << std::endl;

    // Safe version
    int safe_array[10];
    for (int i = 0; i < 10; ++i) {
        safe_array[i] = i;
    }
    std::cout << "Safe access: array[9] = " << safe_array[9] << std::endl;

    // Unsafe version (commented out to prevent crash)
    // int unsafe_array[10];
    // unsafe_array[100] = 42;  // Buffer overflow!

    std::cout << "Buffer overflow would write past array bounds" << std::endl;
    std::cout << "Compile with -fsanitize=address to detect" << std::endl;
}

void demonstrateUseAfterFree() {
    std::cout << "\n=== Use After Free Example ===" << std::endl;

    std::cout << "Demonstrating use-after-free (safely)..." << std::endl;

    int* ptr = new int(42);
    std::cout << "Allocated: " << *ptr << std::endl;

    delete ptr;
    std::cout << "Deleted pointer" << std::endl;

    // Don't use after free!
    // std::cout << *ptr << std::endl;  // Use after free!

    std::cout << "Use-after-free would access freed memory" << std::endl;
    std::cout << "Compile with -fsanitize=address to detect" << std::endl;
}

void demonstrateAssertions() {
    std::cout << "\n=== Assertions for Debugging ===" << std::endl;

    std::cout << "\n1. Standard assert:" << std::endl;
    std::cout << "   #include <cassert>" << std::endl;
    std::cout << "   assert(condition);  // Aborts if false" << std::endl;
    std::cout << "   Disabled with -DNDEBUG" << std::endl;

    std::cout << "\n2. Static assertions:" << std::endl;
    std::cout << "   static_assert(sizeof(int) == 4, \"int must be 4 bytes\");" << std::endl;
    std::cout << "   Compile-time check" << std::endl;

    // Example assertion
    int value = 42;
    // assert(value == 42);  // Would pass
    // assert(value == 0);   // Would fail and abort

    std::cout << "\n3. Custom assertions:" << std::endl;
    std::cout << "   #define VERIFY(cond, msg) if (!(cond)) error(msg)" << std::endl;
}

void demonstrateDebuggingMacros() {
    std::cout << "\n=== Debugging Macros ===" << std::endl;

    std::cout << "\nUseful preprocessor macros:" << std::endl;
    std::cout << "  __FILE__     Current file: " << __FILE__ << std::endl;
    std::cout << "  __LINE__     Current line: " << __LINE__ << std::endl;
    std::cout << "  __FUNCTION__ Current func: " << __FUNCTION__ << std::endl;

    std::cout << "\nDebug print macro example:" << std::endl;
    std::cout << "  #ifdef DEBUG" << std::endl;
    std::cout << "  #define DPRINT(x) std::cout << #x << \" = \" << x << std::endl;" << std::endl;
    std::cout << "  #else" << std::endl;
    std::cout << "  #define DPRINT(x)" << std::endl;
    std::cout << "  #endif" << std::endl;
}

void demonstrateLogging() {
    std::cout << "\n=== Logging for Debugging ===" << std::endl;

    std::cout << "\nLog levels:" << std::endl;
    std::cout << "  TRACE   - Detailed execution flow" << std::endl;
    std::cout << "  DEBUG   - Debug information" << std::endl;
    std::cout << "  INFO    - Informational messages" << std::endl;
    std::cout << "  WARNING - Warning messages" << std::endl;
    std::cout << "  ERROR   - Error messages" << std::endl;
    std::cout << "  FATAL   - Fatal errors" << std::endl;

    std::cout << "\nPopular logging libraries:" << std::endl;
    std::cout << "  - spdlog (fast, header-only)" << std::endl;
    std::cout << "  - glog (Google's logging)" << std::endl;
    std::cout << "  - Boost.Log (comprehensive)" << std::endl;
}

void demonstrateDebuggingStrategies() {
    std::cout << "\n=== Debugging Strategies ===" << std::endl;

    std::cout << "\n1. Reproduce the Bug:" << std::endl;
    std::cout << "   - Create minimal test case" << std::endl;
    std::cout << "   - Identify exact conditions" << std::endl;
    std::cout << "   - Document steps to reproduce" << std::endl;

    std::cout << "\n2. Divide and Conquer:" << std::endl;
    std::cout << "   - Binary search through code" << std::endl;
    std::cout << "   - Add print statements" << std::endl;
    std::cout << "   - Use breakpoints strategically" << std::endl;

    std::cout << "\n3. Rubber Duck Debugging:" << std::endl;
    std::cout << "   - Explain code to someone (or something)" << std::endl;
    std::cout << "   - Often reveals the bug" << std::endl;

    std::cout << "\n4. Read Error Messages Carefully:" << std::endl;
    std::cout << "   - Compiler errors" << std::endl;
    std::cout << "   - Runtime errors" << std::endl;
    std::cout << "   - Stack traces" << std::endl;

    std::cout << "\n5. Check Assumptions:" << std::endl;
    std::cout << "   - Print variable values" << std::endl;
    std::cout << "   - Verify preconditions" << std::endl;
    std::cout << "   - Question everything" << std::endl;

    std::cout << "\n6. Version Control:" << std::endl;
    std::cout << "   - git bisect to find breaking commit" << std::endl;
    std::cout << "   - Compare with last working version" << std::endl;

    std::cout << "\n7. Take a Break:" << std::endl;
    std::cout << "   - Fresh perspective helps" << std::endl;
    std::cout << "   - Avoid tunnel vision" << std::endl;
}

void demonstrateCommonBugs() {
    std::cout << "\n=== Common C++ Bugs ===" << std::endl;

    std::cout << "\n1. Uninitialized Variables:" << std::endl;
    std::cout << "   int x;  // Undefined value!" << std::endl;
    std::cout << "   Should be: int x = 0;" << std::endl;

    std::cout << "\n2. Off-by-One Errors:" << std::endl;
    std::cout << "   for (int i = 0; i <= size; ++i)  // Wrong!" << std::endl;
    std::cout << "   Should be: for (int i = 0; i < size; ++i)" << std::endl;

    std::cout << "\n3. Dangling Pointers:" << std::endl;
    std::cout << "   int* p = new int; delete p; *p = 5;  // Use after free!" << std::endl;

    std::cout << "\n4. Memory Leaks:" << std::endl;
    std::cout << "   new without delete" << std::endl;
    std::cout << "   Use smart pointers instead" << std::endl;

    std::cout << "\n5. Integer Overflow:" << std::endl;
    std::cout << "   int x = INT_MAX; x++; // Undefined behavior!" << std::endl;

    std::cout << "\n6. Race Conditions:" << std::endl;
    std::cout << "   Multiple threads accessing shared data" << std::endl;
    std::cout << "   Use mutexes or atomic operations" << std::endl;

    std::cout << "\n7. Iterator Invalidation:" << std::endl;
    std::cout << "   Modifying container while iterating" << std::endl;

    std::cout << "\n8. Comparing Floats with ==" << std::endl;
    std::cout << "   Use epsilon comparison instead" << std::endl;
}

void demonstrateToolComparison() {
    std::cout << "\n=== Debugging Tools Comparison ===" << std::endl;

    std::cout << "\n                  GDB    Valgrind  Sanitizers" << std::endl;
    std::cout << "Runtime Debug:    Yes    No        No" << std::endl;
    std::cout << "Memory Leaks:     No     Yes       Yes (ASan)" << std::endl;
    std::cout << "Performance:      Fast   Slow      Medium" << std::endl;
    std::cout << "Compile-time:     No     No        Yes" << std::endl;
    std::cout << "Threading:        Yes    Yes       Yes (TSan)" << std::endl;
    std::cout << "Profiling:        No     Yes       No" << std::endl;

    std::cout << "\nWhen to use what:" << std::endl;
    std::cout << "  - Crash debugging: GDB" << std::endl;
    std::cout << "  - Memory leaks: Valgrind or ASan" << std::endl;
    std::cout << "  - Performance profiling: Valgrind (callgrind)" << std::endl;
    std::cout << "  - Development: Sanitizers (fast feedback)" << std::endl;
    std::cout << "  - Production testing: Valgrind (comprehensive)" << std::endl;
}

void demonstrateBestPractices() {
    std::cout << "\n=== Debugging Best Practices ===" << std::endl;

    std::cout << "\n1. Compile with debug symbols:" << std::endl;
    std::cout << "   g++ -g -O0 main.cpp" << std::endl;

    std::cout << "\n2. Enable compiler warnings:" << std::endl;
    std::cout << "   g++ -Wall -Wextra -Wpedantic main.cpp" << std::endl;

    std::cout << "\n3. Use sanitizers during development:" << std::endl;
    std::cout << "   g++ -fsanitize=address,undefined main.cpp" << std::endl;

    std::cout << "\n4. Write tests:" << std::endl;
    std::cout << "   - Unit tests catch bugs early" << std::endl;
    std::cout << "   - Easier to debug small functions" << std::endl;

    std::cout << "\n5. Use version control:" << std::endl;
    std::cout << "   - Commit frequently" << std::endl;
    std::cout << "   - Easy to revert changes" << std::endl;
    std::cout << "   - git bisect for finding bugs" << std::endl;

    std::cout << "\n6. Code review:" << std::endl;
    std::cout << "   - Fresh eyes catch bugs" << std::endl;
    std::cout << "   - Share knowledge" << std::endl;

    std::cout << "\n7. Static analysis:" << std::endl;
    std::cout << "   - clang-tidy" << std::endl;
    std::cout << "   - cppcheck" << std::endl;
    std::cout << "   - Coverity" << std::endl;
}

int main() {
    std::cout << "Debugging Tools Demonstration" << std::endl;
    std::cout << "==============================" << std::endl;

    demonstrateGDB();
    demonstrateValgrind();
    demonstrateSanitizers();
    demonstrateMemoryLeaks();
    demonstrateBufferOverflow();
    demonstrateUseAfterFree();
    demonstrateAssertions();
    demonstrateDebuggingMacros();
    demonstrateLogging();
    demonstrateDebuggingStrategies();
    demonstrateCommonBugs();
    demonstrateToolComparison();
    demonstrateBestPractices();

    std::cout << "\n=== Debugging Tools Complete ===" << std::endl;
    std::cout << "\nQuick reference:" << std::endl;
    std::cout << "  Debug:     gdb ./program" << std::endl;
    std::cout << "  Memory:    valgrind --leak-check=full ./program" << std::endl;
    std::cout << "  Sanitize:  g++ -fsanitize=address,undefined main.cpp" << std::endl;

    return 0;
}
