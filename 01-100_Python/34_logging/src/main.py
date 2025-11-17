#!/usr/bin/env python3
"""Program 34: Logging - Master Python's logging framework."""

import logging
import logging.handlers
import sys
import io
from typing import Any


def demonstrate_basic_logging() -> dict[str, Any]:
    """Demonstrate basic logging functionality."""

    # Create string buffer to capture logs
    log_stream = io.StringIO()
    handler = logging.StreamHandler(log_stream)
    handler.setLevel(logging.DEBUG)

    # Create logger
    logger = logging.getLogger('basic_demo')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    # Log at different levels
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")

    logs = log_stream.getvalue()
    log_lines = [l for l in logs.split('\n') if l]

    return {
        "log_count": len(log_lines),
        "levels": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        "note": "Five standard log levels, DEBUG < INFO < WARNING < ERROR < CRITICAL",
    }


def demonstrate_logger_hierarchy() -> dict[str, Any]:
    """Demonstrate logger hierarchy."""

    # Create loggers in hierarchy
    root_logger = logging.getLogger()
    app_logger = logging.getLogger('myapp')
    module_logger = logging.getLogger('myapp.module')
    submodule_logger = logging.getLogger('myapp.module.submodule')

    logger_names = [
        root_logger.name or "root",
        app_logger.name,
        module_logger.name,
        submodule_logger.name,
    ]

    # Child loggers propagate to parents
    return {
        "logger_names": logger_names,
        "hierarchy": "root -> myapp -> myapp.module -> myapp.module.submodule",
        "note": "Loggers form hierarchy based on dot-separated names",
    }


def demonstrate_formatters() -> dict[str, Any]:
    """Demonstrate log formatters."""

    log_stream = io.StringIO()

    # Create handler with custom format
    handler = logging.StreamHandler(log_stream)

    # Custom format
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)

    logger = logging.getLogger('format_demo')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False

    logger.info("Test message")

    log_output = log_stream.getvalue()

    # Different format styles
    formats = {
        "basic": "%(levelname)s:%(name)s:%(message)s",
        "detailed": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "with_location": "%(pathname)s:%(lineno)d - %(message)s",
    }

    return {
        "sample_output": log_output.strip()[:50] + "...",
        "available_formats": list(formats.keys()),
        "note": "Formatters control log message appearance",
    }


def demonstrate_handlers() -> dict[str, Any]:
    """Demonstrate different log handlers."""

    logger = logging.getLogger('handler_demo')
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    # StreamHandler (stdout/stderr)
    stream_handler = logging.StreamHandler(sys.stdout)

    # FileHandler (writes to file)
    file_handler = logging.FileHandler('/tmp/test.log', mode='w')

    # MemoryHandler (buffers logs)
    memory_handler = logging.handlers.MemoryHandler(
        capacity=10,
        target=stream_handler
    )

    handler_types = [
        type(stream_handler).__name__,
        type(file_handler).__name__,
        type(memory_handler).__name__,
    ]

    # Clean up
    file_handler.close()

    return {
        "handler_types": handler_types,
        "note": "Different handlers for console, file, network, etc.",
    }


def demonstrate_filters() -> dict[str, Any]:
    """Demonstrate log filters."""

    class LevelFilter(logging.Filter):
        """Filter that only allows specific levels."""

        def __init__(self, levels):
            super().__init__()
            self.levels = levels

        def filter(self, record):
            return record.levelno in self.levels

    log_stream = io.StringIO()
    handler = logging.StreamHandler(log_stream)

    # Only allow WARNING and ERROR
    handler.addFilter(LevelFilter([logging.WARNING, logging.ERROR]))

    logger = logging.getLogger('filter_demo')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.propagate = False

    # Try different levels
    logger.debug("Debug - filtered out")
    logger.info("Info - filtered out")
    logger.warning("Warning - allowed")
    logger.error("Error - allowed")
    logger.critical("Critical - filtered out")

    logs = log_stream.getvalue()
    log_count = len([l for l in logs.split('\n') if l])

    return {
        "filtered_log_count": log_count,
        "expected": 2,
        "note": "Filters provide fine-grained control over log records",
    }


def demonstrate_configuration() -> dict[str, Any]:
    """Demonstrate logging configuration."""

    # Dictionary-based configuration
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '%(levelname)s - %(message)s'
            },
            'detailed': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'simple',
                'stream': 'ext://sys.stdout',
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
    }

    # Apply configuration
    logging.config.dictConfig(config)

    return {
        "config_version": config['version'],
        "formatters": list(config['formatters'].keys()),
        "handlers": list(config['handlers'].keys()),
        "note": "dictConfig() configures logging from dictionary",
    }


