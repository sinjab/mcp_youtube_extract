"""
Google API client utilities for fetching YouTube video information.
"""

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .logger import get_logger

logger = get_logger(__name__)


def get_video_info(api_key: str, video_id: str) -> dict | None:
    """
    Fetch detailed information about a YouTube video.
    This matches the working CLI code exactly.

    Args:
        api_key (str): Your YouTube Data API v3 key.
        video_id (str): The YouTube video ID.

    Returns:
        dict: Video information, or None if an error occurs.
    """
    try:
        logger.info(f"Fetching video info for: {video_id}")
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.videos().list(
            part='snippet,contentDetails,statistics,status',
            id=video_id
        )
        response = request.execute()

        if not response.get('items'):
            logger.warning("Video not found.")
            return None

        video_info = response['items'][0]
        snippet = video_info.get('snippet', {})
        logger.info(f"Successfully fetched video: '{snippet.get('title', 'Unknown')}'")
        return video_info

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None


def format_video_info(video_info: dict | None) -> str:
    """Format video information into a readable string."""
    if not video_info:
        logger.debug("No video info to format")
        return "Video not found or unavailable."
    
    snippet = video_info.get('snippet', {})
    result = []
    result.append(f"Title: {snippet.get('title', 'N/A')}")
    result.append(f"Channel: {snippet.get('channelTitle', 'N/A')}")
    result.append(f"Published: {snippet.get('publishedAt', 'N/A')}")
    result.append(f"Description: {snippet.get('description', 'N/A')}")
    
    formatted_info = "\n".join(result)
    logger.debug(f"Formatted video info: {len(formatted_info)} characters")
    return formatted_info
