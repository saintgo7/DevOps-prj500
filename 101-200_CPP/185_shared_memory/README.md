# Program 185: Shared Memory

## Description
Demonstrates shared memory for fast inter-process communication, using POSIX shared memory API for data sharing between unrelated processes.

## Learning Objectives
- Create shared memory segments
- Map shared memory into process space
- Implement synchronization with semaphores
- Handle shared memory lifecycle
- Use memory-mapped files

## Features
- shm_open for creating shared memory
- mmap for mapping memory
- Shared memory synchronization
- Memory-mapped files
- Shared memory cleanup

## Compilation
```bash
g++ -std=c++17 main.cpp -o shared_memory -lrt
./shared_memory
```

## Key Concepts
```cpp
// Create shared memory
int shm_fd = shm_open("/myshm", O_CREAT | O_RDWR, 0666);
ftruncate(shm_fd, SIZE);

// Map to address space
void* ptr = mmap(0, SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);

// Access as normal memory
strcpy((char*)ptr, "Hello");

// Cleanup
munmap(ptr, SIZE);
shm_unlink("/myshm");
```

## Best Practices
1. Synchronize access with semaphores/mutexes
2. Clean up shared memory properly
3. Handle memory mapping errors
4. Use appropriate permissions
5. Consider cache coherency

## Navigation
- **Previous**: [184 - IPC Pipes](/home/user/DevOps-prj500/101-200_CPP/184_ipc_pipes/README.md)
- **Next**: [186 - Signal Handling](/home/user/DevOps-prj500/101-200_CPP/186_signal_handling/README.md)
