"""Logging configuration for CTools."""

import logging
from pathlib import Path
from typing import Optional, Callable


class SignalHandler(logging.Handler):
    """A logging handler that calls a callback function for each log message."""

    def __init__(self, callback: Callable[[str], None]):
        super().__init__()
        self.callback = callback
        self.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            self.callback(msg)
        except Exception:
            self.handleError(record)


def setup_logging(
    level: int = logging.INFO,
    log_file: str = "info-log.txt",
    temp_file: Optional[str] = "output.tmp",
    signal_callback: Optional[Callable[[str], None]] = None
) -> None:
    """
    Configure logging with file and console handlers.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to the main log file
        temp_file: Path to temporary output file for GUI display (None to disable)
        signal_callback: Optional callback function to receive log messages in real-time
    """
    handlers = [
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]

    if temp_file:
        handlers.insert(1, logging.FileHandler(temp_file, mode='w'))

    if signal_callback:
        handlers.append(SignalHandler(signal_callback))

    logging.root.handlers = []
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=handlers
    )


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name."""
    return logging.getLogger(name)
