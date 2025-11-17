/*
 * Program 185: Shared Memory
 * Demonstrates POSIX shared memory, memory mapping, and IPC
 * Compile: g++ -std=c++17 -pthread -lrt -o shared_memory main.cpp
 */

#include <iostream>
#include <cstring>
#include <string>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/wait.h>
#include <semaphore.h>
#include <errno.h>

const char* SHM_NAME = "/test_shared_memory";
const char* SEM_NAME = "/test_semaphore";
const size_t SHM_SIZE = 4096;

// Shared data structure
struct SharedData {
    int counter;
    char message[256];
    bool ready;
};

void demonstrateBasicSharedMemory() {
    std::cout << "\n=== Basic Shared Memory Demonstration ===" << std::endl;

    // Remove existing shared memory if any
    shm_unlink(SHM_NAME);

    // Create shared memory object
    int shm_fd = shm_open(SHM_NAME, O_CREAT | O_RDWR, 0666);
    if (shm_fd == -1) {
        std::cerr << "Failed to create shared memory: " << strerror(errno) << std::endl;
        return;
    }

    std::cout << "Shared memory created: " << SHM_NAME << std::endl;

    // Set size of shared memory
    if (ftruncate(shm_fd, sizeof(SharedData)) == -1) {
        std::cerr << "Failed to set shared memory size: " << strerror(errno) << std::endl;
        close(shm_fd);
        shm_unlink(SHM_NAME);
        return;
    }

    // Map shared memory
    SharedData* shared_data = static_cast<SharedData*>(
        mmap(nullptr, sizeof(SharedData), PROT_READ | PROT_WRITE,
             MAP_SHARED, shm_fd, 0)
    );

    if (shared_data == MAP_FAILED) {
        std::cerr << "Failed to map shared memory: " << strerror(errno) << std::endl;
        close(shm_fd);
        shm_unlink(SHM_NAME);
        return;
    }

    std::cout << "Shared memory mapped at: " << static_cast<void*>(shared_data) << std::endl;

    // Initialize shared data
    shared_data->counter = 0;
    strcpy(shared_data->message, "Initial message");
    shared_data->ready = false;

    std::cout << "Initial counter: " << shared_data->counter << std::endl;
    std::cout << "Initial message: " << shared_data->message << std::endl;

    pid_t pid = fork();

    if (pid < 0) {
        std::cerr << "Fork failed" << std::endl;
        munmap(shared_data, sizeof(SharedData));
        close(shm_fd);
        shm_unlink(SHM_NAME);
        return;
    }

    if (pid == 0) {
        // Child process
        std::cout << "\nChild: Accessing shared memory..." << std::endl;

        // Child modifies shared data
        shared_data->counter = 42;
        strcpy(shared_data->message, "Modified by child process!");
        shared_data->ready = true;

        std::cout << "Child: Updated counter to: " << shared_data->counter << std::endl;
        std::cout << "Child: Updated message to: " << shared_data->message << std::endl;

        munmap(shared_data, sizeof(SharedData));
        close(shm_fd);
        exit(0);
    } else {
        // Parent process
        sleep(1);  // Give child time to modify

        std::cout << "\nParent: Reading shared memory after child modification..." << std::endl;
        std::cout << "Counter: " << shared_data->counter << std::endl;
        std::cout << "Message: " << shared_data->message << std::endl;
        std::cout << "Ready: " << (shared_data->ready ? "true" : "false") << std::endl;

        wait(nullptr);

        // Cleanup
        munmap(shared_data, sizeof(SharedData));
        close(shm_fd);
        shm_unlink(SHM_NAME);

        std::cout << "\nShared memory cleaned up" << std::endl;
    }
}

void demonstrateSynchronizedSharedMemory() {
    std::cout << "\n=== Synchronized Shared Memory with Semaphore ===" << std::endl;

    // Remove existing resources
    shm_unlink(SHM_NAME);
    sem_unlink(SEM_NAME);

    // Create shared memory
    int shm_fd = shm_open(SHM_NAME, O_CREAT | O_RDWR, 0666);
    if (shm_fd == -1) {
        std::cerr << "Failed to create shared memory" << std::endl;
        return;
    }

    ftruncate(shm_fd, sizeof(SharedData));

    SharedData* shared_data = static_cast<SharedData*>(
        mmap(nullptr, sizeof(SharedData), PROT_READ | PROT_WRITE,
             MAP_SHARED, shm_fd, 0)
    );

    if (shared_data == MAP_FAILED) {
        std::cerr << "Failed to map shared memory" << std::endl;
        close(shm_fd);
        shm_unlink(SHM_NAME);
        return;
    }

    // Create semaphore for synchronization
    sem_t* sem = sem_open(SEM_NAME, O_CREAT, 0666, 1);
    if (sem == SEM_FAILED) {
        std::cerr << "Failed to create semaphore: " << strerror(errno) << std::endl;
        munmap(shared_data, sizeof(SharedData));
        close(shm_fd);
        shm_unlink(SHM_NAME);
        return;
    }

    std::cout << "Shared memory and semaphore created" << std::endl;

    // Initialize
    shared_data->counter = 0;

    pid_t pid = fork();

    if (pid < 0) {
        std::cerr << "Fork failed" << std::endl;
        return;
    }

    if (pid == 0) {
        // Child process - increment counter multiple times
        for (int i = 0; i < 5; ++i) {
            sem_wait(sem);  // Lock

            int old_value = shared_data->counter;
            usleep(100000);  // Simulate some work
            shared_data->counter = old_value + 1;

            std::cout << "Child: Incremented counter to " << shared_data->counter << std::endl;

            sem_post(sem);  // Unlock

            usleep(50000);
        }

        sem_close(sem);
        munmap(shared_data, sizeof(SharedData));
        close(shm_fd);
        exit(0);
    } else {
        // Parent process - also increment counter
        for (int i = 0; i < 5; ++i) {
            sem_wait(sem);  // Lock

            int old_value = shared_data->counter;
            usleep(100000);  // Simulate some work
            shared_data->counter = old_value + 1;

            std::cout << "Parent: Incremented counter to " << shared_data->counter << std::endl;

            sem_post(sem);  // Unlock

            usleep(50000);
        }

        wait(nullptr);

        std::cout << "\nFinal counter value: " << shared_data->counter << std::endl;
        std::cout << "Expected: 10" << std::endl;

        // Cleanup
        sem_close(sem);
        sem_unlink(SEM_NAME);
        munmap(shared_data, sizeof(SharedData));
        close(shm_fd);
        shm_unlink(SHM_NAME);
    }
}

