#!/usr/bin/env python3
"""
Program 97: Task Automation
Demonstrates task automation, scheduling, and file processing.
"""

import os
import shutil
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Callable, Dict, Any
import tempfile
import glob
import re


def demonstrate_file_automation() -> None:
    """Demonstrate file automation tasks."""
    print("\n" + "=" * 60)
    print("FILE AUTOMATION")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Create sample files
        for i in range(5):
            (tmpdir / f"file{i}.txt").write_text(f"Content {i}")
            (tmpdir / f"data{i}.csv").write_text(f"Data {i}")

        print("\n1. Batch renaming:")

        # Rename all .txt files
        txt_files = list(tmpdir.glob('*.txt'))
        for i, file in enumerate(txt_files):
            new_name = file.parent / f"renamed_{i}.txt"
            file.rename(new_name)
            print(f"   {file.name} -> {new_name.name}")

        print(f"\n2. File organization:")

        # Create directories by type
        (tmpdir / 'texts').mkdir()
        (tmpdir / 'data').mkdir()

        # Move files
        for file in tmpdir.glob('renamed_*.txt'):
            shutil.move(str(file), tmpdir / 'texts' / file.name)
            print(f"   Moved {file.name} to texts/")

        for file in tmpdir.glob('*.csv'):
            shutil.move(str(file), tmpdir / 'data' / file.name)
            print(f"   Moved {file.name} to data/")


def demonstrate_bulk_operations() -> None:
    """Demonstrate bulk file operations."""
    print("\n" + "=" * 60)
    print("BULK OPERATIONS")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Create test files
        for i in range(10):
            (tmpdir / f"log_{i}.txt").write_text(f"Log entry {i}\n" * 100)

        print("\n1. Finding files by pattern:")
        log_files = list(tmpdir.glob('log_*.txt'))
        print(f"   Found {len(log_files)} log files")

        print("\n2. Batch processing:")
        for file in log_files[:3]:
            # Count lines
            lines = len(file.read_text().split('\n'))
            print(f"   {file.name}: {lines} lines")

        print("\n3. Filtering by size:")
        large_files = [f for f in log_files if f.stat().st_size > 500]
        print(f"   Large files (>500 bytes): {len(large_files)}")


def demonstrate_content_processing() -> None:
    """Demonstrate content processing automation."""
    print("\n" + "=" * 60)
    print("CONTENT PROCESSING")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Create test file
        test_file = tmpdir / "data.txt"
        test_file.write_text("""
        Line 1: Important
        Line 2: TODO: Fix this
        Line 3: FIXME: Critical bug
        Line 4: Normal text
        Line 5: TODO: Add feature
        """)

        print("\n1. Finding TODO comments:")
        content = test_file.read_text()
        todos = [line.strip() for line in content.split('\n')
                if 'TODO' in line or 'FIXME' in line]

        for todo in todos:
            print(f"   {todo}")

        print("\n2. Text replacement:")
        modified = content.replace('TODO', 'DONE')
        output_file = tmpdir / "processed.txt"
        output_file.write_text(modified)
        print(f"   Replaced TODO with DONE")

        print("\n3. Line filtering:")
        important_lines = [line for line in content.split('\n')
                          if 'Important' in line or 'Critical' in line]
        print(f"   Important lines: {len(important_lines)}")


def demonstrate_directory_sync() -> None:
    """Demonstrate directory synchronization."""
    print("\n" + "=" * 60)
    print("DIRECTORY SYNCHRONIZATION")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Create source and dest directories
        source = tmpdir / "source"
        dest = tmpdir / "dest"
        source.mkdir()
        dest.mkdir()

        # Create files in source
        (source / "file1.txt").write_text("File 1")
        (source / "file2.txt").write_text("File 2")

        print("\n1. Initial sync:")

        # Copy files
        for file in source.iterdir():
            shutil.copy2(file, dest / file.name)
            print(f"   Copied {file.name}")

        print("\n2. Incremental sync:")

        # Modify and add files
        (source / "file1.txt").write_text("File 1 Modified")
        (source / "file3.txt").write_text("File 3")

        # Sync only modified/new files
        for src_file in source.iterdir():
            dest_file = dest / src_file.name

            if not dest_file.exists():
                shutil.copy2(src_file, dest_file)
                print(f"   Added {src_file.name}")
            elif src_file.stat().st_mtime > dest_file.stat().st_mtime:
                shutil.copy2(src_file, dest_file)
                print(f"   Updated {src_file.name}")


