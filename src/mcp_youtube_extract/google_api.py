"""
yt-info-extract utilities for fetching YouTube video information.
"""

from yt_info_extract import get_video_info as yt_get_video_info
from .logger import get_logger

logger = get_logger(__name__)


def get_video_info(api_key: str, video_id: str) -> dict | None:
    """
    Fetch detailed information about a YouTube video using yt-info-extract.
    
    Args:
        api_key (str): YouTube Data API v3 key (optional with yt-info-extract).
        video_id (str): The YouTube video ID.

    Returns:
        dict: Video information in yt-info-extract format, or None if an error occurs.
    """
    try:
        logger.info(f"Fetching video info for: {video_id}")
        
        # Use yt-info-extract to get video information
        video_info = yt_get_video_info(video_id)
        
        if not video_info:
            logger.warning("Video not found.")
            return None

        logger.info(f"Successfully fetched video: '{video_info.get('title', 'Unknown')}'")
        return video_info

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None


def format_video_info(video_info: dict | None) -> str:
    """Format video information into a readable string."""
    if not video_info:
        logger.debug("No video info to format")
        return "Video not found or unavailable."
    
    # yt-info-extract returns data in different format than Google API
    result = []
    result.append(f"Title: {video_info.get('title', 'N/A')}")
    result.append(f"Channel: {video_info.get('channel_name', 'N/A')}")
    result.append(f"Published: {video_info.get('publication_date', 'N/A')}")
    result.append(f"Views: {video_info.get('views', 'N/A'):,}" if video_info.get('views') else "Views: N/A")
    result.append(f"Description: {video_info.get('description', 'N/A')}")
    
    formatted_info = "\n".join(result)
    logger.debug(f"Formatted video info: {len(formatted_info)} characters")
    return formatted_info
