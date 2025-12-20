import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
import json
from datetime import datetime

from app.config import CURRENT_LOGGING_CONFIG


class CustomFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""

    # Color codes
    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format_str + reset,
        logging.INFO: blue + format_str + reset,
        logging.WARNING: yellow + format_str + reset,
        logging.ERROR: red + format_str + reset,
        logging.CRITICAL: bold_red + format_str + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


class JSONFormatter(logging.Formatter):
    """JSON formatter for file output"""

    def format(self, record):
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record)


def setup_logger(
    name: str,
    log_level: str = CURRENT_LOGGING_CONFIG["log_level"],
    log_dir: Path = CURRENT_LOGGING_CONFIG["log_dir"],
) -> logging.Logger:
    """
    Set up a logger with both console and file handlers

    Args:
        name: Name of the logger
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory for log files

    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))

    # Remove existing handlers
    logger.handlers = []

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(CustomFormatter())
    logger.addHandler(console_handler)

    # File Handler (if log_dir is provided)
    if log_dir:
        log_dir = Path(log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)

        # Regular log file
        file_handler = RotatingFileHandler(
            filename=log_dir / f"{name}.log",
            maxBytes=10485760,  # 10MB
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setFormatter(JSONFormatter())
        logger.addHandler(file_handler)

        # Error log file
        error_handler = RotatingFileHandler(
            filename=log_dir / f"{name}.error.log",
            maxBytes=10485760,  # 10MB
            backupCount=5,
            encoding="utf-8",
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(JSONFormatter())
        logger.addHandler(error_handler)

    return logger
