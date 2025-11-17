/*
 * Program 188: System Calls
 * Demonstrates system call wrappers, error handling, and low-level I/O
 * Compile: g++ -std=c++17 -o system_calls main.cpp
 */

#include <iostream>
#include <cstring>
#include <string>
#include <vector>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/utsname.h>
#include <sys/time.h>
#include <sys/resource.h>
#include <dirent.h>
#include <errno.h>
#include <pwd.h>
#include <grp.h>

const char* TEST_FILE = "/tmp/syscall_test.txt";

// Error handling wrapper
class SystemCallError {
public:
    static void check(int result, const std::string& operation) {
        if (result < 0) {
            std::cerr << "System call failed: " << operation << std::endl;
            std::cerr << "Error: " << strerror(errno) << " (errno: " << errno << ")" << std::endl;
            throw std::runtime_error(operation + " failed");
        }
    }

    static void checkPtr(void* result, const std::string& operation) {
        if (result == nullptr) {
            std::cerr << "System call failed: " << operation << std::endl;
            std::cerr << "Error: " << strerror(errno) << " (errno: " << errno << ")" << std::endl;
            throw std::runtime_error(operation + " failed");
        }
    }
};

void demonstrateFileSystemCalls() {
    std::cout << "\n=== File System Calls ===" << std::endl;

    // open() - Open/create file
    std::cout << "\n1. open() - Creating file" << std::endl;
    int fd = open(TEST_FILE, O_CREAT | O_WRONLY | O_TRUNC, 0644);
    SystemCallError::check(fd, "open");
    std::cout << "File descriptor: " << fd << std::endl;

    // write() - Write data
    std::cout << "\n2. write() - Writing data" << std::endl;
    const char* data = "Hello from write() system call!\n";
    ssize_t bytes_written = write(fd, data, strlen(data));
    SystemCallError::check(bytes_written, "write");
    std::cout << "Bytes written: " << bytes_written << std::endl;

    // close() - Close file
    std::cout << "\n3. close() - Closing file" << std::endl;
    int result = close(fd);
    SystemCallError::check(result, "close");
    std::cout << "File closed" << std::endl;

    // open() for reading
    std::cout << "\n4. open() - Opening for reading" << std::endl;
    fd = open(TEST_FILE, O_RDONLY);
    SystemCallError::check(fd, "open");

    // read() - Read data
    std::cout << "\n5. read() - Reading data" << std::endl;
    char buffer[256] = {0};
    ssize_t bytes_read = read(fd, buffer, sizeof(buffer) - 1);
    SystemCallError::check(bytes_read, "read");
    std::cout << "Bytes read: " << bytes_read << std::endl;
    std::cout << "Content: " << buffer << std::endl;

    // lseek() - Seek to position
    std::cout << "\n6. lseek() - Seeking to beginning" << std::endl;
    off_t offset = lseek(fd, 0, SEEK_SET);
    SystemCallError::check(offset, "lseek");
    std::cout << "Current position: " << offset << std::endl;

    close(fd);

    // stat() - Get file information
    std::cout << "\n7. stat() - Getting file information" << std::endl;
    struct stat file_stat;
    result = stat(TEST_FILE, &file_stat);
    SystemCallError::check(result, "stat");

    std::cout << "File information:" << std::endl;
    std::cout << "  Size: " << file_stat.st_size << " bytes" << std::endl;
    std::cout << "  Mode: " << std::oct << (file_stat.st_mode & 0777) << std::dec << std::endl;
    std::cout << "  Links: " << file_stat.st_nlink << std::endl;
    std::cout << "  UID: " << file_stat.st_uid << std::endl;
    std::cout << "  GID: " << file_stat.st_gid << std::endl;

    // access() - Check file access
    std::cout << "\n8. access() - Checking file access" << std::endl;
    if (access(TEST_FILE, R_OK) == 0) {
        std::cout << "File is readable" << std::endl;
    }
    if (access(TEST_FILE, W_OK) == 0) {
        std::cout << "File is writable" << std::endl;
    }
    if (access(TEST_FILE, X_OK) == 0) {
        std::cout << "File is executable" << std::endl;
    }

    // chmod() - Change permissions
    std::cout << "\n9. chmod() - Changing permissions to 0755" << std::endl;
    result = chmod(TEST_FILE, 0755);
    SystemCallError::check(result, "chmod");
    std::cout << "Permissions changed" << std::endl;

    // Verify change
    stat(TEST_FILE, &file_stat);
    std::cout << "New mode: " << std::oct << (file_stat.st_mode & 0777) << std::dec << std::endl;

    // unlink() - Delete file
    std::cout << "\n10. unlink() - Deleting file" << std::endl;
    result = unlink(TEST_FILE);
    SystemCallError::check(result, "unlink");
    std::cout << "File deleted" << std::endl;
}

