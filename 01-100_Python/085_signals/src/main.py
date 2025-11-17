#!/usr/bin/env python3
"""
Program 85: Signal Handling
Demonstrates signal handling, SIGTERM, SIGINT, and custom signals.
"""

import signal
import sys
import time
import os
from typing import Callable, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SignalInfo:
    """Store signal information."""
    signal_num: int
    signal_name: str
    received_at: str
    count: int = 0


# Global signal counter
signal_counts = {}


def signal_handler(signum: int, frame) -> None:
    """Generic signal handler."""
    signal_name = signal.Signals(signum).name
    timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]

    if signum not in signal_counts:
        signal_counts[signum] = 0
    signal_counts[signum] += 1

    print(f"\n[{timestamp}] Received signal: {signal_name} ({signum})")
    print(f"   Count: {signal_counts[signum]}")


def demonstrate_signal_basics() -> None:
    """Demonstrate basic signal concepts."""
    print("\n" + "=" * 60)
    print("SIGNAL BASICS")
    print("=" * 60)

    print("\n1. Available signals:")
    common_signals = [
        signal.SIGINT,
        signal.SIGTERM,
        signal.SIGUSR1,
        signal.SIGUSR2,
        signal.SIGALRM,
    ]

    for sig in common_signals:
        print(f"   {signal.Signals(sig).name}: {sig}")

    print("\n2. Current process ID:")
    print(f"   PID: {os.getpid()}")


def demonstrate_sigint_handler() -> None:
    """Demonstrate SIGINT (Ctrl+C) handling."""
    print("\n" + "=" * 60)
    print("SIGINT HANDLER")
    print("=" * 60)

    def sigint_handler(signum, frame):
        print("\n   ✓ SIGINT received (Ctrl+C pressed)")
        print("   Graceful shutdown initiated...")

    # Register handler
    original_handler = signal.signal(signal.SIGINT, sigint_handler)
    print("\n1. SIGINT handler registered")
    print("   (Handler would catch Ctrl+C)")

    # Restore original handler
    signal.signal(signal.SIGINT, original_handler)
    print("2. Original handler restored")


def demonstrate_sigterm_handler() -> None:
    """Demonstrate SIGTERM handling."""
    print("\n" + "=" * 60)
    print("SIGTERM HANDLER")
    print("=" * 60)

    cleanup_done = False

    def sigterm_handler(signum, frame):
        nonlocal cleanup_done
        print("\n   ✓ SIGTERM received")
        print("   Performing cleanup...")
        cleanup_done = True

    # Register handler
    original_handler = signal.signal(signal.SIGTERM, sigterm_handler)
    print("\n1. SIGTERM handler registered")
    print(f"   PID: {os.getpid()}")
    print("   (Can send: kill -TERM <pid>)")

    # Simulate SIGTERM
    try:
        os.kill(os.getpid(), signal.SIGTERM)
        print(f"2. Cleanup done: {cleanup_done}")
    except Exception as e:
        print(f"   Error: {e}")

    # Restore original handler
    signal.signal(signal.SIGTERM, original_handler)


def demonstrate_sigusr_signals() -> None:
    """Demonstrate user-defined signals."""
    print("\n" + "=" * 60)
    print("USER-DEFINED SIGNALS (SIGUSR1, SIGUSR2)")
    print("=" * 60)

    state = {'sigusr1_count': 0, 'sigusr2_count': 0}

    def sigusr1_handler(signum, frame):
        state['sigusr1_count'] += 1
        print(f"\n   ✓ SIGUSR1 received (count: {state['sigusr1_count']})")

    def sigusr2_handler(signum, frame):
        state['sigusr2_count'] += 1
        print(f"\n   ✓ SIGUSR2 received (count: {state['sigusr2_count']})")

    # Register handlers
    old_usr1 = signal.signal(signal.SIGUSR1, sigusr1_handler)
    old_usr2 = signal.signal(signal.SIGUSR2, sigusr2_handler)

    print("\n1. SIGUSR1 and SIGUSR2 handlers registered")

    # Send signals to self
    print("\n2. Sending signals to self:")
    os.kill(os.getpid(), signal.SIGUSR1)
    time.sleep(0.1)
    os.kill(os.getpid(), signal.SIGUSR2)
    time.sleep(0.1)
    os.kill(os.getpid(), signal.SIGUSR1)

    print(f"\n3. Final counts:")
    print(f"   SIGUSR1: {state['sigusr1_count']}")
    print(f"   SIGUSR2: {state['sigusr2_count']}")

    # Restore handlers
    signal.signal(signal.SIGUSR1, old_usr1)
    signal.signal(signal.SIGUSR2, old_usr2)


