/*
 * Program 133: Smart Pointers in C++ (C++11)
 *
 * This program demonstrates:
 * - unique_ptr - exclusive ownership
 * - shared_ptr - shared ownership with reference counting
 * - weak_ptr - non-owning references to shared_ptr
 * - make_unique and make_shared
 * - Custom deleters
 * - Avoiding memory leaks
 * - Smart pointer best practices
 */

#include <iostream>
#include <string>
#include <memory>  // For smart pointers
#include <vector>

using namespace std;

// ===== CLASS FOR DEMONSTRATION =====

class Resource {
private:
    string name;
    int id;
    static int count;

public:
    Resource(const string& n, int i) : name(n), id(i) {
        count++;
        cout << "Resource created: " << name << " (ID: " << id
             << "), Total: " << count << endl;
    }

    ~Resource() {
        count--;
        cout << "Resource destroyed: " << name << " (ID: " << id
             << "), Remaining: " << count << endl;
    }

    void use() const {
        cout << "Using resource: " << name << " (ID: " << id << ")" << endl;
    }

    string getName() const { return name; }
    int getId() const { return id; }

    static int getCount() { return count; }
};

int Resource::count = 0;

// ===== UNIQUE_PTR DEMONSTRATION =====

void demonstrateUniquePtr() {
    cout << "\n=== unique_ptr Demonstration ===" << endl;
    cout << "---------------------------------" << endl;

    // 1. Basic unique_ptr
    cout << "\n1. Basic unique_ptr:" << endl;
    {
        unique_ptr<Resource> ptr1(new Resource("Resource1", 1));
        ptr1->use();

        // Automatic cleanup when ptr1 goes out of scope
    }
    cout << "ptr1 out of scope, resource cleaned up automatically" << endl;

    // 2. make_unique (C++14) - preferred way
    cout << "\n2. Using make_unique:" << endl;
    {
        auto ptr2 = make_unique<Resource>("Resource2", 2);
        ptr2->use();
    }

    // 3. Transfer ownership with std::move
    cout << "\n3. Transfer ownership:" << endl;
    {
        unique_ptr<Resource> ptr3 = make_unique<Resource>("Resource3", 3);
        cout << "ptr3 owns resource" << endl;

        unique_ptr<Resource> ptr4 = std::move(ptr3);  // Ownership transferred
        cout << "Ownership transferred to ptr4" << endl;

        if (!ptr3) {
            cout << "ptr3 is now null" << endl;
        }

        if (ptr4) {
            cout << "ptr4 owns the resource" << endl;
            ptr4->use();
        }
    }

    // 4. Array unique_ptr
    cout << "\n4. unique_ptr with arrays:" << endl;
    {
        unique_ptr<int[]> arr = make_unique<int[]>(5);
        for (int i = 0; i < 5; i++) {
            arr[i] = i * 10;
        }

        cout << "Array contents: ";
        for (int i = 0; i < 5; i++) {
            cout << arr[i] << " ";
        }
        cout << endl;
    }

    // 5. Custom deleter
    cout << "\n5. Custom deleter:" << endl;
    {
        auto customDeleter = [](Resource* r) {
            cout << "Custom deleter called for: " << r->getName() << endl;
            delete r;
        };

        unique_ptr<Resource, decltype(customDeleter)> ptr5(
            new Resource("Resource5", 5), customDeleter);
        ptr5->use();
    }
}

// ===== SHARED_PTR DEMONSTRATION =====

