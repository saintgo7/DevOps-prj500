# Program 97: Task Automation

Comprehensive task automation including file processing, scheduling, and system tasks.

## Description

This program demonstrates task automation patterns for file operations, data processing, system maintenance, and scheduled jobs. Essential for DevOps, system administration, and workflow automation.

## Learning Objectives

- Master file automation patterns
- Implement batch processing
- Learn task scheduling
- Practice error handling
- Create monitoring scripts
- Build automation workflows

## Features

- **File Automation**: Batch rename, organize, cleanup
- **Data Processing**: CSV, JSON, log file processing
- **Backup Automation**: Incremental backups, rotation
- **Log Management**: Rotation, archival, analysis
- **Report Generation**: Automated reports
- **Task Scheduling**: Cron-like scheduling
- **Monitoring**: System health checks
- **Notification**: Email, Slack alerts

## Usage

```bash
cd /home/user/DevOps-prj500/01-100_Python/097_automation
python src/main.py --task backup --schedule daily
```

## Key Concepts

### File Automation

```python
from pathlib import Path

# Batch rename files
for file in Path('data').glob('*.txt'):
    new_name = file.stem.upper() + file.suffix
    file.rename(file.parent / new_name)

# Organize by type
for file in Path('downloads').iterdir():
    dest = Path('organized') / file.suffix[1:]
    dest.mkdir(exist_ok=True)
    file.rename(dest / file.name)
```

### Backup Automation

```python
import shutil
from datetime import datetime

def backup(source, dest_dir):
    """Create timestamped backup."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    dest = dest_dir / f'backup_{timestamp}'
    shutil.copytree(source, dest)
    return dest

# Rotate old backups
def rotate_backups(backup_dir, keep=7):
    """Keep only N most recent backups."""
    backups = sorted(backup_dir.glob('backup_*'))
    for old_backup in backups[:-keep]:
        shutil.rmtree(old_backup)
```

### Log Rotation

```python
from pathlib import Path

def rotate_log(log_file, max_size_mb=10):
    """Rotate log if over size limit."""
    if log_file.stat().st_size > max_size_mb * 1024 * 1024:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        rotated = log_file.with_suffix(f'.{timestamp}.log')
        log_file.rename(rotated)
        log_file.touch()
```

### Task Scheduler Pattern

```python
import time
from dataclasses import dataclass
from typing import Callable

@dataclass
class Task:
    name: str
    func: Callable
    interval: int  # seconds
    last_run: float = 0

    def should_run(self):
        return time.time() - self.last_run >= self.interval

    def run(self):
        self.func()
        self.last_run = time.time()

# Schedule tasks
tasks = [
    Task("backup", backup_data, interval=3600),
    Task("cleanup", cleanup_old_files, interval=86400),
]

while True:
    for task in tasks:
        if task.should_run():
            task.run()
    time.sleep(60)
```

### Data Processing

```python
import csv
import json

# Process CSV
with open('data.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        process(row)

# Generate report
report = {
    'timestamp': datetime.now().isoformat(),
    'total_files': len(files),
    'total_size': sum(f.stat().st_size for f in files),
    'errors': error_count
}

with open('report.json', 'w') as f:
    json.dump(report, f, indent=2)
```

## Best Practices

1. **Log everything**: Track what automation does
2. **Handle errors gracefully**: Don't let automation fail silently
3. **Add retry logic**: Network operations can fail
4. **Use dry-run mode**: Test without making changes
5. **Monitor automation**: Alert on failures
6. **Make idempotent**: Safe to run multiple times
7. **Add locking**: Prevent concurrent runs
8. **Document automation**: What it does, when it runs

## Testing

```bash
# Run tests
pytest tests/

# Dry run mode
python src/main.py --dry-run

# Run specific task
python src/main.py --task backup

# Test scenarios
# - File operations
# - Backup creation and rotation
# - Log processing
# - Error handling
# - Scheduling logic
# - Idempotency
```

## Navigation

- **Previous**: [Program 96 - Argument Parsing](../096_argument_parsing/README.md)
- **Next**: [Program 98 - Scripting](../098_scripting/README.md)
- **Home**: [Main README](../README.md)