def demonstrate_backup_automation() -> None:
    """Demonstrate backup automation."""
    print("\n" + "=" * 60)
    print("BACKUP AUTOMATION")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Create data directory
        data_dir = tmpdir / "data"
        data_dir.mkdir()

        # Create files
        for i in range(3):
            (data_dir / f"important_{i}.txt").write_text(f"Data {i}")

        print("\n1. Creating backup:")

        # Create backup with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"backup_{timestamp}"
        backup_path = tmpdir / backup_name

        # Copy directory
        shutil.copytree(data_dir, backup_path)
        print(f"   Created backup: {backup_name}")
        print(f"   Files backed up: {len(list(backup_path.iterdir()))}")

        print("\n2. Backup rotation:")
        print("   Keep only last N backups")
        print("   Delete backups older than X days")


def demonstrate_log_rotation() -> None:
    """Demonstrate log rotation."""
    print("\n" + "=" * 60)
    print("LOG ROTATION")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        log_file = tmpdir / "app.log"

        print("\n1. Log rotation strategy:")

        # Simulate log file
        log_file.write_text("Log entries...\n" * 1000)

        # Check size
        size_kb = log_file.stat().st_size / 1024

        if size_kb > 1:  # 1 KB threshold
            # Rotate log
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            rotated = tmpdir / f"app.log.{timestamp}"
            shutil.move(str(log_file), str(rotated))
            log_file.write_text("")  # Create new log
            print(f"   Rotated to: {rotated.name}")

        print("\n2. Rotation policies:")
        print("   - By size (e.g., 10 MB)")
        print("   - By time (e.g., daily)")
        print("   - Keep N most recent")


def demonstrate_cleanup_automation() -> None:
    """Demonstrate cleanup automation."""
    print("\n" + "=" * 60)
    print("CLEANUP AUTOMATION")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Create old and new files
        old_time = time.time() - (8 * 24 * 60 * 60)  # 8 days ago

        for i in range(5):
            file = tmpdir / f"old_file_{i}.tmp"
            file.write_text(f"Old {i}")
            os.utime(file, (old_time, old_time))

        for i in range(3):
            (tmpdir / f"new_file_{i}.txt").write_text(f"New {i}")

        print("\n1. Cleaning old temporary files:")

        # Find files older than 7 days
        seven_days_ago = time.time() - (7 * 24 * 60 * 60)
        old_files = []

        for file in tmpdir.iterdir():
            if file.stat().st_mtime < seven_days_ago:
                old_files.append(file)

        print(f"   Found {len(old_files)} old files")

        # Delete old files
        for file in old_files:
            file.unlink()
            print(f"   Deleted: {file.name}")

        print(f"\n2. Remaining files: {len(list(tmpdir.iterdir()))}")


def demonstrate_report_generation() -> None:
    """Demonstrate automated report generation."""
    print("\n" + "=" * 60)
    print("REPORT GENERATION")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Collect data
        data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_files': 150,
            'total_size_mb': 2048,
            'errors': 3,
            'warnings': 12
        }

        print("\n1. Generating report:")

        # Generate HTML report
        html_report = f"""
        <html>
        <head><title>System Report</title></head>
        <body>
            <h1>System Report</h1>
            <p>Generated: {data['timestamp']}</p>
            <table>
                <tr><td>Total Files:</td><td>{data['total_files']}</td></tr>
                <tr><td>Total Size:</td><td>{data['total_size_mb']} MB</td></tr>
                <tr><td>Errors:</td><td>{data['errors']}</td></tr>
                <tr><td>Warnings:</td><td>{data['warnings']}</td></tr>
            </table>
        </body>
        </html>
        """

        report_file = tmpdir / "report.html"
        report_file.write_text(html_report)
        print(f"   Report saved: {report_file.name}")

        print("\n2. Report summary:")
        for key, value in data.items():
            print(f"   {key}: {value}")


