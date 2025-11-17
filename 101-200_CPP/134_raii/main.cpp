/*
 * Program 134: RAII (Resource Acquisition Is Initialization) in C++
 *
 * This program demonstrates:
 * - RAII principle and philosophy
 * - Automatic resource management
 * - Constructor acquires resources
 * - Destructor releases resources
 * - Exception safety with RAII
 * - RAII wrappers for various resources
 * - Scope-based resource management
 * - Lock guards and mutex wrappers
 */

#include <iostream>
#include <string>
#include <fstream>
#include <memory>
#include <mutex>
#include <stdexcept>

using namespace std;

// ===== BASIC RAII EXAMPLE - FILE HANDLE =====

class FileHandle {
private:
    FILE* file;
    string filename;

public:
    // Constructor acquires the resource
    FileHandle(const string& fname, const char* mode) : filename(fname) {
        file = fopen(fname.c_str(), mode);
        if (!file) {
            throw runtime_error("Failed to open file: " + fname);
        }
        cout << "File opened: " << filename << endl;
    }

    // Destructor releases the resource
    ~FileHandle() {
        if (file) {
            fclose(file);
            cout << "File closed: " << filename << endl;
        }
    }

    // Prevent copying
    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;

    // Allow moving (C++11)
    FileHandle(FileHandle&& other) noexcept
        : file(other.file), filename(std::move(other.filename)) {
        other.file = nullptr;
    }

    void write(const string& text) {
        if (file) {
            fprintf(file, "%s\n", text.c_str());
        }
    }

    FILE* get() { return file; }
};

// ===== RAII FOR MEMORY MANAGEMENT =====

class DynamicBuffer {
private:
    char* buffer;
    size_t size;

public:
    // Acquire memory in constructor
    explicit DynamicBuffer(size_t s) : size(s) {
        buffer = new char[size];
        cout << "Buffer allocated: " << size << " bytes" << endl;
    }

    // Release memory in destructor
    ~DynamicBuffer() {
        delete[] buffer;
        cout << "Buffer deallocated: " << size << " bytes" << endl;
    }

    // Prevent copying (or implement proper copy semantics)
    DynamicBuffer(const DynamicBuffer&) = delete;
    DynamicBuffer& operator=(const DynamicBuffer&) = delete;

    // Move semantics
    DynamicBuffer(DynamicBuffer&& other) noexcept
        : buffer(other.buffer), size(other.size) {
        other.buffer = nullptr;
        other.size = 0;
    }

    char* data() { return buffer; }
    size_t getSize() const { return size; }
};

// ===== RAII FOR DATABASE CONNECTION =====

class DatabaseConnection {
private:
    string connectionString;
    bool connected;
    int connectionId;
    static int nextId;

public:
    DatabaseConnection(const string& connStr) : connectionString(connStr) {
        connectionId = nextId++;
        // Simulate opening connection
        connected = true;
        cout << "Database connection " << connectionId
             << " opened: " << connectionString << endl;
    }

    ~DatabaseConnection() {
        if (connected) {
            // Simulate closing connection
            cout << "Database connection " << connectionId << " closed" << endl;
            connected = false;
        }
    }

    // Prevent copying
    DatabaseConnection(const DatabaseConnection&) = delete;
    DatabaseConnection& operator=(const DatabaseConnection&) = delete;

    void executeQuery(const string& query) {
        if (connected) {
            cout << "Executing query: " << query << endl;
        } else {
            throw runtime_error("Not connected to database");
        }
    }

    bool isConnected() const { return connected; }
};

int DatabaseConnection::nextId = 1;

// ===== RAII FOR LOCK MANAGEMENT =====

class SimpleMutex {
private:
    bool locked;

public:
    SimpleMutex() : locked(false) {}

    void lock() {
        cout << "Mutex locked" << endl;
        locked = true;
    }

    void unlock() {
        cout << "Mutex unlocked" << endl;
        locked = false;
    }

    bool isLocked() const { return locked; }
};

// RAII lock guard
class LockGuard {
private:
    SimpleMutex& mutex;

public:
    explicit LockGuard(SimpleMutex& m) : mutex(m) {
        mutex.lock();
    }

    ~LockGuard() {
        mutex.unlock();
    }

    // Prevent copying
    LockGuard(const LockGuard&) = delete;
    LockGuard& operator=(const LockGuard&) = delete;
};

// ===== RAII FOR TIMER =====

#include <chrono>

class Timer {
private:
    string name;
    chrono::high_resolution_clock::time_point start;

public:
    explicit Timer(const string& n) : name(n) {
        start = chrono::high_resolution_clock::now();
        cout << "Timer '" << name << "' started" << endl;
    }

    ~Timer() {
        auto end = chrono::high_resolution_clock::now();
        auto duration = chrono::duration_cast<chrono::microseconds>(end - start);
        cout << "Timer '" << name << "' finished: "
             << duration.count() << " microseconds" << endl;
    }
};

