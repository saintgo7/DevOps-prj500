/*
 * Program 192: Asynchronous I/O
 * Demonstrates asynchronous I/O operations using POSIX AIO
 * Compile: g++ -std=c++17 -lrt -o async_io main.cpp
 */

#include <iostream>
#include <cstring>
#include <vector>
#include <aio.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <signal.h>
#include <sys/stat.h>
#include <chrono>
#include <thread>

const char* TEST_FILE = "/tmp/async_io_test.dat";
const size_t BUFFER_SIZE = 4096;

// Signal handler for AIO completion
volatile sig_atomic_t aio_complete = 0;

void aio_completion_handler(int signo, siginfo_t* info, void* context) {
    aio_complete = 1;
    std::cout << "AIO completion signal received" << std::endl;
}

void demonstrateAsyncRead() {
    std::cout << "\n=== Asynchronous Read ===" << std::endl;

    // Create and populate test file
    int fd = open(TEST_FILE, O_RDWR | O_CREAT | O_TRUNC, 0644);
    if (fd == -1) {
        std::cerr << "Failed to create file" << std::endl;
        return;
    }

    const char* data = "Hello from asynchronous I/O! This is test data for async read.";
    write(fd, data, strlen(data));
    close(fd);

    std::cout << "Test file created with data" << std::endl;

    // Open for async read
    fd = open(TEST_FILE, O_RDONLY);
    if (fd == -1) {
        std::cerr << "Failed to open file" << std::endl;
        return;
    }

    // Prepare buffer
    char* buffer = new char[BUFFER_SIZE];
    memset(buffer, 0, BUFFER_SIZE);

    // Set up AIO control block
    struct aiocb cb;
    memset(&cb, 0, sizeof(struct aiocb));

    cb.aio_fildes = fd;
    cb.aio_buf = buffer;
    cb.aio_nbytes = BUFFER_SIZE;
    cb.aio_offset = 0;

    std::cout << "Initiating asynchronous read..." << std::endl;

    // Start async read
    if (aio_read(&cb) == -1) {
        std::cerr << "aio_read failed: " << strerror(errno) << std::endl;
        close(fd);
        delete[] buffer;
        return;
    }

    std::cout << "Async read started, continuing with other work..." << std::endl;

    // Do other work while read is in progress
    for (int i = 0; i < 3; ++i) {
        std::cout << "Doing other work... " << i << std::endl;
        usleep(100000);
    }

    // Wait for completion
    std::cout << "Waiting for async read to complete..." << std::endl;

    while (aio_error(&cb) == EINPROGRESS) {
        std::cout << "." << std::flush;
        usleep(100000);
    }
    std::cout << std::endl;

    // Check result
    int ret = aio_return(&cb);
    if (ret > 0) {
        std::cout << "Read " << ret << " bytes" << std::endl;
        std::cout << "Data: " << buffer << std::endl;
    } else {
        std::cerr << "Read failed" << std::endl;
    }

    close(fd);
    delete[] buffer;
}

void demonstrateAsyncWrite() {
    std::cout << "\n=== Asynchronous Write ===" << std::endl;

    int fd = open(TEST_FILE, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd == -1) {
        std::cerr << "Failed to create file" << std::endl;
        return;
    }

    // Prepare data to write
    const char* data = "This data is written asynchronously!";
    char* buffer = new char[strlen(data) + 1];
    strcpy(buffer, data);

    // Set up AIO control block
    struct aiocb cb;
    memset(&cb, 0, sizeof(struct aiocb));

    cb.aio_fildes = fd;
    cb.aio_buf = buffer;
    cb.aio_nbytes = strlen(data);
    cb.aio_offset = 0;

    std::cout << "Initiating asynchronous write..." << std::endl;

    // Start async write
    if (aio_write(&cb) == -1) {
        std::cerr << "aio_write failed: " << strerror(errno) << std::endl;
        close(fd);
        delete[] buffer;
        return;
    }

    std::cout << "Async write started, continuing with other work..." << std::endl;

    // Do other work
    for (int i = 0; i < 3; ++i) {
        std::cout << "Doing other work... " << i << std::endl;
        usleep(100000);
    }

    // Wait for completion
    std::cout << "Waiting for async write to complete..." << std::endl;

    while (aio_error(&cb) == EINPROGRESS) {
        std::cout << "." << std::flush;
        usleep(100000);
    }
    std::cout << std::endl;

    // Check result
    int ret = aio_return(&cb);
    if (ret > 0) {
        std::cout << "Wrote " << ret << " bytes asynchronously" << std::endl;
    } else {
        std::cerr << "Write failed" << std::endl;
    }

    close(fd);
    delete[] buffer;

    // Verify write
    fd = open(TEST_FILE, O_RDONLY);
    char verify_buffer[256] = {0};
    read(fd, verify_buffer, sizeof(verify_buffer) - 1);
    close(fd);

    std::cout << "Verified data: " << verify_buffer << std::endl;
}

