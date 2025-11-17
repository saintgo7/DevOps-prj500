#!/usr/bin/env python3
"""
Program 84: Subprocess Management
Demonstrates running commands, pipes, stdout/stderr handling.
"""

import subprocess
import sys
import os
from typing import Tuple, Optional, List
from dataclasses import dataclass
import shlex
import tempfile
from pathlib import Path


@dataclass
class CommandResult:
    """Store command execution result."""
    returncode: int
    stdout: str
    stderr: str
    success: bool


def run_simple_command(command: str) -> CommandResult:
    """Run a simple command and return result."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=5
        )
        return CommandResult(
            returncode=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
            success=result.returncode == 0
        )
    except subprocess.TimeoutExpired:
        return CommandResult(
            returncode=-1,
            stdout="",
            stderr="Command timed out",
            success=False
        )


def demonstrate_basic_subprocess() -> None:
    """Demonstrate basic subprocess operations."""
    print("\n" + "=" * 60)
    print("BASIC SUBPROCESS")
    print("=" * 60)

    # Simple command
    print("\n1. Running simple command (echo):")
    result = subprocess.run(['echo', 'Hello, subprocess!'], capture_output=True, text=True)
    print(f"   Output: {result.stdout.strip()}")
    print(f"   Return code: {result.returncode}")

    # Command with multiple arguments
    print("\n2. Command with arguments (date):")
    result = subprocess.run(['date', '+%Y-%m-%d'], capture_output=True, text=True)
    print(f"   Output: {result.stdout.strip()}")

    # Shell command
    print("\n3. Shell command:")
    result = subprocess.run('echo "Shell: $SHELL"', shell=True, capture_output=True, text=True)
    print(f"   Output: {result.stdout.strip()}")


def demonstrate_output_capture() -> None:
    """Demonstrate capturing stdout and stderr."""
    print("\n" + "=" * 60)
    print("OUTPUT CAPTURE")
    print("=" * 60)

    # Capture stdout
    print("\n1. Capturing stdout:")
    result = subprocess.run(['ls', '-la', '/tmp'], capture_output=True, text=True)
    lines = result.stdout.split('\n')[:5]
    for line in lines:
        if line:
            print(f"   {line}")
    print("   ...")

    # Capture stderr
    print("\n2. Capturing stderr:")
    result = subprocess.run(['ls', '/nonexistent'], capture_output=True, text=True)
    print(f"   Stderr: {result.stderr.strip()}")
    print(f"   Return code: {result.returncode}")

    # Both stdout and stderr
    print("\n3. Redirecting stderr to stdout:")
    result = subprocess.run(
        ['sh', '-c', 'echo "stdout message" && echo "stderr message" >&2'],
        capture_output=True,
        text=True
    )
    print(f"   Stdout: {result.stdout.strip()}")
    print(f"   Stderr: {result.stderr.strip()}")


def demonstrate_input_handling() -> None:
    """Demonstrate passing input to subprocess."""
    print("\n" + "=" * 60)
    print("INPUT HANDLING")
    print("=" * 60)

    # Pass input via stdin
    print("\n1. Passing input via stdin:")
    result = subprocess.run(
        ['cat'],
        input="Hello from stdin\nLine 2\nLine 3",
        capture_output=True,
        text=True
    )
    print(f"   Output: {result.stdout}")

    # Pipe input
    print("\n2. Using input parameter:")
    result = subprocess.run(
        ['grep', 'Line'],
        input="Line 1\nNo match\nLine 2\n",
        capture_output=True,
        text=True
    )
    print(f"   Filtered output: {result.stdout}")


def demonstrate_pipes() -> None:
    """Demonstrate piping between commands."""
    print("\n" + "=" * 60)
    print("COMMAND PIPES")
    print("=" * 60)

    # Method 1: Using shell
    print("\n1. Pipe with shell:")
    result = subprocess.run(
        'echo "line1\nline2\nline3" | grep "line2"',
        shell=True,
        capture_output=True,
        text=True
    )
    print(f"   Output: {result.stdout.strip()}")

    # Method 2: Manual piping
    print("\n2. Manual pipe:")
    # First command
    p1 = subprocess.Popen(['echo', '-e', 'apple\nbanana\ncherry'], stdout=subprocess.PIPE)
    # Second command
    p2 = subprocess.Popen(['grep', 'banana'], stdin=p1.stdout, stdout=subprocess.PIPE, text=True)
    p1.stdout.close()  # Allow p1 to receive SIGPIPE
    output, _ = p2.communicate()
    print(f"   Output: {output.strip()}")

    # Method 3: Chain of pipes
    print("\n3. Chain of pipes:")
    result = subprocess.run(
        'echo "test\nTEST\nTest" | grep -i "test" | wc -l',
        shell=True,
        capture_output=True,
        text=True
    )
    print(f"   Count: {result.stdout.strip()}")


def demonstrate_popen() -> None:
    """Demonstrate Popen for advanced process control."""
    print("\n" + "=" * 60)
    print("POPEN ADVANCED CONTROL")
    print("=" * 60)

    # Basic Popen
    print("\n1. Basic Popen:")
    process = subprocess.Popen(
        ['echo', 'Hello from Popen'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate()
    print(f"   Output: {stdout.strip()}")
    print(f"   Return code: {process.returncode}")

    # Popen with timeout
    print("\n2. Popen with timeout:")
    process = subprocess.Popen(['sleep', '0.1'], stdout=subprocess.PIPE)
    try:
        stdout, stderr = process.communicate(timeout=1)
        print(f"   Completed within timeout")
    except subprocess.TimeoutExpired:
        process.kill()
        print(f"   Timeout expired, process killed")

    # Poll process
    print("\n3. Polling process:")
    process = subprocess.Popen(['sleep', '0.2'], stdout=subprocess.PIPE)
    print(f"   Process started (PID: {process.pid})")
    print(f"   Poll (before completion): {process.poll()}")
    process.wait()
    print(f"   Poll (after completion): {process.poll()}")


def demonstrate_error_handling() -> None:
    """Demonstrate subprocess error handling."""
    print("\n" + "=" * 60)
    print("ERROR HANDLING")
    print("=" * 60)

    # Handle command not found
    print("\n1. Command not found:")
    try:
        result = subprocess.run(
            ['nonexistent_command'],
            capture_output=True,
            text=True,
            check=True
        )
    except FileNotFoundError:
        print("   ✓ Caught FileNotFoundError")

    # Handle non-zero exit
    print("\n2. Non-zero exit code:")
    try:
        result = subprocess.run(
            ['ls', '/nonexistent'],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"   ✓ Caught CalledProcessError")
        print(f"   Return code: {e.returncode}")

    # Timeout handling
    print("\n3. Timeout handling:")
    try:
        result = subprocess.run(
            ['sleep', '10'],
            timeout=0.5,
            capture_output=True
        )
    except subprocess.TimeoutExpired:
        print("   ✓ Caught TimeoutExpired")


def demonstrate_environment() -> None:
    """Demonstrate environment variable handling."""
    print("\n" + "=" * 60)
    print("ENVIRONMENT VARIABLES")
    print("=" * 60)

    # Inherit environment
    print("\n1. Inherit environment:")
    result = subprocess.run(
        ['sh', '-c', 'echo "USER=$USER"'],
        capture_output=True,
        text=True
    )
    print(f"   {result.stdout.strip()}")

    # Custom environment
    print("\n2. Custom environment:")
    custom_env = os.environ.copy()
    custom_env['CUSTOM_VAR'] = 'custom_value'
    result = subprocess.run(
        ['sh', '-c', 'echo "CUSTOM=$CUSTOM_VAR"'],
        env=custom_env,
        capture_output=True,
        text=True
    )
    print(f"   {result.stdout.strip()}")

    # Clean environment
    print("\n3. Minimal environment:")
    result = subprocess.run(
        ['env'],
        env={'PATH': os.environ['PATH'], 'HOME': '/tmp'},
        capture_output=True,
        text=True
    )
    lines = result.stdout.strip().split('\n')
    print(f"   Environment variables: {len(lines)}")


def demonstrate_working_directory() -> None:
    """Demonstrate working directory control."""
    print("\n" + "=" * 60)
    print("WORKING DIRECTORY")
    print("=" * 60)

    # Default working directory
    print("\n1. Default working directory:")
    result = subprocess.run(['pwd'], capture_output=True, text=True)
    print(f"   PWD: {result.stdout.strip()}")

    # Custom working directory
    print("\n2. Custom working directory:")
    result = subprocess.run(
        ['pwd'],
        cwd='/tmp',
        capture_output=True,
        text=True
    )
    print(f"   PWD: {result.stdout.strip()}")


def demonstrate_shell_injection_safety() -> None:
    """Demonstrate safe command execution."""
    print("\n" + "=" * 60)
    print("SHELL INJECTION SAFETY")
    print("=" * 60)

    # Unsafe (shell=True with user input)
    print("\n1. Unsafe example (educational only):")
    print("   DON'T: subprocess.run(f'ls {user_input}', shell=True)")

    # Safe (list arguments)
    print("\n2. Safe method - use list arguments:")
    user_input = "/tmp"
    result = subprocess.run(['ls', user_input], capture_output=True, text=True)
    print(f"   ✓ Safe: subprocess.run(['ls', user_input])")

    # Safe (shlex.quote)
    print("\n3. Safe method - use shlex.quote:")
    unsafe_input = "/tmp; echo 'injected'"
    safe_input = shlex.quote(unsafe_input)
    print(f"   Unsafe: {unsafe_input}")
    print(f"   Safe: {safe_input}")


def demonstrate_real_world_examples() -> None:
    """Demonstrate real-world subprocess usage."""
    print("\n" + "=" * 60)
    print("REAL-WORLD EXAMPLES")
    print("=" * 60)

    # Example 1: Get system info
    print("\n1. Get system information:")
    result = subprocess.run(['uname', '-a'], capture_output=True, text=True)
    print(f"   System: {result.stdout.strip()[:60]}...")

    # Example 2: File operations
    print("\n2. Count files in directory:")
    result = subprocess.run(
        ['sh', '-c', 'ls /tmp | wc -l'],
        capture_output=True,
        text=True
    )
    print(f"   Files in /tmp: {result.stdout.strip()}")

    # Example 3: Process information
    print("\n3. Current process info:")
    result = subprocess.run(['ps', '-p', str(os.getpid())], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')
    if len(lines) > 1:
        print(f"   {lines[1][:60]}...")


def demonstrate_background_processes() -> None:
    """Demonstrate running processes in background."""
    print("\n" + "=" * 60)
    print("BACKGROUND PROCESSES")
    print("=" * 60)

    # Start background process
    print("\n1. Starting background process:")
    process = subprocess.Popen(
        ['sleep', '0.5'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print(f"   Started process PID: {process.pid}")
    print(f"   Process running: {process.poll() is None}")

    # Wait for completion
    print("\n2. Waiting for completion...")
    process.wait()
    print(f"   Process completed: {process.returncode}")


def demonstrate_output_redirection() -> None:
    """Demonstrate output redirection to files."""
    print("\n" + "=" * 60)
    print("OUTPUT REDIRECTION")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Redirect to file
        print("\n1. Redirect stdout to file:")
        output_file = tmpdir / 'output.txt'
        with open(output_file, 'w') as f:
            subprocess.run(['echo', 'Hello, file!'], stdout=f)
        print(f"   Written to: {output_file.name}")
        print(f"   Content: {output_file.read_text().strip()}")

        # Redirect stderr to file
        print("\n2. Redirect stderr to file:")
        error_file = tmpdir / 'error.txt'
        with open(error_file, 'w') as f:
            subprocess.run(['ls', '/nonexistent'], stderr=f)
        print(f"   Error written to: {error_file.name}")


def main() -> None:
    """Main function demonstrating subprocess operations."""
    print("=" * 60)
    print("PYTHON SUBPROCESS MANAGEMENT")
    print("=" * 60)

    demonstrate_basic_subprocess()
    demonstrate_output_capture()
    demonstrate_input_handling()
    demonstrate_pipes()
    demonstrate_popen()
    demonstrate_error_handling()
    demonstrate_environment()
    demonstrate_working_directory()
    demonstrate_shell_injection_safety()
    demonstrate_real_world_examples()
    demonstrate_background_processes()
    demonstrate_output_redirection()

    print("\n" + "=" * 60)
    print("All subprocess operations completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