void demonstrateDirectoryCalls() {
    std::cout << "\n=== Directory System Calls ===" << std::endl;

    const char* test_dir = "/tmp/syscall_test_dir";

    // mkdir() - Create directory
    std::cout << "\n1. mkdir() - Creating directory" << std::endl;
    int result = mkdir(test_dir, 0755);
    if (result < 0 && errno != EEXIST) {
        SystemCallError::check(result, "mkdir");
    }
    std::cout << "Directory created: " << test_dir << std::endl;

    // getcwd() - Get current working directory
    std::cout << "\n2. getcwd() - Getting current directory" << std::endl;
    char cwd[1024];
    if (getcwd(cwd, sizeof(cwd)) != nullptr) {
        std::cout << "Current directory: " << cwd << std::endl;
    }

    // chdir() - Change directory
    std::cout << "\n3. chdir() - Changing to test directory" << std::endl;
    result = chdir(test_dir);
    SystemCallError::check(result, "chdir");

    if (getcwd(cwd, sizeof(cwd)) != nullptr) {
        std::cout << "New current directory: " << cwd << std::endl;
    }

    // Return to original directory
    chdir("/tmp");

    // opendir(), readdir(), closedir() - Read directory
    std::cout << "\n4. opendir/readdir/closedir - Reading directory" << std::endl;
    DIR* dir = opendir("/tmp");
    SystemCallError::checkPtr(dir, "opendir");

    std::cout << "First 10 entries in /tmp:" << std::endl;
    int count = 0;
    struct dirent* entry;

    while ((entry = readdir(dir)) != nullptr && count < 10) {
        std::cout << "  " << entry->d_name;

        // Check type
        if (entry->d_type == DT_DIR) {
            std::cout << " (directory)";
        } else if (entry->d_type == DT_REG) {
            std::cout << " (file)";
        } else if (entry->d_type == DT_LNK) {
            std::cout << " (symlink)";
        }

        std::cout << std::endl;
        count++;
    }

    closedir(dir);

    // rmdir() - Remove directory
    std::cout << "\n5. rmdir() - Removing test directory" << std::endl;
    result = rmdir(test_dir);
    SystemCallError::check(result, "rmdir");
    std::cout << "Directory removed" << std::endl;
}

void demonstrateProcessCalls() {
    std::cout << "\n=== Process System Calls ===" << std::endl;

    // getpid(), getppid()
    std::cout << "\n1. getpid/getppid - Process IDs" << std::endl;
    std::cout << "Process ID: " << getpid() << std::endl;
    std::cout << "Parent Process ID: " << getppid() << std::endl;

    // getuid(), geteuid()
    std::cout << "\n2. getuid/geteuid - User IDs" << std::endl;
    std::cout << "Real User ID: " << getuid() << std::endl;
    std::cout << "Effective User ID: " << geteuid() << std::endl;

    // getgid(), getegid()
    std::cout << "\n3. getgid/getegid - Group IDs" << std::endl;
    std::cout << "Real Group ID: " << getgid() << std::endl;
    std::cout << "Effective Group ID: " << getegid() << std::endl;

    // getpwuid() - Get password entry
    std::cout << "\n4. getpwuid - User information" << std::endl;
    struct passwd* pw = getpwuid(getuid());
    if (pw != nullptr) {
        std::cout << "Username: " << pw->pw_name << std::endl;
        std::cout << "Home directory: " << pw->pw_dir << std::endl;
        std::cout << "Shell: " << pw->pw_shell << std::endl;
    }

    // getgrgid() - Get group entry
    std::cout << "\n5. getgrgid - Group information" << std::endl;
    struct group* gr = getgrgid(getgid());
    if (gr != nullptr) {
        std::cout << "Group name: " << gr->gr_name << std::endl;
    }
}

void demonstrateSystemInfo() {
    std::cout << "\n=== System Information Calls ===" << std::endl;

    // uname() - Get system information
    std::cout << "\n1. uname() - System information" << std::endl;
    struct utsname sys_info;
    int result = uname(&sys_info);
    SystemCallError::check(result, "uname");

    std::cout << "System Name: " << sys_info.sysname << std::endl;
    std::cout << "Node Name: " << sys_info.nodename << std::endl;
    std::cout << "Release: " << sys_info.release << std::endl;
    std::cout << "Version: " << sys_info.version << std::endl;
    std::cout << "Machine: " << sys_info.machine << std::endl;

    // sysconf() - Get system configuration
    std::cout << "\n2. sysconf() - System configuration" << std::endl;
    long page_size = sysconf(_SC_PAGESIZE);
    long processors = sysconf(_SC_NPROCESSORS_ONLN);
    long max_open_files = sysconf(_SC_OPEN_MAX);

    std::cout << "Page size: " << page_size << " bytes" << std::endl;
    std::cout << "Number of processors: " << processors << std::endl;
    std::cout << "Max open files: " << max_open_files << std::endl;
}

