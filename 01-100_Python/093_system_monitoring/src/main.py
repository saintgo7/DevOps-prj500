#!/usr/bin/env python3
"""
Program 93: System Monitoring
Demonstrates CPU, memory, disk, and network monitoring.
"""

import psutil
import time
from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SystemSnapshot:
    """Store system state snapshot."""
    timestamp: str
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    network_sent_mb: float
    network_recv_mb: float


def demonstrate_cpu_monitoring() -> None:
    """Demonstrate CPU monitoring."""
    print("\n" + "=" * 60)
    print("CPU MONITORING")
    print("=" * 60)

    # Overall CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)
    print(f"\n1. Overall CPU usage: {cpu_percent}%")

    # Per-CPU usage
    per_cpu = psutil.cpu_percent(interval=1, percpu=True)
    print(f"\n2. Per-CPU usage:")
    for i, percent in enumerate(per_cpu):
        print(f"   CPU {i}: {percent}%")

    # CPU times
    cpu_times = psutil.cpu_times()
    print(f"\n3. CPU times:")
    print(f"   User: {cpu_times.user:.2f}s")
    print(f"   System: {cpu_times.system:.2f}s")
    print(f"   Idle: {cpu_times.idle:.2f}s")

    # CPU stats
    cpu_stats = psutil.cpu_stats()
    print(f"\n4. CPU statistics:")
    print(f"   Context switches: {cpu_stats.ctx_switches}")
    print(f"   Interrupts: {cpu_stats.interrupts}")
    print(f"   Soft interrupts: {cpu_stats.soft_interrupts}")

    # CPU count
    physical_cores = psutil.cpu_count(logical=False)
    logical_cores = psutil.cpu_count(logical=True)
    print(f"\n5. CPU count:")
    print(f"   Physical cores: {physical_cores}")
    print(f"   Logical cores: {logical_cores}")

    # CPU frequency
    try:
        freq = psutil.cpu_freq()
        if freq:
            print(f"\n6. CPU frequency:")
            print(f"   Current: {freq.current:.2f} MHz")
            print(f"   Min: {freq.min:.2f} MHz")
            print(f"   Max: {freq.max:.2f} MHz")
    except Exception:
        print("\n6. CPU frequency: Not available")


def demonstrate_memory_monitoring() -> None:
    """Demonstrate memory monitoring."""
    print("\n" + "=" * 60)
    print("MEMORY MONITORING")
    print("=" * 60)

    # Virtual memory
    mem = psutil.virtual_memory()
    print(f"\n1. Virtual memory:")
    print(f"   Total: {mem.total / (1024**3):.2f} GB")
    print(f"   Available: {mem.available / (1024**3):.2f} GB")
    print(f"   Used: {mem.used / (1024**3):.2f} GB")
    print(f"   Free: {mem.free / (1024**3):.2f} GB")
    print(f"   Percent: {mem.percent}%")

    # Swap memory
    swap = psutil.swap_memory()
    print(f"\n2. Swap memory:")
    print(f"   Total: {swap.total / (1024**3):.2f} GB")
    print(f"   Used: {swap.used / (1024**3):.2f} GB")
    print(f"   Free: {swap.free / (1024**3):.2f} GB")
    print(f"   Percent: {swap.percent}%")


def demonstrate_disk_monitoring() -> None:
    """Demonstrate disk monitoring."""
    print("\n" + "=" * 60)
    print("DISK MONITORING")
    print("=" * 60)

    # Disk partitions
    print("\n1. Disk partitions:")
    for partition in psutil.disk_partitions():
        print(f"   Device: {partition.device}")
        print(f"   Mountpoint: {partition.mountpoint}")
        print(f"   Filesystem: {partition.fstype}")

        try:
            usage = psutil.disk_usage(partition.mountpoint)
            print(f"   Total: {usage.total / (1024**3):.2f} GB")
            print(f"   Used: {usage.used / (1024**3):.2f} GB")
            print(f"   Free: {usage.free / (1024**3):.2f} GB")
            print(f"   Percent: {usage.percent}%")
        except PermissionError:
            print("   Permission denied")
        print()

    # Disk I/O
    print("2. Disk I/O statistics:")
    disk_io = psutil.disk_io_counters()
    if disk_io:
        print(f"   Read count: {disk_io.read_count}")
        print(f"   Write count: {disk_io.write_count}")
        print(f"   Read bytes: {disk_io.read_bytes / (1024**2):.2f} MB")
        print(f"   Write bytes: {disk_io.write_bytes / (1024**2):.2f} MB")