void demonstrateAsyncWithSignal() {
    std::cout << "\n=== Asynchronous I/O with Signal Notification ===" << std::endl;

    // Set up signal handler
    struct sigaction sa;
    sa.sa_flags = SA_SIGINFO;
    sa.sa_sigaction = aio_completion_handler;
    sigemptyset(&sa.sa_mask);

    if (sigaction(SIGIO, &sa, nullptr) == -1) {
        std::cerr << "Failed to set up signal handler" << std::endl;
        return;
    }

    int fd = open(TEST_FILE, O_RDONLY);
    if (fd == -1) {
        std::cerr << "Failed to open file" << std::endl;
        return;
    }

    char* buffer = new char[BUFFER_SIZE];
    memset(buffer, 0, BUFFER_SIZE);

    // Set up AIO with signal notification
    struct aiocb cb;
    memset(&cb, 0, sizeof(struct aiocb));

    cb.aio_fildes = fd;
    cb.aio_buf = buffer;
    cb.aio_nbytes = BUFFER_SIZE;
    cb.aio_offset = 0;
    cb.aio_sigevent.sigev_notify = SIGEV_SIGNAL;
    cb.aio_sigevent.sigev_signo = SIGIO;

    std::cout << "Starting async read with signal notification..." << std::endl;

    aio_complete = 0;

    if (aio_read(&cb) == -1) {
        std::cerr << "aio_read failed" << std::endl;
        close(fd);
        delete[] buffer;
        return;
    }

    // Wait for signal
    std::cout << "Waiting for completion signal..." << std::endl;

    int timeout = 0;
    while (!aio_complete && timeout < 20) {
        std::cout << "." << std::flush;
        usleep(100000);
        timeout++;
    }
    std::cout << std::endl;

    if (aio_complete) {
        int ret = aio_return(&cb);
        if (ret > 0) {
            std::cout << "Signal received, read " << ret << " bytes" << std::endl;
        }
    } else {
        std::cout << "Timeout waiting for signal" << std::endl;
    }

    close(fd);
    delete[] buffer;
}

void demonstrateMultipleAsyncOps() {
    std::cout << "\n=== Multiple Asynchronous Operations ===" << std::endl;

    const int NUM_OPS = 3;
    const char* files[] = {
        "/tmp/async_file_0.dat",
        "/tmp/async_file_1.dat",
        "/tmp/async_file_2.dat"
    };

    // Create test files
    for (int i = 0; i < NUM_OPS; ++i) {
        int fd = open(files[i], O_WRONLY | O_CREAT | O_TRUNC, 0644);
        if (fd != -1) {
            char data[64];
            snprintf(data, sizeof(data), "Data for file %d", i);
            write(fd, data, strlen(data));
            close(fd);
        }
    }

    std::cout << "Created " << NUM_OPS << " test files" << std::endl;

    // Set up multiple async reads
    struct aiocb cbs[NUM_OPS];
    char* buffers[NUM_OPS];

    for (int i = 0; i < NUM_OPS; ++i) {
        buffers[i] = new char[256];
        memset(buffers[i], 0, 256);

        memset(&cbs[i], 0, sizeof(struct aiocb));

        cbs[i].aio_fildes = open(files[i], O_RDONLY);
        cbs[i].aio_buf = buffers[i];
        cbs[i].aio_nbytes = 256;
        cbs[i].aio_offset = 0;
    }

    std::cout << "Starting " << NUM_OPS << " async reads..." << std::endl;

    // Start all async reads
    for (int i = 0; i < NUM_OPS; ++i) {
        if (aio_read(&cbs[i]) == -1) {
            std::cerr << "Failed to start async read " << i << std::endl;
        }
    }

    // Create list for aio_suspend
    const struct aiocb* cb_list[NUM_OPS];
    for (int i = 0; i < NUM_OPS; ++i) {
        cb_list[i] = &cbs[i];
    }

    std::cout << "Waiting for all operations to complete..." << std::endl;

    // Wait for all operations
    struct timespec timeout;
    timeout.tv_sec = 5;
    timeout.tv_nsec = 0;

    while (true) {
        int incomplete = 0;

        for (int i = 0; i < NUM_OPS; ++i) {
            if (aio_error(&cbs[i]) == EINPROGRESS) {
                incomplete++;
            }
        }

        if (incomplete == 0) break;

        std::cout << "Still waiting for " << incomplete << " operations..." << std::endl;
        aio_suspend(cb_list, NUM_OPS, &timeout);
    }

    std::cout << "All operations complete!" << std::endl;

    // Check results
    for (int i = 0; i < NUM_OPS; ++i) {
        int ret = aio_return(&cbs[i]);
        if (ret > 0) {
            std::cout << "File " << i << ": " << buffers[i] << std::endl;
        }

        close(cbs[i].aio_fildes);
        delete[] buffers[i];
        unlink(files[i]);
    }
}