void demonstrateSharedPtr() {
    cout << "\n=== shared_ptr Demonstration ===" << endl;
    cout << "---------------------------------" << endl;

    // 1. Basic shared_ptr
    cout << "\n1. Basic shared_ptr:" << endl;
    {
        shared_ptr<Resource> ptr1 = make_shared<Resource>("SharedResource1", 10);
        cout << "Reference count: " << ptr1.use_count() << endl;
        ptr1->use();

        {
            shared_ptr<Resource> ptr2 = ptr1;  // Share ownership
            cout << "After copying, reference count: " << ptr1.use_count() << endl;
            ptr2->use();

            shared_ptr<Resource> ptr3 = ptr1;
            cout << "With 3 owners, reference count: " << ptr1.use_count() << endl;
            cout << "ptr3 going out of scope..." << endl;
        }
        cout << "After inner scope, reference count: " << ptr1.use_count() << endl;
    }
    cout << "All shared_ptrs out of scope, resource cleaned up" << endl;

    // 2. make_shared - efficient
    cout << "\n2. Using make_shared:" << endl;
    {
        auto ptr = make_shared<Resource>("SharedResource2", 20);
        cout << "Created with make_shared, count: " << ptr.use_count() << endl;
    }

    // 3. Sharing in containers
    cout << "\n3. Shared pointers in containers:" << endl;
    {
        vector<shared_ptr<Resource>> resources;

        auto res1 = make_shared<Resource>("VectorResource1", 31);
        auto res2 = make_shared<Resource>("VectorResource2", 32);

        resources.push_back(res1);
        resources.push_back(res2);
        resources.push_back(res1);  // Same resource shared multiple times

        cout << "res1 reference count: " << res1.use_count() << endl;
        cout << "res2 reference count: " << res2.use_count() << endl;

        for (const auto& res : resources) {
            res->use();
        }
    }

    // 4. Custom deleter with shared_ptr
    cout << "\n4. Custom deleter with shared_ptr:" << endl;
    {
        auto deleter = [](Resource* r) {
            cout << "Custom shared_ptr deleter for: " << r->getName() << endl;
            delete r;
        };

        shared_ptr<Resource> ptr(new Resource("CustomDeleted", 40), deleter);
        ptr->use();
    }

    // 5. Resetting and releasing
    cout << "\n5. Resetting shared_ptr:" << endl;
    {
        auto ptr1 = make_shared<Resource>("ResetResource", 50);
        auto ptr2 = ptr1;

        cout << "Reference count: " << ptr1.use_count() << endl;

        ptr1.reset();  // Release ptr1's ownership
        cout << "After ptr1.reset(), ptr2 count: " << ptr2.use_count() << endl;

        ptr2.reset(new Resource("NewResource", 51));
        cout << "After ptr2.reset(new), count: " << ptr2.use_count() << endl;
    }
}

// ===== WEAK_PTR DEMONSTRATION =====

class Node;

class Node {
public:
    string name;
    shared_ptr<Node> next;    // Strong reference
    weak_ptr<Node> prev;      // Weak reference to avoid circular dependency

    Node(const string& n) : name(n) {
        cout << "Node created: " << name << endl;
    }

    ~Node() {
        cout << "Node destroyed: " << name << endl;
    }
};

void demonstrateWeakPtr() {
    cout << "\n=== weak_ptr Demonstration ===" << endl;
    cout << "-------------------------------" << endl;

    // 1. Basic weak_ptr
    cout << "\n1. Basic weak_ptr:" << endl;
    {
        weak_ptr<Resource> weakPtr;

        {
            auto sharedPtr = make_shared<Resource>("WeakResource", 60);
            weakPtr = sharedPtr;  // Doesn't increase reference count

            cout << "shared_ptr count: " << sharedPtr.use_count() << endl;
            cout << "weak_ptr expired? " << (weakPtr.expired() ? "Yes" : "No") << endl;

            // Lock to get shared_ptr
            if (auto locked = weakPtr.lock()) {
                locked->use();
                cout << "Successfully locked weak_ptr" << endl;
            }
        }

        cout << "After shared_ptr destroyed:" << endl;
        cout << "weak_ptr expired? " << (weakPtr.expired() ? "Yes" : "No") << endl;

        if (auto locked = weakPtr.lock()) {
            cout << "Locked successfully" << endl;
        } else {
            cout << "Failed to lock - resource is gone" << endl;
        }
    }

    // 2. Avoiding circular references
    cout << "\n2. Avoiding circular references:" << endl;
    {
        auto node1 = make_shared<Node>("Node1");
        auto node2 = make_shared<Node>("Node2");
        auto node3 = make_shared<Node>("Node3");

        // Build doubly-linked list
        node1->next = node2;
        node2->prev = node1;  // weak_ptr, doesn't increase count
        node2->next = node3;
        node3->prev = node2;  // weak_ptr

        cout << "node1 count: " << node1.use_count() << endl;
        cout << "node2 count: " << node2.use_count() << endl;
        cout << "node3 count: " << node3.use_count() << endl;

        // Can still access through weak_ptr
        if (auto prev = node2->prev.lock()) {
            cout << "node2's previous: " << prev->name << endl;
        }
    }
    cout << "All nodes properly destroyed (no circular reference leak)" << endl;

    // 3. Observer pattern with weak_ptr
    cout << "\n3. Observer pattern:" << endl;
    {
        vector<weak_ptr<Resource>> observers;

        {
            auto res1 = make_shared<Resource>("ObservedResource1", 71);
            auto res2 = make_shared<Resource>("ObservedResource2", 72);

            observers.push_back(res1);
            observers.push_back(res2);

            cout << "Notifying observers:" << endl;
            for (auto& weakObs : observers) {
                if (auto obs = weakObs.lock()) {
                    obs->use();
                } else {
                    cout << "Observer no longer exists" << endl;
                }
            }

            cout << "\nres1 going out of scope..." << endl;
        }

        cout << "\nTrying to notify after some resources destroyed:" << endl;
        for (auto& weakObs : observers) {
            if (auto obs = weakObs.lock()) {
                obs->use();
            } else {
                cout << "Observer no longer exists" << endl;
            }
        }
    }
}