// ===== RAII FOR RESOURCE POOL =====

class ResourcePool {
private:
    int totalResources;
    int availableResources;

public:
    explicit ResourcePool(int total)
        : totalResources(total), availableResources(total) {
        cout << "Resource pool created with " << total << " resources" << endl;
    }

    ~ResourcePool() {
        cout << "Resource pool destroyed (freed " << totalResources
             << " resources)" << endl;
    }

    class ResourceLease {
    private:
        ResourcePool& pool;
        bool valid;

    public:
        explicit ResourceLease(ResourcePool& p) : pool(p), valid(false) {
            if (pool.availableResources > 0) {
                pool.availableResources--;
                valid = true;
                cout << "Resource acquired (available: "
                     << pool.availableResources << ")" << endl;
            } else {
                throw runtime_error("No resources available");
            }
        }

        ~ResourceLease() {
            if (valid) {
                pool.availableResources++;
                cout << "Resource released (available: "
                     << pool.availableResources << ")" << endl;
            }
        }

        ResourceLease(const ResourceLease&) = delete;
        ResourceLease& operator=(const ResourceLease&) = delete;
    };

    ResourceLease acquire() {
        return ResourceLease(*this);
    }

    int getAvailable() const { return availableResources; }
};

// ===== EXCEPTION SAFETY WITH RAII =====

void riskyOperation() {
    cout << "\nRisky operation without RAII:" << endl;
    cout << "------------------------------" << endl;

    int* data = new int[100];
    cout << "Memory allocated" << endl;

    // If exception occurs here, memory leaks!
    // throw runtime_error("Something went wrong");

    delete[] data;
    cout << "Memory deallocated" << endl;
}

void safeOperation() {
    cout << "\nSafe operation with RAII:" << endl;
    cout << "--------------------------" << endl;

    unique_ptr<int[]> data(new int[100]);
    cout << "Memory allocated (RAII)" << endl;

    // Even if exception occurs, RAII ensures cleanup
    // throw runtime_error("Something went wrong");

    cout << "Operation completed" << endl;
    // Memory automatically deallocated
}

// ===== SCOPE GUARD PATTERN =====

template<typename Func>
class ScopeGuard {
private:
    Func func;
    bool active;

public:
    explicit ScopeGuard(Func f) : func(f), active(true) {}

    ~ScopeGuard() {
        if (active) {
            func();
        }
    }

    void dismiss() {
        active = false;
    }

    ScopeGuard(const ScopeGuard&) = delete;
    ScopeGuard& operator=(const ScopeGuard&) = delete;
};

template<typename Func>
ScopeGuard<Func> makeScopeGuard(Func f) {
    return ScopeGuard<Func>(f);
}

// ===== MULTIPLE RESOURCES WITH RAII =====

class Transaction {
private:
    DatabaseConnection dbConn;
    bool committed;

public:
    Transaction(const string& connStr)
        : dbConn(connStr), committed(false) {
        cout << "Transaction started" << endl;
        dbConn.executeQuery("BEGIN TRANSACTION");
    }

    ~Transaction() {
        if (!committed) {
            cout << "Rolling back transaction" << endl;
            try {
                dbConn.executeQuery("ROLLBACK");
            } catch (...) {
                // Destructor should not throw
            }
        }
    }

    void commit() {
        dbConn.executeQuery("COMMIT");
        committed = true;
        cout << "Transaction committed" << endl;
    }

    DatabaseConnection& getConnection() {
        return dbConn;
    }
};

// ===== RAII IN PRACTICE =====

void demonstrateFileRAII() {
    cout << "\n=== File Handling with RAII ===" << endl;
    cout << "--------------------------------" << endl;

    try {
        FileHandle file("test.txt", "w");
        file.write("Hello, RAII!");
        file.write("Automatic cleanup guaranteed");
        // File automatically closed when exiting scope
    } catch (const exception& e) {
        cout << "Error: " << e.what() << endl;
    }

    cout << "\nFile operations complete" << endl;
}

void demonstrateLockRAII() {
    cout << "\n=== Lock Management with RAII ===" << endl;
    cout << "----------------------------------" << endl;

    SimpleMutex mutex;

    {
        LockGuard lock(mutex);
        cout << "Critical section - mutex is locked" << endl;
        cout << "Performing thread-safe operations..." << endl;
        // Lock automatically released when exiting scope
    }

    cout << "Outside critical section - mutex unlocked" << endl;
}

void demonstrateTimerRAII() {
    cout << "\n=== Timing with RAII ===" << endl;
    cout << "------------------------" << endl;

    {
        Timer timer("ComplexOperation");

        // Simulate work
        int sum = 0;
        for (int i = 0; i < 1000000; i++) {
            sum += i;
        }

        cout << "Work completed (sum: " << sum << ")" << endl;
        // Timer automatically prints duration on destruction
    }
}

