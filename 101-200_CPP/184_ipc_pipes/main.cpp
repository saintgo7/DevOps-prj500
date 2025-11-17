/*
 * Program 184: IPC Pipes
 * Demonstrates pipes, named pipes (FIFOs), and inter-process communication
 * Compile: g++ -std=c++17 -o ipc_pipes main.cpp
 */

#include <iostream>
#include <string>
#include <cstring>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>

const char* FIFO_PATH = "/tmp/test_fifo";

void demonstrateAnonymousPipe() {
    std::cout << "\n=== Anonymous Pipe Demonstration ===" << std::endl;

    int pipefd[2];

    // Create pipe
    if (pipe(pipefd) == -1) {
        std::cerr << "Pipe creation failed: " << strerror(errno) << std::endl;
        return;
    }

    std::cout << "Pipe created successfully" << std::endl;
    std::cout << "  Read end: fd " << pipefd[0] << std::endl;
    std::cout << "  Write end: fd " << pipefd[1] << std::endl;

    pid_t pid = fork();

    if (pid < 0) {
        std::cerr << "Fork failed" << std::endl;
        close(pipefd[0]);
        close(pipefd[1]);
        return;
    }

    if (pid == 0) {
        // Child process - reads from pipe
        close(pipefd[1]);  // Close write end

        std::cout << "\nChild: Waiting to read from pipe..." << std::endl;

        char buffer[256];
        ssize_t bytes_read = read(pipefd[0], buffer, sizeof(buffer) - 1);

        if (bytes_read > 0) {
            buffer[bytes_read] = '\0';
            std::cout << "Child: Received message: \"" << buffer << "\"" << std::endl;
            std::cout << "Child: Bytes received: " << bytes_read << std::endl;
        }

        close(pipefd[0]);
        exit(0);
    } else {
        // Parent process - writes to pipe
        close(pipefd[0]);  // Close read end

        sleep(1);  // Give child time to set up

        const char* message = "Hello from parent process!";
        std::cout << "\nParent: Writing to pipe: \"" << message << "\"" << std::endl;

        ssize_t bytes_written = write(pipefd[1], message, strlen(message));
        std::cout << "Parent: Bytes written: " << bytes_written << std::endl;

        close(pipefd[1]);

        // Wait for child
        wait(nullptr);
        std::cout << "\nParent: Child process completed" << std::endl;
    }
}

void demonstrateBidirectionalPipe() {
    std::cout << "\n=== Bidirectional Communication (Two Pipes) ===" << std::endl;

    int pipe_parent_to_child[2];
    int pipe_child_to_parent[2];

    if (pipe(pipe_parent_to_child) == -1 || pipe(pipe_child_to_parent) == -1) {
        std::cerr << "Pipe creation failed" << std::endl;
        return;
    }

    pid_t pid = fork();

    if (pid < 0) {
        std::cerr << "Fork failed" << std::endl;
        return;
    }

    if (pid == 0) {
        // Child process
        close(pipe_parent_to_child[1]);  // Close write end of parent->child
        close(pipe_child_to_parent[0]);   // Close read end of child->parent

        // Read from parent
        char buffer[256];
        ssize_t bytes_read = read(pipe_parent_to_child[0], buffer, sizeof(buffer) - 1);

        if (bytes_read > 0) {
            buffer[bytes_read] = '\0';
            std::cout << "Child: Received from parent: \"" << buffer << "\"" << std::endl;
        }

        // Send response to parent
        const char* response = "Message received, this is child's response!";
        write(pipe_child_to_parent[1], response, strlen(response));
        std::cout << "Child: Sent response to parent" << std::endl;

        close(pipe_parent_to_child[0]);
        close(pipe_child_to_parent[1]);
        exit(0);
    } else {
        // Parent process
        close(pipe_parent_to_child[0]);  // Close read end of parent->child
        close(pipe_child_to_parent[1]);   // Close write end of child->parent

        // Send message to child
        const char* message = "Hello child, this is parent!";
        write(pipe_parent_to_child[1], message, strlen(message));
        std::cout << "Parent: Sent message to child" << std::endl;

        // Read response from child
        char buffer[256];
        ssize_t bytes_read = read(pipe_child_to_parent[0], buffer, sizeof(buffer) - 1);

        if (bytes_read > 0) {
            buffer[bytes_read] = '\0';
            std::cout << "Parent: Received from child: \"" << buffer << "\"" << std::endl;
        }

        close(pipe_parent_to_child[1]);
        close(pipe_child_to_parent[0]);

        wait(nullptr);
    }
}

void demonstrateNamedPipe() {
    std::cout << "\n=== Named Pipe (FIFO) Demonstration ===" << std::endl;

    // Remove existing FIFO if it exists
    unlink(FIFO_PATH);

    // Create named pipe
    if (mkfifo(FIFO_PATH, 0666) == -1) {
        std::cerr << "Failed to create FIFO: " << strerror(errno) << std::endl;
        return;
    }

    std::cout << "Named pipe created at: " << FIFO_PATH << std::endl;

    pid_t pid = fork();

    if (pid < 0) {
        std::cerr << "Fork failed" << std::endl;
        unlink(FIFO_PATH);
        return;
    }

    if (pid == 0) {
        // Child process - reader
        std::cout << "Child: Opening FIFO for reading..." << std::endl;

        int fd = open(FIFO_PATH, O_RDONLY);
        if (fd == -1) {
            std::cerr << "Child: Failed to open FIFO" << std::endl;
            exit(1);
        }

        std::cout << "Child: FIFO opened, waiting for data..." << std::endl;

        char buffer[256];
        ssize_t bytes_read = read(fd, buffer, sizeof(buffer) - 1);

        if (bytes_read > 0) {
            buffer[bytes_read] = '\0';
            std::cout << "Child: Received via FIFO: \"" << buffer << "\"" << std::endl;
        }

        close(fd);
        exit(0);
    } else {
        // Parent process - writer
        sleep(1);  // Give child time to open for reading

        std::cout << "Parent: Opening FIFO for writing..." << std::endl;

        int fd = open(FIFO_PATH, O_WRONLY);
        if (fd == -1) {
            std::cerr << "Parent: Failed to open FIFO" << std::endl;
            wait(nullptr);
            unlink(FIFO_PATH);
            return;
        }

        const char* message = "Hello through named pipe!";
        std::cout << "Parent: Writing to FIFO: \"" << message << "\"" << std::endl;

        write(fd, message, strlen(message));

        close(fd);

        wait(nullptr);
        std::cout << "Parent: Communication complete" << std::endl;

        // Clean up
        unlink(FIFO_PATH);
        std::cout << "Named pipe removed" << std::endl;
    }
}

