/*
 * Program 189: Memory Mapped Files
 * Demonstrates mmap, file mapping, and shared memory mapping
 * Compile: g++ -std=c++17 -o memory_mapped_files main.cpp
 */

#include <iostream>
#include <cstring>
#include <string>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/wait.h>
#include <errno.h>

const char* TEST_FILE = "/tmp/mmap_test.dat";

void demonstrateBasicMmap() {
    std::cout << "\n=== Basic Memory Mapping ===" << std::endl;

    // Create and initialize file
    const size_t file_size = 4096;
    int fd = open(TEST_FILE, O_RDWR | O_CREAT | O_TRUNC, 0644);

    if (fd == -1) {
        std::cerr << "Failed to open file: " << strerror(errno) << std::endl;
        return;
    }

    // Set file size
    if (ftruncate(fd, file_size) == -1) {
        std::cerr << "Failed to set file size: " << strerror(errno) << std::endl;
        close(fd);
        return;
    }

    std::cout << "Created file: " << TEST_FILE << " (" << file_size << " bytes)" << std::endl;

    // Map file into memory
    void* mapped = mmap(nullptr, file_size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);

    if (mapped == MAP_FAILED) {
        std::cerr << "mmap failed: " << strerror(errno) << std::endl;
        close(fd);
        return;
    }

    std::cout << "File mapped to memory at: " << mapped << std::endl;

    // Write data through mapped memory
    char* data = static_cast<char*>(mapped);
    strcpy(data, "Hello, Memory Mapped File!");

    std::cout << "Wrote data through mmap: " << data << std::endl;

    // Sync to disk
    if (msync(mapped, file_size, MS_SYNC) == -1) {
        std::cerr << "msync failed: " << strerror(errno) << std::endl;
    } else {
        std::cout << "Data synchronized to disk" << std::endl;
    }

    // Read data
    std::cout << "Read data through mmap: " << data << std::endl;

    // Unmap memory
    if (munmap(mapped, file_size) == -1) {
        std::cerr << "munmap failed: " << strerror(errno) << std::endl;
    } else {
        std::cout << "Memory unmapped" << std::endl;
    }

    close(fd);

    // Verify data persisted
    fd = open(TEST_FILE, O_RDONLY);
    char buffer[256] = {0};
    read(fd, buffer, sizeof(buffer) - 1);
    close(fd);

    std::cout << "Data persisted to file: " << buffer << std::endl;
}

void demonstrateMmapProtections() {
    std::cout << "\n=== Memory Protection Flags ===" << std::endl;

    const size_t size = 4096;
    int fd = open(TEST_FILE, O_RDWR | O_CREAT | O_TRUNC, 0644);

    if (fd == -1) {
        std::cerr << "Failed to open file" << std::endl;
        return;
    }

    ftruncate(fd, size);

    // 1. Read-only mapping
    std::cout << "\n1. Read-only mapping (PROT_READ)" << std::endl;
    void* readonly = mmap(nullptr, size, PROT_READ, MAP_SHARED, fd, 0);

    if (readonly != MAP_FAILED) {
        std::cout << "Read-only mapping created at: " << readonly << std::endl;

        // Try to read (should work)
        char* data = static_cast<char*>(readonly);
        char c = data[0];
        std::cout << "Reading from read-only mapping: success" << std::endl;

        // Note: Writing would cause segmentation fault
        // *data = 'X';  // DON'T DO THIS!

        munmap(readonly, size);
    }

    // 2. Read-write mapping
    std::cout << "\n2. Read-write mapping (PROT_READ | PROT_WRITE)" << std::endl;
    void* readwrite = mmap(nullptr, size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);

    if (readwrite != MAP_FAILED) {
        std::cout << "Read-write mapping created at: " << readwrite << std::endl;

        char* data = static_cast<char*>(readwrite);
        strcpy(data, "Read-write test");
        std::cout << "Writing to read-write mapping: " << data << std::endl;

        munmap(readwrite, size);
    }

    // 3. Private mapping (changes not reflected to file)
    std::cout << "\n3. Private mapping (MAP_PRIVATE)" << std::endl;
    void* private_map = mmap(nullptr, size, PROT_READ | PROT_WRITE, MAP_PRIVATE, fd, 0);

    if (private_map != MAP_FAILED) {
        std::cout << "Private mapping created at: " << private_map << std::endl;

        char* data = static_cast<char*>(private_map);
        strcpy(data, "Private changes");
        std::cout << "Wrote to private mapping: " << data << std::endl;
        std::cout << "Note: Changes won't be written to file" << std::endl;

        munmap(private_map, size);
    }

    close(fd);
}

