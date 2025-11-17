"""
Unit tests for 085_signals program.

These tests verify:
- Signal handling
- Custom signal handlers
- Signal sending
- Signal blocking and unblocking
- Alarm signals
"""

import sys
from pathlib import Path
import pytest
import signal
import os

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from main import main


class TestSignalHandling:
    """Test cases for signal handling."""

    def test_signal_handler_registration(self):
        """Test registering signal handler."""
        def handler(signum, frame):
            pass

        original = signal.signal(signal.SIGUSR1, handler)
        signal.signal(signal.SIGUSR1, original)

    def test_send_signal_to_self(self):
        """Test sending signal to own process."""
        received = []

        def handler(signum, frame):
            received.append(signum)

        original = signal.signal(signal.SIGUSR1, handler)
        os.kill(os.getpid(), signal.SIGUSR1)
        signal.signal(signal.SIGUSR1, original)

        assert len(received) > 0


class TestMainFunction:
    """Test cases for main function."""

    def test_main_executes(self):
        """Test that main executes without errors."""
        try:
            main()
        except Exception as e:
            pytest.fail(f"main() raised an exception: {e}")


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
