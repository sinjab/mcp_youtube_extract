"""
MCP YouTube Extract - A Model Context Protocol server for YouTube operations
"""

from .logger import get_logger
from .server import mcp, main
from .google_api import get_video_info, format_video_info
from .transcript_api import get_video_transcript

logger = get_logger(__name__)

__version__ = "0.1.0"

logger.info(f"MCP YouTube Extract package initialized, version: {__version__}")

__all__ = [
    "mcp",
    "main",
    "get_video_info",
    "get_video_transcript", 
    "format_video_info",
]