void demonstrateListIO() {
    std::cout << "\n=== List I/O (lio_listio) ===" << std::endl;

    const int NUM_OPS = 3;
    struct aiocb* cb_list[NUM_OPS];
    char* buffers[NUM_OPS];

    // Prepare operations
    for (int i = 0; i < NUM_OPS; ++i) {
        buffers[i] = new char[64];

        cb_list[i] = new struct aiocb;
        memset(cb_list[i], 0, sizeof(struct aiocb));

        if (i < 2) {
            // Write operations
            snprintf(buffers[i], 64, "List I/O write %d", i);

            cb_list[i]->aio_fildes = open(TEST_FILE, O_WRONLY | O_CREAT | O_TRUNC, 0644);
            cb_list[i]->aio_buf = buffers[i];
            cb_list[i]->aio_nbytes = strlen(buffers[i]);
            cb_list[i]->aio_offset = i * 64;
            cb_list[i]->aio_lio_opcode = LIO_WRITE;
        } else {
            // No operation
            cb_list[i]->aio_lio_opcode = LIO_NOP;
        }
    }

    std::cout << "Submitting list I/O operations..." << std::endl;

    // Submit all operations at once
    if (lio_listio(LIO_WAIT, cb_list, NUM_OPS, nullptr) == -1) {
        std::cerr << "lio_listio failed: " << strerror(errno) << std::endl;
    } else {
        std::cout << "All list I/O operations completed" << std::endl;
    }

    // Clean up
    for (int i = 0; i < NUM_OPS; ++i) {
        if (cb_list[i]->aio_fildes > 0) {
            close(cb_list[i]->aio_fildes);
        }
        delete cb_list[i];
        delete[] buffers[i];
    }
}

void demonstrateAsyncCancel() {
    std::cout << "\n=== Asynchronous Operation Cancellation ===" << std::endl;

    int fd = open(TEST_FILE, O_RDONLY);
    if (fd == -1) {
        std::cerr << "Failed to open file" << std::endl;
        return;
    }

    char* buffer = new char[BUFFER_SIZE];
    memset(buffer, 0, BUFFER_SIZE);

    struct aiocb cb;
    memset(&cb, 0, sizeof(struct aiocb));

    cb.aio_fildes = fd;
    cb.aio_buf = buffer;
    cb.aio_nbytes = BUFFER_SIZE;
    cb.aio_offset = 0;

    std::cout << "Starting async read..." << std::endl;

    if (aio_read(&cb) == -1) {
        std::cerr << "aio_read failed" << std::endl;
        close(fd);
        delete[] buffer;
        return;
    }

    // Try to cancel
    std::cout << "Attempting to cancel operation..." << std::endl;

    int cancel_result = aio_cancel(fd, &cb);

    switch (cancel_result) {
        case AIO_CANCELED:
            std::cout << "Operation canceled successfully" << std::endl;
            break;
        case AIO_NOTCANCELED:
            std::cout << "Operation could not be canceled (already in progress)" << std::endl;
            break;
        case AIO_ALLDONE:
            std::cout << "Operation already completed" << std::endl;
            break;
        default:
            std::cout << "aio_cancel failed" << std::endl;
    }

    // Wait for any remaining operation
    while (aio_error(&cb) == EINPROGRESS) {
        usleep(10000);
    }

    close(fd);
    delete[] buffer;
}

void demonstrateSyncModes() {
    std::cout << "\n=== Synchronization Modes ===" << std::endl;

    std::cout << "\n1. LIO_WAIT (synchronous):" << std::endl;
    std::cout << "   - Blocks until all operations complete" << std::endl;
    std::cout << "   - Simple to use" << std::endl;

    std::cout << "\n2. LIO_NOWAIT (asynchronous):" << std::endl;
    std::cout << "   - Returns immediately" << std::endl;
    std::cout << "   - Check status with aio_error()" << std::endl;
    std::cout << "   - Use aio_suspend() to wait" << std::endl;

    std::cout << "\n3. Signal notification:" << std::endl;
    std::cout << "   - Get notified via signal when complete" << std::endl;
    std::cout << "   - Set up with aio_sigevent" << std::endl;
}

int main() {
    std::cout << "Asynchronous I/O Demonstration" << std::endl;
    std::cout << "===============================" << std::endl;

    demonstrateSyncModes();
    demonstrateAsyncRead();
    demonstrateAsyncWrite();
    demonstrateAsyncWithSignal();
    demonstrateMultipleAsyncOps();
    demonstrateListIO();
    demonstrateAsyncCancel();

    // Clean up
    unlink(TEST_FILE);

    std::cout << "\n=== Asynchronous I/O Complete ===" << std::endl;

    return 0;
}