def demonstrate_alarm_signal() -> None:
    """Demonstrate SIGALRM for timeouts."""
    print("\n" + "=" * 60)
    print("ALARM SIGNAL (SIGALRM)")
    print("=" * 60)

    alarm_triggered = False

    def alarm_handler(signum, frame):
        nonlocal alarm_triggered
        alarm_triggered = True
        print("\n   ✓ SIGALRM - Alarm triggered!")

    # Register handler
    old_handler = signal.signal(signal.SIGALRM, alarm_handler)

    print("\n1. Setting alarm for 1 second:")
    signal.alarm(1)
    print("   Waiting...")

    time.sleep(1.5)

    print(f"2. Alarm triggered: {alarm_triggered}")

    # Cancel any pending alarm
    signal.alarm(0)

    # Restore handler
    signal.signal(signal.SIGALRM, old_handler)


def demonstrate_signal_ignore() -> None:
    """Demonstrate ignoring signals."""
    print("\n" + "=" * 60)
    print("IGNORING SIGNALS")
    print("=" * 60)

    # Save original handler
    original_handler = signal.signal(signal.SIGUSR1, signal.SIG_IGN)

    print("\n1. SIGUSR1 set to ignore (SIG_IGN)")

    # Send signal (will be ignored)
    os.kill(os.getpid(), signal.SIGUSR1)
    print("2. Sent SIGUSR1 - signal ignored")

    # Restore handler
    signal.signal(signal.SIGUSR1, original_handler)
    print("3. Handler restored")


def demonstrate_signal_default() -> None:
    """Demonstrate default signal handlers."""
    print("\n" + "=" * 60)
    print("DEFAULT SIGNAL HANDLERS")
    print("=" * 60)

    print("\n1. Setting signal to default behavior:")
    print("   SIG_DFL restores default handling")

    # Example: Set SIGUSR1 to default
    signal.signal(signal.SIGUSR1, signal.SIG_DFL)
    print("2. SIGUSR1 set to SIG_DFL")

    # Note: Can't easily demonstrate default behavior
    # as it would terminate/affect the process
    print("3. (Default handlers vary by signal)")


def demonstrate_context_manager() -> None:
    """Demonstrate signal handling with context manager."""
    print("\n" + "=" * 60)
    print("SIGNAL CONTEXT MANAGER")
    print("=" * 60)

    class SignalHandler:
        """Context manager for temporary signal handlers."""

        def __init__(self, signum: int, handler: Callable):
            self.signum = signum
            self.handler = handler
            self.old_handler = None

        def __enter__(self):
            self.old_handler = signal.signal(self.signum, self.handler)
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            signal.signal(self.signum, self.old_handler)

    def temp_handler(signum, frame):
        print("   ✓ Temporary handler called")

    print("\n1. Using context manager for temporary handler:")
    print("   Handler active only in context")

    with SignalHandler(signal.SIGUSR1, temp_handler):
        print("2. Inside context - sending signal:")
        os.kill(os.getpid(), signal.SIGUSR1)

    print("3. Outside context - handler restored")


def demonstrate_signal_masks() -> None:
    """Demonstrate signal masking (blocking)."""
    print("\n" + "=" * 60)
    print("SIGNAL MASKING")
    print("=" * 60)

    print("\n1. Signal masking allows blocking signals temporarily")
    print("   (Not available on all platforms)")

    try:
        # Block SIGUSR1
        old_mask = signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGUSR1])
        print("2. SIGUSR1 blocked")

        # Send signal while blocked
        os.kill(os.getpid(), signal.SIGUSR1)
        print("3. Sent SIGUSR1 (currently blocked)")

        # Unblock
        signal.pthread_sigmask(signal.SIG_SETMASK, old_mask)
        print("4. SIGUSR1 unblocked")

    except AttributeError:
        print("2. pthread_sigmask not available on this platform")


