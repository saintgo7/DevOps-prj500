# Program 180: Chrono

## Description
Explores the chrono library for time measurement, providing type-safe duration and time point representations for timing code and scheduling.

## Learning Objectives
- Use chrono clocks (system_clock, steady_clock, high_resolution_clock)
- Work with durations and time_points
- Measure code execution time
- Convert between time units
- Use chrono literals (C++14)

## Features
- Clock types and usage
- Duration types
- Time point arithmetic
- Time measurement
- Duration literals
- Chrono with threading

## Compilation
```bash
g++ -std=c++17 main.cpp -o chrono
./chrono
```

## Key Concepts
```cpp
using namespace std::chrono;

auto start = steady_clock::now();
// ... code to time ...
auto end = steady_clock::now();
auto duration = duration_cast<milliseconds>(end - start);

using namespace std::chrono_literals;
auto delay = 100ms;  // milliseconds
auto timeout = 5s;   // seconds
```

## Best Practices
1. Use steady_clock for measuring intervals
2. Use system_clock for wall-clock time
3. Leverage duration_cast for conversions
4. Use chrono literals for readability (C++14)
5. Prefer chrono over C-style time functions

## Navigation
- **Previous**: [179 - Filesystem](/home/user/DevOps-prj500/101-200_CPP/179_filesystem/README.md)
- **Next**: [181 - Socket Programming](/home/user/DevOps-prj500/101-200_CPP/181_socket_programming/README.md)
