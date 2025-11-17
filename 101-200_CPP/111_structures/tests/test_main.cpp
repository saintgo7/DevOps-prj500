/*
 * Test Suite for Program 111: Structures
 *
 * Tests struct declaration, initialization, and operations
 */

#include <iostream>
#include <string>
#include <cassert>

#define TEST(name) void name()
#define ASSERT_EQ(expected, actual) assert((expected) == (actual))
#define ASSERT_TRUE(condition) assert(condition)
#define RUN_TEST(test) \
    std::cout << "Running " << #test << "..." << std::endl; \
    test(); \
    std::cout << "PASSED: " << #test << std::endl;

// Test structures
struct Point {
    int x;
    int y;
};

struct Person {
    std::string name;
    int age;
    double height;
};

struct Rectangle {
    int width;
    int height;

    int area() const {
        return width * height;
    }
};

struct Node {
    int data;
    Node* next;
};

// Tests
TEST(test_struct_declaration) {
    Point p;
    p.x = 10;
    p.y = 20;

    ASSERT_EQ(p.x, 10);
    ASSERT_EQ(p.y, 20);
}

TEST(test_struct_initialization) {
    Point p = {5, 10};
    ASSERT_EQ(p.x, 5);
    ASSERT_EQ(p.y, 10);

    Point p2{15, 25};  // C++11 uniform initialization
    ASSERT_EQ(p2.x, 15);
    ASSERT_EQ(p2.y, 25);
}

TEST(test_struct_assignment) {
    Point p1 = {10, 20};
    Point p2 = p1;

    ASSERT_EQ(p2.x, 10);
    ASSERT_EQ(p2.y, 20);
}

TEST(test_struct_with_strings) {
    Person person = {"Alice", 30, 5.6};

    ASSERT_EQ(person.name, "Alice");
    ASSERT_EQ(person.age, 30);
    ASSERT_TRUE(person.height > 5.5 && person.height < 5.7);
}

TEST(test_struct_member_functions) {
    Rectangle rect = {5, 10};
    ASSERT_EQ(rect.area(), 50);

    rect.width = 3;
    rect.height = 4;
    ASSERT_EQ(rect.area(), 12);
}

TEST(test_struct_pointer) {
    Point p = {10, 20};
    Point* ptr = &p;

    ASSERT_EQ(ptr->x, 10);
    ASSERT_EQ(ptr->y, 20);

    ptr->x = 30;
    ASSERT_EQ(p.x, 30);
}

TEST(test_struct_array) {
    Point points[3] = {{1, 2}, {3, 4}, {5, 6}};

    ASSERT_EQ(points[0].x, 1);
    ASSERT_EQ(points[1].y, 4);
    ASSERT_EQ(points[2].x, 5);
}

TEST(test_nested_struct) {
    struct Address {
        std::string city;
        int zipcode;
    };

    struct Employee {
        std::string name;
        Address address;
    };

    Employee emp = {"Bob", {"New York", 10001}};
    ASSERT_EQ(emp.name, "Bob");
    ASSERT_EQ(emp.address.city, "New York");
    ASSERT_EQ(emp.address.zipcode, 10001);
}

TEST(test_struct_with_pointer_member) {
    Node node1 = {10, nullptr};
    Node node2 = {20, nullptr};
    node1.next = &node2;

    ASSERT_EQ(node1.data, 10);
    ASSERT_EQ(node1.next->data, 20);
    ASSERT_TRUE(node2.next == nullptr);
}

TEST(test_struct_sizeof) {
    ASSERT_TRUE(sizeof(Point) >= 8);  // At least 2 ints
}

TEST(test_struct_comparison) {
    Point p1 = {10, 20};
    Point p2 = {10, 20};
    Point p3 = {15, 25};

    // Manual comparison
    bool equal = (p1.x == p2.x && p1.y == p2.y);
    ASSERT_TRUE(equal);

    bool notEqual = (p1.x != p3.x || p1.y != p3.y);
    ASSERT_TRUE(notEqual);
}

TEST(test_anonymous_struct) {
    struct {
        int x;
        int y;
    } point = {5, 10};

    ASSERT_EQ(point.x, 5);
    ASSERT_EQ(point.y, 10);
}

TEST(test_struct_passed_by_value) {
    auto doublePoint = [](Point p) {
        p.x *= 2;
        p.y *= 2;
        return p;
    };

    Point original = {5, 10};
    Point doubled = doublePoint(original);

    ASSERT_EQ(original.x, 5);    // Unchanged
    ASSERT_EQ(original.y, 10);
    ASSERT_EQ(doubled.x, 10);
    ASSERT_EQ(doubled.y, 20);
}

TEST(test_struct_passed_by_reference) {
    auto doublePoint = [](Point& p) {
        p.x *= 2;
        p.y *= 2;
    };

    Point p = {5, 10};
    doublePoint(p);

    ASSERT_EQ(p.x, 10);  // Modified
    ASSERT_EQ(p.y, 20);
}

int main() {
    std::cout << "=== Running Tests for Program 111: Structures ===" << std::endl;
    std::cout << std::endl;

    RUN_TEST(test_struct_declaration);
    RUN_TEST(test_struct_initialization);
    RUN_TEST(test_struct_assignment);
    RUN_TEST(test_struct_with_strings);
    RUN_TEST(test_struct_member_functions);
    RUN_TEST(test_struct_pointer);
    RUN_TEST(test_struct_array);
    RUN_TEST(test_nested_struct);
    RUN_TEST(test_struct_with_pointer_member);
    RUN_TEST(test_struct_sizeof);
    RUN_TEST(test_struct_comparison);
    RUN_TEST(test_anonymous_struct);
    RUN_TEST(test_struct_passed_by_value);
    RUN_TEST(test_struct_passed_by_reference);

    std::cout << std::endl;
    std::cout << "=== All Tests Passed ===" << std::endl;

    return 0;
}
