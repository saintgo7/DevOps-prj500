#!/usr/bin/env python3
"""
Program 98: Shell Scripting with Python
Demonstrates Python for system tasks and shell script replacement.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import tempfile
from typing import List, Optional, Tuple


def demonstrate_shell_commands() -> None:
    """Demonstrate running shell commands."""
    print("\n" + "=" * 60)
    print("SHELL COMMANDS")
    print("=" * 60)

    print("\n1. Running simple commands:")

    # Get current user
    result = subprocess.run(['whoami'], capture_output=True, text=True)
    print(f"   Current user: {result.stdout.strip()}")

    # Get current directory
    result = subprocess.run(['pwd'], capture_output=True, text=True)
    print(f"   Working directory: {result.stdout.strip()}")

    print("\n2. Command with pipes:")
    result = subprocess.run(
        'ls -la | head -5',
        shell=True,
        capture_output=True,
        text=True,
        cwd='/tmp'
    )
    print("   Output (first 5 lines of ls):")
    for line in result.stdout.split('\n')[:3]:
        if line:
            print(f"     {line[:60]}...")


def demonstrate_file_operations() -> None:
    """Demonstrate file operations (bash replacement)."""
    print("\n" + "=" * 60)
    print("FILE OPERATIONS")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        print("\n1. Creating files:")
        for i in range(3):
            file = tmpdir / f"file{i}.txt"
            file.write_text(f"Content {i}")
            print(f"   Created: {file.name}")

        print("\n2. Listing files:")
        for file in sorted(tmpdir.iterdir()):
            print(f"   {file.name}")

        print("\n3. Copying files:")
        src = tmpdir / "file0.txt"
        dst = tmpdir / "file0_copy.txt"
        shutil.copy2(src, dst)
        print(f"   Copied: {src.name} -> {dst.name}")

        print("\n4. Moving files:")
        old_path = tmpdir / "file0_copy.txt"
        new_path = tmpdir / "renamed.txt"
        old_path.rename(new_path)
        print(f"   Moved: {old_path.name} -> {new_path.name}")


def demonstrate_text_processing() -> None:
    """Demonstrate text processing (grep/sed/awk replacement)."""
    print("\n" + "=" * 60)
    print("TEXT PROCESSING")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Create test file
        log_file = tmpdir / "app.log"
        log_file.write_text("""
