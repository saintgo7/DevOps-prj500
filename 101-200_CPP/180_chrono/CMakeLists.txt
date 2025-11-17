cmake_minimum_required(VERSION 3.14)
project(CPP_Program)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Main executable
add_executable(main src/main.cpp)
target_include_directories(main PRIVATE include)

# Tests (optional - requires Google Test)
# add_executable(tests tests/test_main.cpp)
# target_include_directories(tests PRIVATE include)
# target_link_libraries(tests gtest gtest_main pthread)
