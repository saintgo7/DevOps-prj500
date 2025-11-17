/*
 * Test Suite for Program 179: Filesystem (C++17)
 */

#include <iostream>
#include <filesystem>
#include <fstream>
#include <cassert>

using namespace std;
namespace fs = std::filesystem;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

TEST(test_path_creation) {
    fs::path p = "/tmp/test.txt";
    ASSERT_EQ(p.string(), "/tmp/test.txt");
}

TEST(test_path_filename) {
    fs::path p = "/tmp/test.txt";
    ASSERT_EQ(p.filename().string(), "test.txt");
}

TEST(test_path_parent) {
    fs::path p = "/tmp/test.txt";
    ASSERT_EQ(p.parent_path().string(), "/tmp");
}

TEST(test_path_extension) {
    fs::path p = "file.txt";
    ASSERT_EQ(p.extension().string(), ".txt");
}

TEST(test_path_stem) {
    fs::path p = "file.txt";
    ASSERT_EQ(p.stem().string(), "file");
}

TEST(test_path_concatenation) {
    fs::path p1 = "/tmp";
    fs::path p2 = "test.txt";
    fs::path combined = p1 / p2;
    ASSERT_EQ(combined.string(), "/tmp/test.txt");
}

TEST(test_current_path) {
    fs::path p = fs::current_path();
    ASSERT_TRUE(!p.empty());
}

TEST(test_temp_directory) {
    fs::path temp = fs::temp_directory_path();
    ASSERT_TRUE(!temp.empty());
    ASSERT_TRUE(fs::exists(temp));
}

int main() {
    cout << "Running Filesystem Tests\n========================\n\n";
    RUN_TEST(test_path_creation);
    RUN_TEST(test_path_filename);
    RUN_TEST(test_path_parent);
    RUN_TEST(test_path_extension);
    RUN_TEST(test_path_stem);
    RUN_TEST(test_path_concatenation);
    RUN_TEST(test_current_path);
    RUN_TEST(test_temp_directory);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