void demonstrateResourcePool() {
    cout << "\n=== Resource Pool with RAII ===" << endl;
    cout << "--------------------------------" << endl;

    ResourcePool pool(3);

    {
        cout << "\nAcquiring resources:" << endl;
        auto res1 = pool.acquire();
        auto res2 = pool.acquire();
        auto res3 = pool.acquire();

        cout << "All 3 resources acquired" << endl;
        cout << "Available: " << pool.getAvailable() << endl;

        try {
            auto res4 = pool.acquire();  // Should fail
        } catch (const exception& e) {
            cout << "Expected error: " << e.what() << endl;
        }

        cout << "\nResources going out of scope..." << endl;
    }

    cout << "\nAfter scope, available: " << pool.getAvailable() << endl;
}

void demonstrateScopeGuard() {
    cout << "\n=== Scope Guard Pattern ===" << endl;
    cout << "---------------------------" << endl;

    int value = 0;

    {
        auto guard = makeScopeGuard([&]() {
            cout << "Scope guard cleanup: restoring value" << endl;
            value = 0;
        });

        value = 42;
        cout << "Value modified to: " << value << endl;

        // guard.dismiss();  // Can dismiss if not needed

        cout << "Exiting scope..." << endl;
    }

    cout << "After scope, value: " << value << endl;
}

void demonstrateTransaction() {
    cout << "\n=== Transaction with RAII ===" << endl;
    cout << "-----------------------------" << endl;

    {
        Transaction trans("localhost:5432");
        trans.getConnection().executeQuery("INSERT INTO users VALUES (1, 'Alice')");
        trans.getConnection().executeQuery("INSERT INTO users VALUES (2, 'Bob')");

        trans.commit();  // Explicit commit
        // If commit not called, automatic rollback in destructor
    }

    cout << "\nSimulating failed transaction:" << endl;
    {
        Transaction trans2("localhost:5432");
        trans2.getConnection().executeQuery("INSERT INTO users VALUES (3, 'Charlie')");

        // Oops, forgot to commit or exception occurred
        // Destructor will rollback automatically
    }
}

int main() {
    cout << "=== Program 134: RAII ===" << endl;
    cout << "=========================\n" << endl;

    // 1. File handling with RAII
    demonstrateFileRAII();

    // 2. Memory management with RAII
    cout << "\n=== Memory Management with RAII ===" << endl;
    cout << "------------------------------------" << endl;
    {
        DynamicBuffer buffer(1024);
        cout << "Using buffer..." << endl;
        // Automatically freed on scope exit
    }

    // 3. Database connection with RAII
    cout << "\n=== Database Connection with RAII ===" << endl;
    cout << "--------------------------------------" << endl;
    {
        DatabaseConnection db("server=localhost;db=mydb");
        db.executeQuery("SELECT * FROM users");
        // Connection automatically closed
    }

    // 4. Lock management with RAII
    demonstrateLockRAII();

    // 5. Timer with RAII
    demonstrateTimerRAII();

    // 6. Exception safety
    cout << "\n=== Exception Safety with RAII ===" << endl;
    cout << "-----------------------------------" << endl;
    riskyOperation();
    safeOperation();

    // 7. Resource pool
    demonstrateResourcePool();

    // 8. Scope guard
    demonstrateScopeGuard();

    // 9. Transaction
    demonstrateTransaction();

    // 10. Standard library RAII examples
    cout << "\n=== Standard Library RAII ===" << endl;
    cout << "-----------------------------" << endl;
    {
        unique_ptr<int> ptr(new int(42));
        cout << "unique_ptr value: " << *ptr << endl;

        mutex m;
        {
            lock_guard<mutex> lock(m);
            cout << "Mutex locked with lock_guard" << endl;
        }
        cout << "Mutex automatically unlocked" << endl;

        ofstream file("output.txt");
        file << "RAII with ofstream" << endl;
        // File automatically closed
    }

    cout << "\n=== Key Concepts Demonstrated ===" << endl;
    cout << "1. RAII - Resource Acquisition Is Initialization" << endl;
    cout << "2. Constructor acquires resources" << endl;
    cout << "3. Destructor releases resources" << endl;
    cout << "4. Automatic cleanup on scope exit" << endl;
    cout << "5. Exception safety - cleanup even with exceptions" << endl;
    cout << "6. No manual resource management needed" << endl;
    cout << "7. Prevents resource leaks" << endl;
    cout << "8. Scope-based resource management" << endl;
    cout << "9. Lock guards and mutex wrappers" << endl;
    cout << "10. Smart pointers as RAII (unique_ptr, shared_ptr)" << endl;

    return 0;
}