void demonstratePipeCapacity() {
    std::cout << "\n=== Pipe Capacity Demonstration ===" << std::endl;

    int pipefd[2];

    if (pipe(pipefd) == -1) {
        std::cerr << "Pipe creation failed" << std::endl;
        return;
    }

    // Get pipe capacity (Linux-specific)
#ifdef F_GETPIPE_SZ
    long capacity = fcntl(pipefd[0], F_GETPIPE_SZ);
    if (capacity != -1) {
        std::cout << "Default pipe capacity: " << capacity << " bytes" << std::endl;
    }
#else
    std::cout << "Pipe capacity query not supported on this system" << std::endl;
    std::cout << "Default pipe capacity is typically 65536 bytes on Linux" << std::endl;
#endif

    // Set non-blocking mode
    int flags = fcntl(pipefd[1], F_GETFL);
    fcntl(pipefd[1], F_SETFL, flags | O_NONBLOCK);

    // Try to write data to see when it blocks
    std::cout << "\nTesting pipe fill..." << std::endl;

    char data[1024];
    memset(data, 'A', sizeof(data));

    size_t total_written = 0;
    int write_count = 0;

    while (true) {
        ssize_t bytes = write(pipefd[1], data, sizeof(data));

        if (bytes == -1) {
            if (errno == EAGAIN || errno == EWOULDBLOCK) {
                std::cout << "Pipe full after writing " << total_written
                         << " bytes in " << write_count << " writes" << std::endl;
                break;
            } else {
                std::cerr << "Write error: " << strerror(errno) << std::endl;
                break;
            }
        }

        total_written += bytes;
        write_count++;

        // Safety limit
        if (write_count > 100) {
            std::cout << "Safety limit reached" << std::endl;
            break;
        }
    }

    // Read some data
    std::cout << "\nReading data from pipe..." << std::endl;
    char read_buffer[1024];
    ssize_t bytes_read = read(pipefd[0], read_buffer, sizeof(read_buffer));
    std::cout << "Read " << bytes_read << " bytes" << std::endl;

    close(pipefd[0]);
    close(pipefd[1]);
}

void demonstratePipeChain() {
    std::cout << "\n=== Pipe Chain Demonstration (simulating: ls | grep | wc) ===" << std::endl;

    int pipe1[2], pipe2[2];

    if (pipe(pipe1) == -1 || pipe(pipe2) == -1) {
        std::cerr << "Pipe creation failed" << std::endl;
        return;
    }

    // First child: producer
    pid_t pid1 = fork();

    if (pid1 == 0) {
        close(pipe1[0]);  // Close read end

        // Redirect stdout to pipe
        dup2(pipe1[1], STDOUT_FILENO);
        close(pipe1[1]);

        // Close unused pipe2
        close(pipe2[0]);
        close(pipe2[1]);

        // Execute ls
        execlp("ls", "ls", "-l", "/tmp", nullptr);
        std::cerr << "execlp failed" << std::endl;
        exit(1);
    }

    // Second child: filter
    pid_t pid2 = fork();

    if (pid2 == 0) {
        close(pipe1[1]);  // Close write end of pipe1
        close(pipe2[0]);  // Close read end of pipe2

        // Redirect stdin from pipe1
        dup2(pipe1[0], STDIN_FILENO);
        close(pipe1[0]);

        // Redirect stdout to pipe2
        dup2(pipe2[1], STDOUT_FILENO);
        close(pipe2[1]);

        // Execute grep
        execlp("grep", "grep", "test", nullptr);
        std::cerr << "execlp failed" << std::endl;
        exit(1);
    }

    // Parent: reader
    close(pipe1[0]);
    close(pipe1[1]);
    close(pipe2[1]);

    std::cout << "Pipe chain output:" << std::endl;
    std::cout << "-------------------" << std::endl;

    char buffer[256];
    ssize_t bytes_read;

    while ((bytes_read = read(pipe2[0], buffer, sizeof(buffer) - 1)) > 0) {
        buffer[bytes_read] = '\0';
        std::cout << buffer;
    }

    std::cout << "-------------------" << std::endl;

    close(pipe2[0]);

    // Wait for both children
    waitpid(pid1, nullptr, 0);
    waitpid(pid2, nullptr, 0);

    std::cout << "Pipe chain complete" << std::endl;
}

int main() {
    std::cout << "IPC Pipes Demonstration" << std::endl;
    std::cout << "=======================" << std::endl;

    demonstrateAnonymousPipe();
    demonstrateBidirectionalPipe();
    demonstrateNamedPipe();
    demonstratePipeCapacity();
    demonstratePipeChain();

    std::cout << "\n=== IPC Pipes Complete ===" << std::endl;

    return 0;
}