void demonstrateTimeCalls() {
    std::cout << "\n=== Time System Calls ===" << std::endl;

    // time() - Get current time
    std::cout << "\n1. time() - Current time" << std::endl;
    time_t current_time = time(nullptr);
    std::cout << "Unix timestamp: " << current_time << std::endl;
    std::cout << "Readable time: " << ctime(&current_time);

    // gettimeofday() - Get time with microsecond precision
    std::cout << "\n2. gettimeofday() - High precision time" << std::endl;
    struct timeval tv;
    int result = gettimeofday(&tv, nullptr);
    SystemCallError::check(result, "gettimeofday");

    std::cout << "Seconds: " << tv.tv_sec << std::endl;
    std::cout << "Microseconds: " << tv.tv_usec << std::endl;

    // clock_gettime() - Get monotonic time
    std::cout << "\n3. clock_gettime() - Monotonic time" << std::endl;
    struct timespec ts;
    result = clock_gettime(CLOCK_MONOTONIC, &ts);
    SystemCallError::check(result, "clock_gettime");

    std::cout << "Seconds: " << ts.tv_sec << std::endl;
    std::cout << "Nanoseconds: " << ts.tv_nsec << std::endl;
}

void demonstrateResourceCalls() {
    std::cout << "\n=== Resource System Calls ===" << std::endl;

    // getrusage() - Get resource usage
    std::cout << "\n1. getrusage() - Resource usage" << std::endl;
    struct rusage usage;
    int result = getrusage(RUSAGE_SELF, &usage);
    SystemCallError::check(result, "getrusage");

    std::cout << "User CPU time: " << usage.ru_utime.tv_sec << "."
              << usage.ru_utime.tv_usec << " seconds" << std::endl;
    std::cout << "System CPU time: " << usage.ru_stime.tv_sec << "."
              << usage.ru_stime.tv_usec << " seconds" << std::endl;
    std::cout << "Max RSS: " << usage.ru_maxrss << " KB" << std::endl;
    std::cout << "Page faults (minor): " << usage.ru_minflt << std::endl;
    std::cout << "Page faults (major): " << usage.ru_majflt << std::endl;
    std::cout << "Block input operations: " << usage.ru_inblock << std::endl;
    std::cout << "Block output operations: " << usage.ru_oublock << std::endl;
    std::cout << "Voluntary context switches: " << usage.ru_nvcsw << std::endl;
    std::cout << "Involuntary context switches: " << usage.ru_nivcsw << std::endl;

    // getrlimit() - Get resource limits
    std::cout << "\n2. getrlimit() - Resource limits" << std::endl;
    struct rlimit limit;

    result = getrlimit(RLIMIT_NOFILE, &limit);
    SystemCallError::check(result, "getrlimit");

    std::cout << "Open files limit:" << std::endl;
    std::cout << "  Soft: " << limit.rlim_cur << std::endl;
    std::cout << "  Hard: " << limit.rlim_max << std::endl;

    result = getrlimit(RLIMIT_STACK, &limit);
    SystemCallError::check(result, "getrlimit");

    std::cout << "Stack size limit:" << std::endl;
    std::cout << "  Soft: " << limit.rlim_cur << " bytes" << std::endl;
    std::cout << "  Hard: " << (limit.rlim_max == RLIM_INFINITY ? "unlimited" :
                               std::to_string(limit.rlim_max) + " bytes") << std::endl;
}

void demonstrateLinkCalls() {
    std::cout << "\n=== Link System Calls ===" << std::endl;

    const char* original = "/tmp/original.txt";
    const char* hardlink = "/tmp/hardlink.txt";
    const char* symlink_path = "/tmp/symlink.txt";

    // Create original file
    int fd = open(original, O_CREAT | O_WRONLY | O_TRUNC, 0644);
    if (fd >= 0) {
        write(fd, "Test data\n", 10);
        close(fd);
    }

    // link() - Create hard link
    std::cout << "\n1. link() - Creating hard link" << std::endl;
    unlink(hardlink);  // Remove if exists
    int result = link(original, hardlink);
    SystemCallError::check(result, "link");
    std::cout << "Hard link created: " << hardlink << std::endl;

    // symlink() - Create symbolic link
    std::cout << "\n2. symlink() - Creating symbolic link" << std::endl;
    unlink(symlink_path);  // Remove if exists
    result = symlink(original, symlink_path);
    SystemCallError::check(result, "symlink");
    std::cout << "Symbolic link created: " << symlink_path << std::endl;

    // readlink() - Read symbolic link
    std::cout << "\n3. readlink() - Reading symbolic link" << std::endl;
    char link_target[256];
    ssize_t len = readlink(symlink_path, link_target, sizeof(link_target) - 1);
    if (len >= 0) {
        link_target[len] = '\0';
        std::cout << "Symlink points to: " << link_target << std::endl;
    }

    // Clean up
    unlink(original);
    unlink(hardlink);
    unlink(symlink_path);
}

int main() {
    std::cout << "System Calls Demonstration" << std::endl;
    std::cout << "==========================" << std::endl;

    try {
        demonstrateFileSystemCalls();
        demonstrateDirectoryCalls();
        demonstrateProcessCalls();
        demonstrateSystemInfo();
        demonstrateTimeCalls();
        demonstrateResourceCalls();
        demonstrateLinkCalls();

    } catch (const std::exception& e) {
        std::cerr << "Exception: " << e.what() << std::endl;
        return 1;
    }

    std::cout << "\n=== System Calls Complete ===" << std::endl;

    return 0;
}
