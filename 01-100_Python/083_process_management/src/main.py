#!/usr/bin/env python3
"""
Program 83: Process Management
Demonstrates process creation, monitoring, and control.
"""

import os
import sys
import time
import psutil
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ProcessInfo:
    """Store process information."""
    pid: int
    name: str
    status: str
    cpu_percent: float
    memory_mb: float
    create_time: str
    num_threads: int


def get_current_process_info() -> ProcessInfo:
    """Get information about current process."""
    process = psutil.Process()

    return ProcessInfo(
        pid=process.pid,
        name=process.name(),
        status=process.status(),
        cpu_percent=process.cpu_percent(interval=0.1),
        memory_mb=process.memory_info().rss / 1024 / 1024,
        create_time=datetime.fromtimestamp(process.create_time()).strftime('%H:%M:%S'),
        num_threads=process.num_threads()
    )


def demonstrate_process_info() -> None:
    """Demonstrate getting process information."""
    print("\n" + "=" * 60)
    print("CURRENT PROCESS INFORMATION")
    print("=" * 60)

    info = get_current_process_info()

    print(f"\n1. Process Details:")
    print(f"   PID: {info.pid}")
    print(f"   Name: {info.name}")
    print(f"   Status: {info.status}")
    print(f"   CPU: {info.cpu_percent:.2f}%")
    print(f"   Memory: {info.memory_mb:.2f} MB")
    print(f"   Created: {info.create_time}")
    print(f"   Threads: {info.num_threads}")

    # Parent process
    current = psutil.Process()
    if current.parent():
        parent = current.parent()
        print(f"\n2. Parent Process:")
        print(f"   PID: {parent.pid}")
        print(f"   Name: {parent.name()}")

    # Environment
    print(f"\n3. Environment Variables (sample):")
    env_vars = ['PATH', 'HOME', 'USER', 'SHELL']
    for var in env_vars:
        value = os.environ.get(var, 'Not set')
        if var == 'PATH':
            value = value[:50] + '...' if len(value) > 50 else value
        print(f"   {var}: {value}")


def demonstrate_process_creation() -> None:
    """Demonstrate process creation concepts."""
    print("\n" + "=" * 60)
    print("PROCESS CREATION CONCEPTS")
    print("=" * 60)

    print("\n1. Current Process ID (PID):")
    print(f"   PID: {os.getpid()}")
    print(f"   Parent PID: {os.getppid()}")

    print("\n2. Process Groups:")
    print(f"   Process Group ID: {os.getpgrp()}")

    print("\n3. User/Group IDs:")
    print(f"   User ID: {os.getuid()}")
    print(f"   Effective User ID: {os.geteuid()}")
    print(f"   Group ID: {os.getgid()}")
    print(f"   Effective Group ID: {os.getegid()}")

    print("\n4. Working Directory:")
    print(f"   CWD: {os.getcwd()}")


def list_running_processes(limit: int = 10) -> List[ProcessInfo]:
    """List running processes sorted by CPU usage."""
    processes = []

    for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_info', 'create_time', 'num_threads']):
        try:
            info = ProcessInfo(
                pid=proc.info['pid'],
                name=proc.info['name'],
                status=proc.info['status'],
                cpu_percent=proc.info['cpu_percent'] or 0,
                memory_mb=proc.info['memory_info'].rss / 1024 / 1024,
                create_time=datetime.fromtimestamp(proc.info['create_time']).strftime('%H:%M:%S'),
                num_threads=proc.info['num_threads']
            )
            processes.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # Sort by CPU usage
    processes.sort(key=lambda x: x.cpu_percent, reverse=True)
    return processes[:limit]


def demonstrate_process_listing() -> None:
    """Demonstrate listing and monitoring processes."""
    print("\n" + "=" * 60)
    print("PROCESS LISTING")
    print("=" * 60)

    processes = list_running_processes(10)

    print(f"\nTop 10 processes by CPU usage:")
    print(f"{'PID':<8} {'Name':<20} {'CPU%':<8} {'Memory(MB)':<12} {'Status'}")
    print("-" * 60)

    for proc in processes:
        print(f"{proc.pid:<8} {proc.name[:19]:<20} {proc.cpu_percent:<8.2f} {proc.memory_mb:<12.2f} {proc.status}")


def demonstrate_system_info() -> None:
    """Demonstrate system-level process information."""
    print("\n" + "=" * 60)
    print("SYSTEM PROCESS INFORMATION")
    print("=" * 60)

    # Process count
    proc_count = len(psutil.pids())
    print(f"\n1. Total Processes: {proc_count}")

    # Process states
    states = {}
    for proc in psutil.process_iter(['status']):
        try:
            status = proc.info['status']
            states[status] = states.get(status, 0) + 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    print(f"\n2. Processes by State:")
    for state, count in sorted(states.items()):
        print(f"   {state}: {count}")

    # CPU times
    cpu_times = psutil.cpu_times()
    print(f"\n3. CPU Times:")
    print(f"   User: {cpu_times.user:.2f}s")
    print(f"   System: {cpu_times.system:.2f}s")
    print(f"   Idle: {cpu_times.idle:.2f}s")