2024-01-01 10:00:00 INFO Starting application
2024-01-01 10:00:01 DEBUG Loading configuration
2024-01-01 10:00:02 ERROR Failed to connect
2024-01-01 10:00:03 INFO Retrying connection
2024-01-01 10:00:04 ERROR Connection timeout
2024-01-01 10:00:05 WARNING Low memory
        """)

        print("\n1. Grep-like filtering:")
        content = log_file.read_text()
        errors = [line for line in content.split('\n') if 'ERROR' in line]
        print(f"   Error lines: {len(errors)}")
        for error in errors[:2]:
            print(f"     {error.strip()[:60]}...")

        print("\n2. Sed-like replacement:")
        modified = content.replace('ERROR', 'CRITICAL')
        print("   Replaced ERROR with CRITICAL")

        print("\n3. Awk-like field extraction:")
        for line in content.split('\n')[1:4]:
            if line.strip():
                parts = line.split()
                if len(parts) >= 3:
                    timestamp = f"{parts[0]} {parts[1]}"
                    level = parts[2]
                    print(f"   {timestamp} [{level}]")


def demonstrate_process_management() -> None:
    """Demonstrate process management."""
    print("\n" + "=" * 60)
    print("PROCESS MANAGEMENT")
    print("=" * 60)

    print("\n1. Starting background process:")

    # Start a process
    proc = subprocess.Popen(
        ['sleep', '0.5'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    print(f"   Started process PID: {proc.pid}")
    print(f"   Process running: {proc.poll() is None}")

    # Wait for it
    proc.wait()
    print(f"   Process finished with code: {proc.returncode}")


def demonstrate_environment_variables() -> None:
    """Demonstrate environment variable handling."""
    print("\n" + "=" * 60)
    print("ENVIRONMENT VARIABLES")
    print("=" * 60)

    print("\n1. Reading environment variables:")
    home = os.environ.get('HOME', '/home/default')
    user = os.environ.get('USER', 'unknown')
    print(f"   HOME: {home}")
    print(f"   USER: {user}")

    print("\n2. Setting environment variables:")
    os.environ['CUSTOM_VAR'] = 'custom_value'
    print(f"   CUSTOM_VAR: {os.environ['CUSTOM_VAR']}")

    print("\n3. Environment for subprocess:")
    env = os.environ.copy()
    env['MY_VAR'] = 'test'
    result = subprocess.run(
        ['sh', '-c', 'echo $MY_VAR'],
        env=env,
        capture_output=True,
        text=True
    )
    print(f"   Subprocess saw: {result.stdout.strip()}")


def demonstrate_command_line_args() -> None:
    """Demonstrate command-line argument handling."""
    print("\n" + "=" * 60)
    print("COMMAND-LINE ARGUMENTS")
    print("=" * 60)

    print("\n1. Script arguments (sys.argv):")
    print(f"   Script name: {sys.argv[0]}")
    print(f"   Argument count: {len(sys.argv) - 1}")

    print("\n2. Common patterns:")
    print("   for arg in sys.argv[1:]:")
    print("       process(arg)")


def demonstrate_error_handling() -> None:
    """Demonstrate error handling in scripts."""
    print("\n" + "=" * 60)
    print("ERROR HANDLING")
    print("=" * 60)

    print("\n1. Exit codes:")
    print("   sys.exit(0)  # Success")
    print("   sys.exit(1)  # General error")
    print("   sys.exit(2)  # Misuse")

    print("\n2. Command errors:")
    result = subprocess.run(
        ['ls', '/nonexistent'],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("   Command failed!")
        print(f"   Return code: {result.returncode}")
        print(f"   Error: {result.stderr.strip()[:50]}...")

    print("\n3. Try-except pattern:")
    try:
        Path('/nonexistent/file').read_text()
    except FileNotFoundError:
        print("   ✓ Caught file not found error")


def demonstrate_user_interaction() -> None:
    """Demonstrate user interaction."""
    print("\n" + "=" * 60)
    print("USER INTERACTION")
    print("=" * 60)

    print("\n1. Input methods:")
    print("   # Interactive input")
    print("   name = input('Enter name: ')")

    print("\n2. Confirmation:")
    print("   response = input('Continue? [y/n]: ')")
    print("   if response.lower() == 'y':")
    print("       proceed()")

    print("\n3. Password input:")
    print("   import getpass")
    print("   password = getpass.getpass('Password: ')")


def demonstrate_file_searching() -> None:
    """Demonstrate file searching (find replacement)."""
    print("\n" + "=" * 60)
    print("FILE SEARCHING")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Create test structure
        (tmpdir / 'dir1').mkdir()
        (tmpdir / 'dir2').mkdir()
        (tmpdir / 'file1.txt').write_text("File 1")
        (tmpdir / 'dir1' / 'file2.txt').write_text("File 2")
        (tmpdir / 'dir2' / 'file3.log').write_text("File 3")

        print("\n1. Find all .txt files:")
        txt_files = list(tmpdir.rglob('*.txt'))
        for file in txt_files:
            rel_path = file.relative_to(tmpdir)
            print(f"   {rel_path}")

        print("\n2. Find files in specific directory:")
        dir1_files = list((tmpdir / 'dir1').iterdir())
        for file in dir1_files:
            print(f"   {file.name}")


def demonstrate_archiving() -> None:
    """Demonstrate archiving (tar replacement)."""
    print("\n" + "=" * 60)
    print("ARCHIVING")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Create files to archive
        data_dir = tmpdir / 'data'
        data_dir.mkdir()

        for i in range(3):
            (data_dir / f'file{i}.txt').write_text(f"Data {i}")

        print("\n1. Creating archive:")

        # Create zip archive
        archive_path = tmpdir / 'archive'
        shutil.make_archive(
            str(archive_path),
            'zip',
            data_dir
        )

        archive_file = Path(str(archive_path) + '.zip')
        size_kb = archive_file.stat().st_size / 1024
        print(f"   Archive created: {archive_file.name}")
        print(f"   Size: {size_kb:.1f} KB")

        print("\n2. Extracting archive:")
        extract_dir = tmpdir / 'extracted'
        extract_dir.mkdir()

        shutil.unpack_archive(archive_file, extract_dir)
        extracted_files = list(extract_dir.rglob('*'))
        print(f"   Extracted {len(extracted_files)} items")


def demonstrate_system_info() -> None:
    """Demonstrate system information gathering."""
    print("\n" + "=" * 60)
    print("SYSTEM INFORMATION")
    print("=" * 60)

    print("\n1. Platform information:")
    print(f"   OS: {sys.platform}")
    print(f"   Python version: {sys.version.split()[0]}")

    print("\n2. Path information:")
    print(f"   Executable: {sys.executable}")
    print(f"   Current directory: {os.getcwd()}")

    print("\n3. Disk usage:")
    usage = shutil.disk_usage('/')
    total_gb = usage.total / (1024**3)
    used_gb = usage.used / (1024**3)
    free_gb = usage.free / (1024**3)
    print(f"   Total: {total_gb:.1f} GB")
    print(f"   Used: {used_gb:.1f} GB")
    print(f"   Free: {free_gb:.1f} GB")


def demonstrate_parallel_execution() -> None:
    """Demonstrate parallel command execution."""
    print("\n" + "=" * 60)
    print("PARALLEL EXECUTION")
    print("=" * 60)

    print("\n1. Running commands in parallel:")

    import concurrent.futures

    def run_command(cmd: List[str]) -> Tuple[int, str]:
        """Run a command and return result."""
        result = subprocess.run(cmd, capture_output=True, text=True)
        return (result.returncode, result.stdout)

    commands = [
        ['echo', 'Task 1'],
        ['echo', 'Task 2'],
        ['echo', 'Task 3']
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(run_command, cmd) for cmd in commands]

        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            code, output = future.result()
            print(f"   Command {i+1}: {output.strip()}")


def demonstrate_scripting_best_practices() -> None:
    """Demonstrate scripting best practices."""
    print("\n" + "=" * 60)
    print("SCRIPTING BEST PRACTICES")
    print("=" * 60)

    print("\n1. Script structure:")
    print("   #!/usr/bin/env python3")
    print("   # Docstring explaining purpose")
    print("   # Imports")
    print("   # Functions")
    print("   # if __name__ == '__main__':")

    print("\n2. Error handling:")
    print("   ✓ Check return codes")
    print("   ✓ Use try-except")
    print("   ✓ Provide error messages")
    print("   ✓ Exit with appropriate codes")

    print("\n3. Logging:")
    print("   ✓ Log important operations")
    print("   ✓ Include timestamps")
    print("   ✓ Different log levels")
    print("   ✓ Log to file option")

    print("\n4. Configuration:")
    print("   ✓ Use config files")
    print("   ✓ Environment variables")
    print("   ✓ Command-line args")
    print("   ✓ Sensible defaults")

    print("\n5. Safety:")
    print("   ✓ Validate inputs")
    print("   ✓ Dry-run mode")
    print("   ✓ Confirm destructive ops")
    print("   ✓ Create backups")


def main() -> None:
    """Main function demonstrating scripting."""
    print("=" * 60)
    print("PYTHON SHELL SCRIPTING")
    print("=" * 60)

    demonstrate_shell_commands()
    demonstrate_file_operations()
    demonstrate_text_processing()
    demonstrate_process_management()
    demonstrate_environment_variables()
    demonstrate_command_line_args()
    demonstrate_error_handling()
    demonstrate_user_interaction()
    demonstrate_file_searching()
    demonstrate_archiving()
    demonstrate_system_info()
    demonstrate_parallel_execution()
    demonstrate_scripting_best_practices()

    print("\n" + "=" * 60)
    print("All scripting demonstrations completed!")
    print("=" * 60)
    print("\nPython vs Shell:")
    print("✓ Better error handling")
    print("✓ More readable")
    print("✓ Cross-platform")
    print("✓ Rich standard library")
    print("✓ Easier to test")


if __name__ == "__main__":
    main()