void demonstrateMmapSharing() {
    std::cout << "\n=== Shared Memory Mapping Between Processes ===" << std::endl;

    const size_t size = 4096;
    int fd = open(TEST_FILE, O_RDWR | O_CREAT | O_TRUNC, 0644);

    if (fd == -1) {
        std::cerr << "Failed to open file" << std::endl;
        return;
    }

    ftruncate(fd, size);

    // Create shared mapping
    void* shared = mmap(nullptr, size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);

    if (shared == MAP_FAILED) {
        std::cerr << "mmap failed" << std::endl;
        close(fd);
        return;
    }

    std::cout << "Shared mapping created" << std::endl;

    char* data = static_cast<char*>(shared);
    strcpy(data, "Initial data from parent");

    std::cout << "Parent wrote: " << data << std::endl;

    pid_t pid = fork();

    if (pid < 0) {
        std::cerr << "Fork failed" << std::endl;
        munmap(shared, size);
        close(fd);
        return;
    }

    if (pid == 0) {
        // Child process
        sleep(1);  // Wait for parent

        std::cout << "Child reads: " << data << std::endl;

        // Modify data
        strcpy(data, "Modified by child process");
        std::cout << "Child wrote: " << data << std::endl;

        msync(shared, size, MS_SYNC);
        munmap(shared, size);
        close(fd);
        exit(0);
    } else {
        // Parent process
        sleep(2);  // Wait for child to modify

        std::cout << "Parent reads after child: " << data << std::endl;

        wait(nullptr);

        munmap(shared, size);
        close(fd);
    }
}

void demonstrateAnonymousMmap() {
    std::cout << "\n=== Anonymous Memory Mapping ===" << std::endl;

    const size_t size = 4096;

    // Create anonymous mapping (no file backing)
    void* anon = mmap(nullptr, size, PROT_READ | PROT_WRITE,
                     MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);

    if (anon == MAP_FAILED) {
        std::cerr << "Anonymous mmap failed: " << strerror(errno) << std::endl;
        return;
    }

    std::cout << "Anonymous mapping created at: " << anon << std::endl;

    // Use the memory
    char* data = static_cast<char*>(anon);
    strcpy(data, "Anonymous mapped memory");

    std::cout << "Data stored: " << data << std::endl;

    // This memory is private to this process
    std::cout << "Memory is private and not backed by file" << std::endl;

    munmap(anon, size);
    std::cout << "Anonymous mapping unmapped" << std::endl;
}

void demonstrateMmapAdvice() {
    std::cout << "\n=== Memory Mapping Advice (madvise) ===" << std::endl;

    const size_t size = 8192;
    int fd = open(TEST_FILE, O_RDWR | O_CREAT | O_TRUNC, 0644);

    if (fd == -1) {
        std::cerr << "Failed to open file" << std::endl;
        return;
    }

    ftruncate(fd, size);

    void* mapped = mmap(nullptr, size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);

    if (mapped == MAP_FAILED) {
        std::cerr << "mmap failed" << std::endl;
        close(fd);
        return;
    }

    std::cout << "Memory mapped, providing advice to kernel..." << std::endl;

    // Tell kernel we'll access sequentially
    if (madvise(mapped, size, MADV_SEQUENTIAL) == 0) {
        std::cout << "MADV_SEQUENTIAL: Optimized for sequential access" << std::endl;
    }

    // Tell kernel we'll access randomly
    if (madvise(mapped, size, MADV_RANDOM) == 0) {
        std::cout << "MADV_RANDOM: Optimized for random access" << std::endl;
    }

    // Tell kernel we'll need this soon
    if (madvise(mapped, size, MADV_WILLNEED) == 0) {
        std::cout << "MADV_WILLNEED: Pre-load into memory" << std::endl;
    }

    // Tell kernel we won't need this anymore
    if (madvise(mapped, size, MADV_DONTNEED) == 0) {
        std::cout << "MADV_DONTNEED: Can free this memory" << std::endl;
    }

    munmap(mapped, size);
    close(fd);
}