def demonstrate_process_control() -> None:
    """Demonstrate process control concepts."""
    print("\n" + "=" * 60)
    print("PROCESS CONTROL")
    print("=" * 60)

    current = psutil.Process()

    print("\n1. Process Priority:")
    try:
        nice = current.nice()
        print(f"   Nice value: {nice}")
        print("   (Lower values = higher priority)")
    except psutil.AccessDenied:
        print("   Access denied to get nice value")

    print("\n2. Process Status:")
    print(f"   Status: {current.status()}")
    print(f"   Running: {current.is_running()}")

    print("\n3. Process Threads:")
    threads = current.threads()
    print(f"   Number of threads: {len(threads)}")

    print("\n4. Process Connections:")
    try:
        connections = current.connections()
        print(f"   Open connections: {len(connections)}")
    except psutil.AccessDenied:
        print("   Access denied to list connections")


def demonstrate_resource_limits() -> None:
    """Demonstrate process resource limits."""
    print("\n" + "=" * 60)
    print("PROCESS RESOURCE LIMITS")
    print("=" * 60)

    current = psutil.Process()

    # Memory limits
    try:
        rlimits = current.rlimit(psutil.RLIMIT_AS)
        soft, hard = rlimits
        print(f"\n1. Virtual Memory Limit:")
        print(f"   Soft: {'Unlimited' if soft == psutil.RLIM_INFINITY else f'{soft / 1024 / 1024:.0f} MB'}")
        print(f"   Hard: {'Unlimited' if hard == psutil.RLIM_INFINITY else f'{hard / 1024 / 1024:.0f} MB'}")
    except (AttributeError, psutil.AccessDenied):
        print("\n1. Resource limits not available on this platform")

    # File descriptors
    try:
        num_fds = current.num_fds()
        print(f"\n2. Open File Descriptors: {num_fds}")
    except (AttributeError, psutil.AccessDenied):
        open_files = current.open_files()
        print(f"\n2. Open Files: {len(open_files)}")

    # Context switches
    try:
        ctx_switches = current.num_ctx_switches()
        print(f"\n3. Context Switches:")
        print(f"   Voluntary: {ctx_switches.voluntary}")
        print(f"   Involuntary: {ctx_switches.involuntary}")
    except (AttributeError, psutil.AccessDenied):
        print("\n3. Context switches not available")


def monitor_process(duration: int = 3) -> None:
    """Monitor current process for a duration."""
    print("\n" + "=" * 60)
    print("PROCESS MONITORING")
    print("=" * 60)

    print(f"\nMonitoring current process for {duration} seconds...")
    print(f"{'Time':<8} {'CPU%':<8} {'Memory(MB)':<12} {'Threads'}")
    print("-" * 40)

    current = psutil.Process()
    start_time = time.time()

    while time.time() - start_time < duration:
        cpu = current.cpu_percent(interval=0.5)
        mem = current.memory_info().rss / 1024 / 1024
        threads = current.num_threads()
        elapsed = time.time() - start_time

        print(f"{elapsed:<8.1f} {cpu:<8.2f} {mem:<12.2f} {threads}")
        time.sleep(0.5)


def demonstrate_child_processes() -> None:
    """Demonstrate working with child processes."""
    print("\n" + "=" * 60)
    print("CHILD PROCESSES")
    print("=" * 60)

    current = psutil.Process()

    print("\n1. Current Process Children:")
    children = current.children(recursive=True)
    if children:
        for child in children:
            print(f"   PID {child.pid}: {child.name()}")
    else:
        print("   No child processes")

    print("\n2. Process Family Tree:")
    print(f"   Current: PID {current.pid} ({current.name()})")
    if current.parent():
        parent = current.parent()
        print(f"   Parent: PID {parent.pid} ({parent.name()})")
        if parent.parent():
            grandparent = parent.parent()
            print(f"   Grandparent: PID {grandparent.pid} ({grandparent.name()})")


def demonstrate_process_metrics() -> None:
    """Demonstrate process performance metrics."""
    print("\n" + "=" * 60)
    print("PROCESS METRICS")
    print("=" * 60)

    current = psutil.Process()

    # Memory details
    mem_info = current.memory_info()
    print(f"\n1. Memory Details:")
    print(f"   RSS: {mem_info.rss / 1024 / 1024:.2f} MB")
    print(f"   VMS: {mem_info.vms / 1024 / 1024:.2f} MB")

    mem_percent = current.memory_percent()
    print(f"   Percent: {mem_percent:.2f}%")

    # CPU details
    cpu_times = current.cpu_times()
    print(f"\n2. CPU Times:")
    print(f"   User: {cpu_times.user:.2f}s")
    print(f"   System: {cpu_times.system:.2f}s")

    # I/O counters
    try:
        io_counters = current.io_counters()
        print(f"\n3. I/O Counters:")
        print(f"   Read bytes: {io_counters.read_bytes / 1024:.2f} KB")
        print(f"   Write bytes: {io_counters.write_bytes / 1024:.2f} KB")
    except (AttributeError, psutil.AccessDenied):
        print("\n3. I/O counters not available")


def main() -> None:
    """Main function demonstrating process management."""
    print("=" * 60)
    print("PYTHON PROCESS MANAGEMENT")
    print("=" * 60)

    demonstrate_process_info()
    demonstrate_process_creation()
    demonstrate_process_listing()
    demonstrate_system_info()
    demonstrate_process_control()
    demonstrate_resource_limits()
    demonstrate_child_processes()
    demonstrate_process_metrics()
    monitor_process(duration=2)

    print("\n" + "=" * 60)
    print("All process management operations completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
