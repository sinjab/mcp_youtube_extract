"""
Centralized logger - provides consistent logging across all modules
"""

import logging
from pathlib import Path
from typing import Optional, Dict, Any

# Create logs directory if it doesn't exist
# Go up to project root: src/mcp_youtube_extract/logger.py -> src/mcp_youtube_extract -> src -> project_root (mcp_youtube_extract)
log_dir = Path(__file__).parent.parent.parent / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "mcp_youtube_extract.log"

# Define a formatter that includes filename and line number
FORMATTER = logging.Formatter(
    '%(asctime)s - %(name)s - [%(filename)s:%(lineno)d] - %(levelname)s - %(message)s'
)

# More detailed formatter for debugging
DEBUG_FORMATTER = logging.Formatter(
    '%(asctime)s - %(name)s:%(lineno)d - %(funcName)s - %(levelname)s - %(message)s'
)

# Root logger for the package
ROOT_LOGGER_NAME = "mcp_youtube_extract"

# Configure root logger once
root_logger = logging.getLogger(ROOT_LOGGER_NAME)
root_logger.setLevel(logging.INFO)

# Prevent adding handlers multiple times
if not root_logger.handlers:
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(FORMATTER)
    root_logger.addHandler(file_handler)
    
    # Console handler - only show warnings and errors by default
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(FORMATTER)
    console_handler.setLevel(logging.ERROR)
    root_logger.addHandler(console_handler)


def get_logger(module_name: str) -> logging.Logger:
    """
    Get a logger instance for the given module name.
    Typically, module_name should be __name__ from the calling module.
    This ensures the logger is part of the application's logging hierarchy,
    inheriting configuration from the root logger ('mcp_youtube_extract').
    
    Args:
        module_name: The name for the logger (e.g., __name__ from the calling module).
        
    Returns:
        A logger instance.
    """
    return logging.getLogger(module_name)


def set_log_level(level: int) -> None:
    """
    Set the log level for the root logger.
    
    Args:
        level: The logging level (e.g., logging.DEBUG, logging.INFO)
    """
    root_logger.setLevel(level)
    
    # Update file handler level
    for handler in root_logger.handlers:
        if isinstance(handler, logging.FileHandler):
            handler.setLevel(level)
            # If DEBUG level, use more detailed formatter
            if level == logging.DEBUG:
                handler.setFormatter(DEBUG_FORMATTER)
            else:
                handler.setFormatter(FORMATTER)


def log_dict(logger_instance: logging.Logger, level: int, message: str, data: Dict[str, Any]) -> None:
    """
    Log a dictionary with a given message at the specified level
    
    Args:
        logger_instance: The logger to use
        level: Logging level
        message: Message to include
        data: Dictionary to log
    """
    logger_instance.log(level, f"{message}: {data}")


def log_exception(logger_instance: logging.Logger, message: str, exc_info: Optional[bool] = True) -> None:
    """
    Log an exception with full traceback
    
    Args:
        logger_instance: The logger to use
        message: Message to include
        exc_info: Whether to include exception info (defaults to True)
    """
    logger_instance.exception(message, exc_info=exc_info) 