def demonstrate_network_monitoring() -> None:
    """Demonstrate network monitoring."""
    print("\n" + "=" * 60)
    print("NETWORK MONITORING")
    print("=" * 60)

    # Network I/O
    net_io = psutil.net_io_counters()
    print(f"\n1. Network I/O:")
    print(f"   Bytes sent: {net_io.bytes_sent / (1024**2):.2f} MB")
    print(f"   Bytes received: {net_io.bytes_recv / (1024**2):.2f} MB")
    print(f"   Packets sent: {net_io.packets_sent}")
    print(f"   Packets received: {net_io.packets_recv}")
    print(f"   Errors in: {net_io.errin}")
    print(f"   Errors out: {net_io.errout}")

    # Per-interface stats
    print(f"\n2. Per-interface statistics:")
    net_if_stats = psutil.net_if_stats()
    for interface, stats in net_if_stats.items():
        print(f"   {interface}:")
        print(f"     Speed: {stats.speed} Mbps")
        print(f"     MTU: {stats.mtu}")
        print(f"     Up: {stats.isup}")

    # Network connections
    print(f"\n3. Network connections:")
    try:
        connections = psutil.net_connections(kind='inet')
        tcp_count = sum(1 for c in connections if c.type == 1)
        udp_count = sum(1 for c in connections if c.type == 2)
        print(f"   TCP connections: {tcp_count}")
        print(f"   UDP connections: {udp_count}")
    except psutil.AccessDenied:
        print("   Access denied (need elevated privileges)")


def demonstrate_process_monitoring() -> None:
    """Demonstrate process monitoring."""
    print("\n" + "=" * 60)
    print("PROCESS MONITORING")
    print("=" * 60)

    # Process count
    print(f"\n1. Total processes: {len(psutil.pids())}")

    # Top processes by memory
    print(f"\n2. Top 5 processes by memory:")
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    processes.sort(key=lambda x: x['memory_percent'] or 0, reverse=True)

    for proc in processes[:5]:
        print(f"   PID {proc['pid']}: {proc['name'][:30]} - {proc['memory_percent']:.2f}%")

    # Process states
    print(f"\n3. Processes by state:")
    states = {}
    for proc in psutil.process_iter(['status']):
        try:
            status = proc.info['status']
            states[status] = states.get(status, 0) + 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    for state, count in sorted(states.items()):
        print(f"   {state}: {count}")


def demonstrate_temperature_monitoring() -> None:
    """Demonstrate temperature monitoring."""
    print("\n" + "=" * 60)
    print("TEMPERATURE MONITORING")
    print("=" * 60)

    try:
        temps = psutil.sensors_temperatures()
        if temps:
            print("\n1. System temperatures:")
            for name, entries in temps.items():
                print(f"   {name}:")
                for entry in entries:
                    print(f"     {entry.label}: {entry.current}°C")
        else:
            print("\n1. Temperature sensors: Not available")
    except AttributeError:
        print("\n1. Temperature monitoring: Not supported on this platform")


def demonstrate_battery_monitoring() -> None:
    """Demonstrate battery monitoring."""
    print("\n" + "=" * 60)
    print("BATTERY MONITORING")
    print("=" * 60)

    try:
        battery = psutil.sensors_battery()
        if battery:
            print(f"\n1. Battery status:")
            print(f"   Percent: {battery.percent}%")
            print(f"   Plugged in: {battery.power_plugged}")
            if battery.secsleft != psutil.POWER_TIME_UNLIMITED:
                hours = battery.secsleft // 3600
                minutes = (battery.secsleft % 3600) // 60
                print(f"   Time remaining: {hours}h {minutes}m")
        else:
            print("\n1. Battery: Not present")
    except AttributeError:
        print("\n1. Battery monitoring: Not supported on this platform")