def demonstrate_monitoring_automation() -> None:
    """Demonstrate monitoring automation."""
    print("\n" + "=" * 60)
    print("MONITORING AUTOMATION")
    print("=" * 60)

    print("\n1. System checks:")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Check disk space
        usage = shutil.disk_usage(tmpdir)
        percent = (usage.used / usage.total) * 100

        print(f"   Disk usage: {percent:.1f}%")

        if percent > 80:
            print("   WARNING: High disk usage!")

        # Check file counts
        file_count = len(list(tmpdir.iterdir()))
        print(f"   Files in directory: {file_count}")

        print("\n2. Health checks:")
        print("   ✓ Disk space")
        print("   ✓ File counts")
        print("   ✓ Process status")
        print("   ✓ Service availability")


def demonstrate_task_scheduler_pattern() -> None:
    """Demonstrate task scheduler pattern."""
    print("\n" + "=" * 60)
    print("TASK SCHEDULER PATTERN")
    print("=" * 60)

    class Task:
        """Scheduled task."""

        def __init__(self, name: str, func: Callable, interval: int):
            self.name = name
            self.func = func
            self.interval = interval
            self.last_run = None

        def should_run(self) -> bool:
            """Check if task should run."""
            if self.last_run is None:
                return True

            elapsed = time.time() - self.last_run
            return elapsed >= self.interval

        def run(self):
            """Run the task."""
            print(f"   Running task: {self.name}")
            self.func()
            self.last_run = time.time()

    print("\n1. Task scheduler:")

    # Define tasks
    def backup_task():
        print("     Performing backup...")

    def cleanup_task():
        print("     Cleaning up old files...")

    tasks = [
        Task("backup", backup_task, interval=5),
        Task("cleanup", cleanup_task, interval=10)
    ]

    print("   Tasks registered:")
    for task in tasks:
        print(f"     - {task.name} (every {task.interval}s)")

    print("\n2. Simulating scheduler:")
    # Run for a short time
    for _ in range(2):
        for task in tasks:
            if task.should_run():
                task.run()
        time.sleep(0.1)


def demonstrate_best_practices() -> None:
    """Demonstrate automation best practices."""
    print("\n" + "=" * 60)
    print("AUTOMATION BEST PRACTICES")
    print("=" * 60)

    print("\n1. Reliability:")
    print("   ✓ Handle errors gracefully")
    print("   ✓ Log all operations")
    print("   ✓ Add retry logic")
    print("   ✓ Validate inputs")

    print("\n2. Maintainability:")
    print("   ✓ Use configuration files")
    print("   ✓ Make tasks idempotent")
    print("   ✓ Add dry-run mode")
    print("   ✓ Document behavior")

    print("\n3. Monitoring:")
    print("   ✓ Track success/failure")
    print("   ✓ Send notifications")
    print("   ✓ Log execution time")
    print("   ✓ Alert on errors")

    print("\n4. Scheduling:")
    print("   ✓ Use cron for periodic tasks")
    print("   ✓ Consider APScheduler for Python")
    print("   ✓ Avoid overlapping runs")
    print("   ✓ Handle long-running tasks")


def main() -> None:
    """Main function demonstrating automation."""
    print("=" * 60)
    print("PYTHON TASK AUTOMATION")
    print("=" * 60)

    demonstrate_file_automation()
    demonstrate_bulk_operations()
    demonstrate_content_processing()
    demonstrate_directory_sync()
    demonstrate_backup_automation()
    demonstrate_log_rotation()
    demonstrate_cleanup_automation()
    demonstrate_report_generation()
    demonstrate_monitoring_automation()
    demonstrate_task_scheduler_pattern()
    demonstrate_best_practices()

    print("\n" + "=" * 60)
    print("All automation demonstrations completed!")
    print("=" * 60)
    print("\nTools for scheduling:")
    print("- cron (Unix/Linux)")
    print("- Task Scheduler (Windows)")
    print("- APScheduler (Python library)")
    print("- Celery (Distributed tasks)")


if __name__ == "__main__":
    main()
