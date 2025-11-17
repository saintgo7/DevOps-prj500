/*
 * Test Suite for Program 180: Chrono
 */

#include <iostream>
#include <chrono>
#include <thread>
#include <cassert>

using namespace std;
using namespace chrono;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { cout << "Running " << #name << "..."; name(); cout << " PASSED\n"; } while(0)
#define ASSERT_EQ(a, b) do { if ((a) != (b)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)
#define ASSERT_TRUE(c) do { if (!(c)) { cerr << "  FAILED\n"; tests_failed++; return; } tests_passed++; } while(0)

TEST(test_duration_seconds) {
    seconds sec(60);
    ASSERT_EQ(sec.count(), 60);
}

TEST(test_duration_milliseconds) {
    milliseconds ms(1000);
    seconds sec = duration_cast<seconds>(ms);
    ASSERT_EQ(sec.count(), 1);
}

TEST(test_duration_addition) {
    seconds s1(10);
    seconds s2(20);
    seconds result = s1 + s2;
    ASSERT_EQ(result.count(), 30);
}

TEST(test_time_point) {
    auto now = system_clock::now();
    auto later = now + seconds(10);
    auto diff = duration_cast<seconds>(later - now);
    ASSERT_EQ(diff.count(), 10);
}

TEST(test_duration_cast) {
    hours h(2);
    minutes m = duration_cast<minutes>(h);
    ASSERT_EQ(m.count(), 120);

    seconds s = duration_cast<seconds>(h);
    ASSERT_EQ(s.count(), 7200);
}

TEST(test_high_resolution_clock) {
    auto start = high_resolution_clock::now();
    this_thread::sleep_for(milliseconds(10));
    auto end = high_resolution_clock::now();

    auto elapsed = duration_cast<milliseconds>(end - start);
    ASSERT_TRUE(elapsed.count() >= 10);
}

TEST(test_steady_clock) {
    auto start = steady_clock::now();
    this_thread::sleep_for(milliseconds(5));
    auto end = steady_clock::now();

    auto elapsed = duration_cast<milliseconds>(end - start);
    ASSERT_TRUE(elapsed.count() >= 5);
}

TEST(test_duration_comparison) {
    seconds s1(10);
    seconds s2(20);
    ASSERT_TRUE(s1 < s2);
    ASSERT_TRUE(s2 > s1);
    ASSERT_TRUE(s1 != s2);
}

int main() {
    cout << "Running Chrono Tests\n====================\n\n";
    RUN_TEST(test_duration_seconds);
    RUN_TEST(test_duration_milliseconds);
    RUN_TEST(test_duration_addition);
    RUN_TEST(test_time_point);
    RUN_TEST(test_duration_cast);
    RUN_TEST(test_high_resolution_clock);
    RUN_TEST(test_steady_clock);
    RUN_TEST(test_duration_comparison);
    cout << "\nTest Results:\n  Passed: " << tests_passed << "\n  Failed: " << tests_failed << "\n";
    return tests_failed == 0 ? 0 : 1;
}