void demonstrateMemoryMapping() {
    std::cout << "\n=== Memory Mapping Demonstration ===" << std::endl;

    // Create a temporary file
    const char* filename = "/tmp/mmap_test.txt";
    int fd = open(filename, O_RDWR | O_CREAT | O_TRUNC, 0666);

    if (fd == -1) {
        std::cerr << "Failed to create file" << std::endl;
        return;
    }

    // Write some data to file
    const char* data = "Hello, Memory Mapped File!";
    size_t data_len = strlen(data);

    write(fd, data, data_len);

    // Extend file to page size
    size_t file_size = 4096;
    if (ftruncate(fd, file_size) == -1) {
        std::cerr << "Failed to set file size" << std::endl;
        close(fd);
        return;
    }

    std::cout << "Created and initialized file: " << filename << std::endl;
    std::cout << "Original content: " << data << std::endl;

    // Map file into memory
    char* mapped = static_cast<char*>(
        mmap(nullptr, file_size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0)
    );

    if (mapped == MAP_FAILED) {
        std::cerr << "Failed to map file: " << strerror(errno) << std::endl;
        close(fd);
        return;
    }

    std::cout << "File mapped to memory at: " << static_cast<void*>(mapped) << std::endl;

    // Read from mapped memory
    std::cout << "Content via mmap: " << mapped << std::endl;

    // Modify through mapped memory
    strcpy(mapped, "Modified via memory mapping!");

    // Sync changes to disk
    if (msync(mapped, file_size, MS_SYNC) == -1) {
        std::cerr << "Failed to sync: " << strerror(errno) << std::endl;
    }

    std::cout << "Modified content: " << mapped << std::endl;

    // Unmap memory
    munmap(mapped, file_size);
    close(fd);

    // Verify changes persisted to file
    fd = open(filename, O_RDONLY);
    char verify_buffer[256] = {0};
    read(fd, verify_buffer, sizeof(verify_buffer) - 1);
    close(fd);

    std::cout << "Content after unmapping (read from file): " << verify_buffer << std::endl;

    // Cleanup
    unlink(filename);
    std::cout << "File cleaned up" << std::endl;
}

void demonstrateAnonymousMapping() {
    std::cout << "\n=== Anonymous Memory Mapping ===" << std::endl;

    size_t size = 4096;

    // Create anonymous mapping (not backed by file)
    void* addr = mmap(nullptr, size, PROT_READ | PROT_WRITE,
                     MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);

    if (addr == MAP_FAILED) {
        std::cerr << "Failed to create anonymous mapping: " << strerror(errno) << std::endl;
        return;
    }

    std::cout << "Anonymous memory mapped at: " << addr << std::endl;

    // Use the memory
    char* data = static_cast<char*>(addr);
    strcpy(data, "This is anonymous mapped memory!");

    std::cout << "Stored data: " << data << std::endl;

    // Get memory info
    std::cout << "\nMemory region info:" << std::endl;
    std::cout << "  Address: " << addr << std::endl;
    std::cout << "  Size: " << size << " bytes" << std::endl;

    // Unmap
    munmap(addr, size);
    std::cout << "Anonymous memory unmapped" << std::endl;
}

void demonstrateSharedMemoryInfo() {
    std::cout << "\n=== Shared Memory Information ===" << std::endl;

    // Remove existing
    shm_unlink(SHM_NAME);

    // Create shared memory
    int shm_fd = shm_open(SHM_NAME, O_CREAT | O_RDWR, 0666);
    if (shm_fd == -1) {
        std::cerr << "Failed to create shared memory" << std::endl;
        return;
    }

    size_t shm_size = 8192;
    ftruncate(shm_fd, shm_size);

    // Get file statistics
    struct stat shm_stat;
    if (fstat(shm_fd, &shm_stat) == 0) {
        std::cout << "Shared memory statistics:" << std::endl;
        std::cout << "  Size: " << shm_stat.st_size << " bytes" << std::endl;
        std::cout << "  Mode: " << std::oct << (shm_stat.st_mode & 0777) << std::dec << std::endl;
        std::cout << "  Links: " << shm_stat.st_nlink << std::endl;
        std::cout << "  UID: " << shm_stat.st_uid << std::endl;
        std::cout << "  GID: " << shm_stat.st_gid << std::endl;
    }

    close(shm_fd);
    shm_unlink(SHM_NAME);
}

int main() {
    std::cout << "Shared Memory Demonstration" << std::endl;
    std::cout << "============================" << std::endl;

    demonstrateBasicSharedMemory();
    demonstrateSynchronizedSharedMemory();
    demonstrateMemoryMapping();
    demonstrateAnonymousMapping();
    demonstrateSharedMemoryInfo();

    std::cout << "\n=== Shared Memory Complete ===" << std::endl;

    return 0;
}