def demonstrate_contextual_logging() -> dict[str, Any]:
    """Demonstrate contextual logging with extra."""

    log_stream = io.StringIO()
    handler = logging.StreamHandler(log_stream)
    formatter = logging.Formatter(
        '%(name)s - %(levelname)s - %(user)s - %(message)s'
    )
    handler.setFormatter(formatter)

    logger = logging.getLogger('context_demo')
    logger.addHandler(handler)
    logger.propagate = False

    # Log with context
    logger.info("User logged in", extra={'user': 'alice'})
    logger.info("Action performed", extra={'user': 'bob'})

    logs = log_stream.getvalue()

    return {
        "logs": logs.strip().split('\n'),
        "note": "extra dict adds context to log records",
    }


def demonstrate_exception_logging() -> dict[str, Any]:
    """Demonstrate logging exceptions."""

    log_stream = io.StringIO()
    handler = logging.StreamHandler(log_stream)

    logger = logging.getLogger('exception_demo')
    logger.addHandler(handler)
    logger.propagate = False

    # Log exception with traceback
    try:
        result = 10 / 0
    except ZeroDivisionError:
        logger.exception("Division by zero occurred")

    # Log exception without traceback
    try:
        int("not a number")
    except ValueError as e:
        logger.error(f"Value error: {e}")

    logs = log_stream.getvalue()
    has_traceback = "Traceback" in logs

    return {
        "has_traceback": has_traceback,
        "note": "logger.exception() automatically includes traceback",
    }


def demonstrate_rotating_file_handler() -> dict[str, Any]:
    """Demonstrate rotating file handlers."""

    # Size-based rotation
    size_handler = logging.handlers.RotatingFileHandler(
        '/tmp/rotating.log',
        maxBytes=1024,
        backupCount=3
    )

    # Time-based rotation
    time_handler = logging.handlers.TimedRotatingFileHandler(
        '/tmp/timed.log',
        when='midnight',
        interval=1,
        backupCount=7
    )

    handler_info = {
        "size_rotation": "RotatingFileHandler - rotates by size",
        "time_rotation": "TimedRotatingFileHandler - rotates by time",
        "max_bytes": size_handler.maxBytes,
        "backup_count": size_handler.backupCount,
    }

    # Clean up
    size_handler.close()
    time_handler.close()

    return {
        **handler_info,
        "note": "Rotating handlers prevent log files from growing indefinitely",
    }


def demonstrate_logger_adapter() -> dict[str, Any]:
    """Demonstrate LoggerAdapter for adding context."""

    log_stream = io.StringIO()
    handler = logging.StreamHandler(log_stream)
    formatter = logging.Formatter('%(levelname)s - %(message)s - [%(request_id)s]')
    handler.setFormatter(formatter)

    logger = logging.getLogger('adapter_demo')
    logger.addHandler(handler)
    logger.propagate = False

    # Create adapter with context
    class ContextAdapter(logging.LoggerAdapter):
        def process(self, msg, kwargs):
            # Add default context
            if 'extra' not in kwargs:
                kwargs['extra'] = {}
            kwargs['extra'].update(self.extra)
            return msg, kwargs

    # Use adapter
    adapter = ContextAdapter(logger, {'request_id': '12345'})
    adapter.info("Request started")
    adapter.info("Request completed")

    logs = log_stream.getvalue()
    has_request_id = "12345" in logs

    return {
        "has_request_id": has_request_id,
        "note": "LoggerAdapter adds context to all log calls",
    }


def main() -> None:
    """Main demonstration function."""
    print("=" * 60)
    print("Program 34: Logging")
    print("=" * 60)

    print("\n1. Basic Logging:")
    basic = demonstrate_basic_logging()
    for key, value in basic.items():
        print(f"   {key}: {value}")

    print("\n2. Logger Hierarchy:")
    hierarchy = demonstrate_logger_hierarchy()
    for key, value in hierarchy.items():
        print(f"   {key}: {value}")

    print("\n3. Formatters:")
    formatters = demonstrate_formatters()
    for key, value in formatters.items():
        print(f"   {key}: {value}")

    print("\n4. Handlers:")
    handlers = demonstrate_handlers()
    for key, value in handlers.items():
        print(f"   {key}: {value}")

    print("\n5. Filters:")
    filters = demonstrate_filters()
    for key, value in filters.items():
        print(f"   {key}: {value}")

    print("\n6. Configuration:")
    config = demonstrate_configuration()
    for key, value in config.items():
        print(f"   {key}: {value}")

    print("\n7. Contextual Logging:")
    contextual = demonstrate_contextual_logging()
    for key, value in contextual.items():
        print(f"   {key}: {value}")

    print("\n8. Exception Logging:")
    exceptions = demonstrate_exception_logging()
    for key, value in exceptions.items():
        print(f"   {key}: {value}")

    print("\n9. Rotating Handlers:")
    rotating = demonstrate_rotating_file_handler()
    for key, value in rotating.items():
        print(f"   {key}: {value}")

    print("\n10. Logger Adapter:")
    adapter = demonstrate_logger_adapter()
    for key, value in adapter.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Program completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