void demonstrateMmapOffsets() {
    std::cout << "\n=== Memory Mapping with Offsets ===" << std::endl;

    const size_t file_size = 16384;
    const size_t page_size = sysconf(_SC_PAGESIZE);

    std::cout << "Page size: " << page_size << " bytes" << std::endl;

    int fd = open(TEST_FILE, O_RDWR | O_CREAT | O_TRUNC, 0644);

    if (fd == -1) {
        std::cerr << "Failed to open file" << std::endl;
        return;
    }

    ftruncate(fd, file_size);

    // Write different data at different offsets
    lseek(fd, 0, SEEK_SET);
    write(fd, "Page 0 data", 11);

    lseek(fd, page_size, SEEK_SET);
    write(fd, "Page 1 data", 11);

    lseek(fd, page_size * 2, SEEK_SET);
    write(fd, "Page 2 data", 11);

    // Map second page only
    void* mapped = mmap(nullptr, page_size, PROT_READ | PROT_WRITE,
                       MAP_SHARED, fd, page_size);

    if (mapped == MAP_FAILED) {
        std::cerr << "mmap failed: " << strerror(errno) << std::endl;
        close(fd);
        return;
    }

    std::cout << "Mapped second page (offset " << page_size << ")" << std::endl;

    char* data = static_cast<char*>(mapped);
    std::cout << "Data at offset: " << data << std::endl;

    munmap(mapped, page_size);
    close(fd);
}

void demonstrateMmapResizing() {
    std::cout << "\n=== Memory Mapping Resizing (mremap) ===" << std::endl;

    const size_t initial_size = 4096;
    const size_t new_size = 8192;

    void* mapped = mmap(nullptr, initial_size, PROT_READ | PROT_WRITE,
                       MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);

    if (mapped == MAP_FAILED) {
        std::cerr << "mmap failed" << std::endl;
        return;
    }

    std::cout << "Initial mapping: " << initial_size << " bytes at " << mapped << std::endl;

    char* data = static_cast<char*>(mapped);
    strcpy(data, "Initial data");

#ifdef __linux__
    // mremap is Linux-specific
    void* resized = mremap(mapped, initial_size, new_size, MREMAP_MAYMOVE);

    if (resized == MAP_FAILED) {
        std::cerr << "mremap failed: " << strerror(errno) << std::endl;
        munmap(mapped, initial_size);
        return;
    }

    std::cout << "Resized mapping: " << new_size << " bytes at " << resized << std::endl;

    data = static_cast<char*>(resized);
    std::cout << "Data preserved: " << data << std::endl;

    munmap(resized, new_size);
#else
    std::cout << "mremap not available on this platform" << std::endl;
    munmap(mapped, initial_size);
#endif
}

void demonstrateMmapLocking() {
    std::cout << "\n=== Memory Locking (mlock) ===" << std::endl;

    const size_t size = 4096;

    void* mapped = mmap(nullptr, size, PROT_READ | PROT_WRITE,
                       MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);

    if (mapped == MAP_FAILED) {
        std::cerr << "mmap failed" << std::endl;
        return;
    }

    std::cout << "Memory mapped at: " << mapped << std::endl;

    // Lock memory (prevent swapping)
    if (mlock(mapped, size) == 0) {
        std::cout << "Memory locked (cannot be swapped out)" << std::endl;

        // Use the memory
        char* data = static_cast<char*>(mapped);
        strcpy(data, "Locked memory");

        std::cout << "Data in locked memory: " << data << std::endl;

        // Unlock memory
        if (munlock(mapped, size) == 0) {
            std::cout << "Memory unlocked" << std::endl;
        }
    } else {
        std::cout << "mlock failed: " << strerror(errno) << std::endl;
        std::cout << "Note: May require root privileges or increased limits" << std::endl;
    }

    munmap(mapped, size);
}

int main() {
    std::cout << "Memory Mapped Files Demonstration" << std::endl;
    std::cout << "==================================" << std::endl;

    demonstrateBasicMmap();
    demonstrateMmapProtections();
    demonstrateMmapSharing();
    demonstrateAnonymousMmap();
    demonstrateMmapAdvice();
    demonstrateMmapOffsets();
    demonstrateMmapResizing();
    demonstrateMmapLocking();

    // Clean up
    unlink(TEST_FILE);

    std::cout << "\n=== Memory Mapped Files Complete ===" << std::endl;

    return 0;
}
