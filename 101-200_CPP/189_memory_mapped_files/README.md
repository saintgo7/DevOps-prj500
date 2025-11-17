# Program 189: Memory Mapped Files

## Description
Demonstrates memory-mapped file I/O using mmap, providing efficient file access by mapping files directly into process address space.

## Learning Objectives
- Map files to memory with mmap
- Use memory-mapped I/O for performance
- Implement shared file mappings
- Handle memory mapping errors
- Synchronize mapped memory

## Features
- File mapping with mmap
- Memory access patterns
- Shared vs private mappings
- Memory synchronization (msync)
- Unmapping (munmap)
- Large file handling

## Compilation
```bash
g++ -std=c++17 main.cpp -o memory_mapped_files
./memory_mapped_files
```

## Key Concepts
```cpp
int fd = open("file.txt", O_RDWR);
struct stat sb;
fstat(fd, &sb);

char* mapped = (char*)mmap(NULL, sb.st_size, 
                           PROT_READ | PROT_WRITE,
                           MAP_SHARED, fd, 0);

// Access file as memory
mapped[0] = 'X';

msync(mapped, sb.st_size, MS_SYNC);
munmap(mapped, sb.st_size);
```

## Best Practices
1. Use mmap for large file I/O
2. Handle mapping errors properly
3. Sync memory before unmapping
4. Consider page alignment
5. Profile to ensure performance benefit

## Navigation
- **Previous**: [188 - System Calls](/home/user/DevOps-prj500/101-200_CPP/188_system_calls/README.md)
- **Next**: [190 - POSIX Threads](/home/user/DevOps-prj500/101-200_CPP/190_posix_threads/README.md)