def demonstrate_graceful_shutdown() -> None:
    """Demonstrate graceful shutdown pattern."""
    print("\n" + "=" * 60)
    print("GRACEFUL SHUTDOWN PATTERN")
    print("=" * 60)

    class Application:
        """Application with graceful shutdown."""

        def __init__(self):
            self.running = True
            self.shutdown_requested = False

        def signal_handler(self, signum, frame):
            sig_name = signal.Signals(signum).name
            print(f"\n   Received {sig_name} - initiating shutdown")
            self.shutdown_requested = True
            self.running = False

        def setup_signals(self):
            """Setup signal handlers."""
            signal.signal(signal.SIGINT, self.signal_handler)
            signal.signal(signal.SIGTERM, self.signal_handler)

        def cleanup(self):
            """Cleanup resources."""
            print("   Cleaning up resources...")
            time.sleep(0.1)
            print("   ✓ Cleanup complete")

        def run(self):
            """Main application loop."""
            print("\n1. Application running...")
            print("   (Simulating work for 0.5 seconds)")

            start_time = time.time()
            while self.running and (time.time() - start_time < 0.5):
                time.sleep(0.1)

            if self.shutdown_requested:
                print("2. Shutdown requested - cleaning up")
                self.cleanup()
            else:
                print("2. Normal completion")

    app = Application()
    app.setup_signals()
    print("\nGraceful shutdown pattern:")
    app.run()


def demonstrate_signal_safety() -> None:
    """Demonstrate signal handler safety."""
    print("\n" + "=" * 60)
    print("SIGNAL HANDLER SAFETY")
    print("=" * 60)

    print("\n1. Signal handler best practices:")
    print("   ✓ Keep handlers short and simple")
    print("   ✓ Avoid complex operations")
    print("   ✓ Don't call non-reentrant functions")
    print("   ✓ Set flags instead of complex logic")

    print("\n2. Safe pattern - flag setting:")

    safe_flag = False

    def safe_handler(signum, frame):
        nonlocal safe_flag
        safe_flag = True  # Just set a flag

    old_handler = signal.signal(signal.SIGUSR1, safe_handler)
    os.kill(os.getpid(), signal.SIGUSR1)
    time.sleep(0.1)

    if safe_flag:
        print("   ✓ Flag set by handler")
        print("   Main code can now handle the signal safely")

    signal.signal(signal.SIGUSR1, old_handler)


def demonstrate_multiple_signals() -> None:
    """Demonstrate handling multiple signals."""
    print("\n" + "=" * 60)
    print("HANDLING MULTIPLE SIGNALS")
    print("=" * 60)

    received_signals = []

    def multi_handler(signum, frame):
        sig_name = signal.Signals(signum).name
        received_signals.append(sig_name)
        print(f"   Received: {sig_name}")

    # Register same handler for multiple signals
    signals_to_handle = [signal.SIGUSR1, signal.SIGUSR2, signal.SIGTERM]
    old_handlers = {}

    print("\n1. Registering handler for multiple signals:")
    for sig in signals_to_handle:
        old_handlers[sig] = signal.signal(sig, multi_handler)
        print(f"   {signal.Signals(sig).name}")

    # Send multiple signals
    print("\n2. Sending signals:")
    for sig in signals_to_handle:
        os.kill(os.getpid(), sig)
        time.sleep(0.05)

    print(f"\n3. Received signals: {received_signals}")

    # Restore handlers
    for sig, handler in old_handlers.items():
        signal.signal(sig, handler)


def main() -> None:
    """Main function demonstrating signal handling."""
    print("=" * 60)
    print("PYTHON SIGNAL HANDLING")
    print("=" * 60)

    demonstrate_signal_basics()
    demonstrate_sigint_handler()
    demonstrate_sigterm_handler()
    demonstrate_sigusr_signals()
    demonstrate_alarm_signal()
    demonstrate_signal_ignore()
    demonstrate_signal_default()
    demonstrate_context_manager()
    demonstrate_signal_masks()
    demonstrate_graceful_shutdown()
    demonstrate_signal_safety()
    demonstrate_multiple_signals()

    print("\n" + "=" * 60)
    print("All signal handling demonstrations completed!")
    print("=" * 60)
    print("\nNote: Some signals may behave differently based on platform")
    print("and system configuration.")


if __name__ == "__main__":
    main()