// ===== PRACTICAL EXAMPLES =====

// Factory function returning unique_ptr
unique_ptr<Resource> createResource(const string& name, int id) {
    return make_unique<Resource>(name, id);
}

// Function accepting unique_ptr by move
void consumeResource(unique_ptr<Resource> res) {
    cout << "Function received resource: ";
    res->use();
    // Resource automatically cleaned up when function exits
}

// Function accepting shared_ptr by value (shares ownership)
void shareResource(shared_ptr<Resource> res) {
    cout << "Function sharing resource (count: " << res.use_count() << "): ";
    res->use();
}

// Function accepting shared_ptr by const reference (doesn't share)
void useResource(const shared_ptr<Resource>& res) {
    cout << "Function using resource (count: " << res.use_count() << "): ";
    res->use();
}

class ResourceManager {
private:
    vector<shared_ptr<Resource>> resources;

public:
    void addResource(shared_ptr<Resource> res) {
        resources.push_back(res);
        cout << "Added resource to manager" << endl;
    }

    void useAllResources() {
        cout << "\nUsing all managed resources:" << endl;
        for (const auto& res : resources) {
            res->use();
        }
    }

    void displayCounts() {
        cout << "\nResource reference counts:" << endl;
        for (const auto& res : resources) {
            cout << res->getName() << ": " << res.use_count() << endl;
        }
    }
};

int main() {
    cout << "=== Program 133: Smart Pointers ===" << endl;
    cout << "===================================\n" << endl;

    // 1. unique_ptr demonstrations
    demonstrateUniquePtr();

    // 2. shared_ptr demonstrations
    demonstrateSharedPtr();

    // 3. weak_ptr demonstrations
    demonstrateWeakPtr();

    // 4. Practical usage patterns
    cout << "\n=== Practical Usage Patterns ===" << endl;
    cout << "---------------------------------" << endl;

    cout << "\n1. Factory function with unique_ptr:" << endl;
    {
        auto res = createResource("FactoryResource", 80);
        res->use();
    }

    cout << "\n2. Passing unique_ptr to function:" << endl;
    {
        auto res = make_unique<Resource>("ConsumedResource", 81);
        consumeResource(std::move(res));  // Transfer ownership

        if (!res) {
            cout << "Original pointer is now null" << endl;
        }
    }

    cout << "\n3. Sharing with shared_ptr:" << endl;
    {
        auto res = make_shared<Resource>("SharedResource", 82);
        cout << "Initial count: " << res.use_count() << endl;

        shareResource(res);  // Shares ownership temporarily
        cout << "After shareResource: " << res.use_count() << endl;

        useResource(res);    // Doesn't share ownership
        cout << "After useResource: " << res.use_count() << endl;
    }

    cout << "\n4. Resource manager with shared_ptr:" << endl;
    {
        ResourceManager manager;

        auto res1 = make_shared<Resource>("ManagedResource1", 91);
        auto res2 = make_shared<Resource>("ManagedResource2", 92);

        cout << "Before adding to manager, res1 count: " << res1.use_count() << endl;

        manager.addResource(res1);
        manager.addResource(res2);
        manager.addResource(res1);  // Same resource added twice

        manager.displayCounts();
        manager.useAllResources();
    }

    // 5. Polymorphism with smart pointers
    cout << "\n5. Polymorphism with smart pointers:" << endl;
    {
        vector<unique_ptr<Resource>> resources;
        resources.push_back(make_unique<Resource>("Poly1", 101));
        resources.push_back(make_unique<Resource>("Poly2", 102));
        resources.push_back(make_unique<Resource>("Poly3", 103));

        for (const auto& res : resources) {
            res->use();
        }
        // All resources automatically cleaned up
    }

    cout << "\n=== Key Concepts Demonstrated ===" << endl;
    cout << "1. unique_ptr - exclusive ownership, move-only" << endl;
    cout << "2. shared_ptr - shared ownership, reference counting" << endl;
    cout << "3. weak_ptr - non-owning reference, breaks cycles" << endl;
    cout << "4. make_unique/make_shared - safe construction" << endl;
    cout << "5. Custom deleters - for special cleanup" << endl;
    cout << "6. Automatic memory management - no leaks" << endl;
    cout << "7. Move semantics with unique_ptr" << endl;
    cout << "8. Reference counting with shared_ptr" << endl;
    cout << "9. Avoiding circular references with weak_ptr" << endl;
    cout << "10. Smart pointers in containers and polymorphism" << endl;

    cout << "\nTotal remaining resources: " << Resource::getCount() << endl;

    return 0;
}
