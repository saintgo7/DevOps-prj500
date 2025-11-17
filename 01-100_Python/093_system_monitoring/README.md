# Program 93: System Monitoring

Comprehensive system monitoring including CPU, memory, disk, network, and process monitoring.

## Description

This program demonstrates system monitoring using psutil library. Covers monitoring system resources, processes, network activity, and implementing monitoring dashboards. Essential for system administration and DevOps.

## Learning Objectives

- Master psutil library
- Monitor system resources
- Track process information
- Analyze network activity
- Implement monitoring alerts
- Build monitoring dashboards

## Features

- **CPU Monitoring**: Usage, per-core, times, frequency
- **Memory Monitoring**: Virtual, swap, process memory
- **Disk Monitoring**: Usage, I/O, partitions
- **Network Monitoring**: Interfaces, connections, I/O
- **Process Monitoring**: List, filter, resource usage
- **Temperature**: CPU and sensor temperatures
- **Battery**: Power status and remaining time
- **System Info**: Uptime, boot time, users

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/093_system_monitoring
python src/main.py

# Install psutil if needed
pip install psutil
```

## Key Concepts

### CPU Monitoring

```python
import psutil

# Overall CPU usage
cpu_percent = psutil.cpu_percent(interval=1)

# Per-CPU usage
per_cpu = psutil.cpu_percent(interval=1, percpu=True)

# CPU times
times = psutil.cpu_times()

# CPU count
physical = psutil.cpu_count(logical=False)
logical = psutil.cpu_count(logical=True)
```

### Memory Monitoring

```python
# Virtual memory
mem = psutil.virtual_memory()
print(f"Total: {mem.total / (1024**3):.2f} GB")
print(f"Available: {mem.available / (1024**3):.2f} GB")
print(f"Percent: {mem.percent}%")

# Swap memory
swap = psutil.swap_memory()
```

### Disk Monitoring

```python
# Disk usage
usage = psutil.disk_usage('/')
print(f"Total: {usage.total / (1024**3):.2f} GB")
print(f"Used: {usage.used / (1024**3):.2f} GB")
print(f"Free: {usage.free / (1024**3):.2f} GB")

# Disk I/O
io = psutil.disk_io_counters()
```

### Network Monitoring

```python
# Network I/O
net_io = psutil.net_io_counters()
print(f"Bytes sent: {net_io.bytes_sent / (1024**2):.2f} MB")
print(f"Bytes recv: {net_io.bytes_recv / (1024**2):.2f} MB")

# Network connections
connections = psutil.net_connections()
```

### Process Monitoring

```python
# Current process
process = psutil.Process()
print(f"CPU: {process.cpu_percent()}%")
print(f"Memory: {process.memory_percent()}%")

# All processes
for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
    print(proc.info)
```

### Monitoring Loop

```python
import time

while True:
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent

    # Alert if high usage
    if cpu > 80:
        print(f"High CPU: {cpu}%")
    if mem > 85:
        print(f"High memory: {mem}%")

    time.sleep(60)  # Check every minute
```

## Best Practices

1. **Set appropriate intervals**: Balance accuracy vs overhead
2. **Monitor thresholds**: Alert on high usage
3. **Log historical data**: Track trends
4. **Use dashboards**: Visualize metrics
5. **Handle permissions**: Some info requires elevated privileges
6. **Sample regularly**: Catch transient issues
7. **Aggregate data**: Reduce storage requirements
8. **Set up alerts**: Proactive problem detection

## Testing

```bash
# Run tests
pytest tests/

# Run monitoring dashboard
python src/main.py --dashboard

# Test scenarios
# - Resource monitoring accuracy
# - Alert threshold triggers
# - Historical data collection
# - Dashboard updates
# - Process tracking
# - Network monitoring
```

## Navigation

- **Previous**: [Program 92 - Event Loops](../092_event_loops/README.md)
- **Next**: [Program 94 - Resource Management](../094_resource_management/README.md)
- **Home**: [Main README](../README.md)