def demonstrate_boot_time() -> None:
    """Demonstrate system boot time."""
    print("\n" + "=" * 60)
    print("SYSTEM UPTIME")
    print("=" * 60)

    boot_time = psutil.boot_time()
    boot_datetime = datetime.fromtimestamp(boot_time)

    uptime_seconds = time.time() - boot_time
    uptime_hours = uptime_seconds / 3600
    uptime_days = uptime_hours / 24

    print(f"\n1. Boot time: {boot_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"2. Uptime: {uptime_days:.1f} days ({uptime_hours:.1f} hours)")


def monitor_system(duration: int = 5, interval: int = 1) -> List[SystemSnapshot]:
    """Monitor system for a duration."""
    print("\n" + "=" * 60)
    print("CONTINUOUS MONITORING")
    print("=" * 60)

    print(f"\nMonitoring for {duration} seconds...")
    print(f"{'Time':<12} {'CPU%':<8} {'Mem%':<8} {'Disk%':<8} {'Net↑(MB)':<10} {'Net↓(MB)'}")
    print("-" * 70)

    snapshots = []
    net_start = psutil.net_io_counters()

    for i in range(duration):
        timestamp = datetime.now().strftime('%H:%M:%S')

        cpu = psutil.cpu_percent(interval=interval)
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        net_now = psutil.net_io_counters()

        net_sent = (net_now.bytes_sent - net_start.bytes_sent) / (1024**2)
        net_recv = (net_now.bytes_recv - net_start.bytes_recv) / (1024**2)

        snapshot = SystemSnapshot(
            timestamp=timestamp,
            cpu_percent=cpu,
            memory_percent=mem,
            disk_percent=disk,
            network_sent_mb=net_sent,
            network_recv_mb=net_recv
        )
        snapshots.append(snapshot)

        print(f"{timestamp:<12} {cpu:<8.1f} {mem:<8.1f} {disk:<8.1f} {net_sent:<10.2f} {net_recv:.2f}")

    return snapshots


def demonstrate_alerts() -> None:
    """Demonstrate monitoring alerts."""
    print("\n" + "=" * 60)
    print("MONITORING ALERTS")
    print("=" * 60)

    # Define thresholds
    cpu_threshold = 80
    memory_threshold = 80
    disk_threshold = 90

    print(f"\n1. Alert thresholds:")
    print(f"   CPU: > {cpu_threshold}%")
    print(f"   Memory: > {memory_threshold}%")
    print(f"   Disk: > {disk_threshold}%")

    # Check current values
    print(f"\n2. Current status:")

    cpu = psutil.cpu_percent(interval=1)
    if cpu > cpu_threshold:
        print(f"   ⚠ CPU: {cpu}% (HIGH)")
    else:
        print(f"   ✓ CPU: {cpu}% (OK)")

    mem = psutil.virtual_memory().percent
    if mem > memory_threshold:
        print(f"   ⚠ Memory: {mem}% (HIGH)")
    else:
        print(f"   ✓ Memory: {mem}% (OK)")

    disk = psutil.disk_usage('/').percent
    if disk > disk_threshold:
        print(f"   ⚠ Disk: {disk}% (HIGH)")
    else:
        print(f"   ✓ Disk: {disk}% (OK)")


def demonstrate_resource_trends() -> None:
    """Demonstrate resource trend analysis."""
    print("\n" + "=" * 60)
    print("RESOURCE TRENDS")
    print("=" * 60)

    print("\n1. Collecting samples...")

    samples = []
    for i in range(5):
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory().percent
        samples.append({'cpu': cpu, 'mem': mem})

    # Calculate averages
    avg_cpu = sum(s['cpu'] for s in samples) / len(samples)
    avg_mem = sum(s['mem'] for s in samples) / len(samples)

    print(f"\n2. Average usage:")
    print(f"   CPU: {avg_cpu:.1f}%")
    print(f"   Memory: {avg_mem:.1f}%")

    # Detect trends
    cpu_trend = "stable"
    if samples[-1]['cpu'] > samples[0]['cpu'] + 10:
        cpu_trend = "increasing"
    elif samples[-1]['cpu'] < samples[0]['cpu'] - 10:
        cpu_trend = "decreasing"

    print(f"\n3. Trends:")
    print(f"   CPU: {cpu_trend}")


def demonstrate_best_practices() -> None:
    """Demonstrate monitoring best practices."""
    print("\n" + "=" * 60)
    print("MONITORING BEST PRACTICES")
    print("=" * 60)

    print("\n1. What to monitor:")
    print("   ✓ CPU usage and load average")
    print("   ✓ Memory usage and swap")
    print("   ✓ Disk usage and I/O")
    print("   ✓ Network traffic")
    print("   ✓ Process count and status")

    print("\n2. Monitoring intervals:")
    print("   - System metrics: 1-5 seconds")
    print("   - Disk usage: 1-5 minutes")
    print("   - Process stats: 5-30 seconds")

    print("\n3. Alert thresholds:")
    print("   - CPU: > 80% sustained")
    print("   - Memory: > 85%")
    print("   - Disk: > 90%")
    print("   - Swap: Any usage")

    print("\n4. Data retention:")
    print("   - Real-time: 1 hour")
    print("   - High-res: 24 hours")
    print("   - Aggregated: 30 days+")


def main() -> None:
    """Main function demonstrating system monitoring."""
    print("=" * 60)
    print("PYTHON SYSTEM MONITORING")
    print("=" * 60)

    demonstrate_cpu_monitoring()
    demonstrate_memory_monitoring()
    demonstrate_disk_monitoring()
    demonstrate_network_monitoring()
    demonstrate_process_monitoring()
    demonstrate_temperature_monitoring()
    demonstrate_battery_monitoring()
    demonstrate_boot_time()
    monitor_system(duration=3, interval=1)
    demonstrate_alerts()
    demonstrate_resource_trends()
    demonstrate_best_practices()

    print("\n" + "=" * 60)
    print("All monitoring demonstrations completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
