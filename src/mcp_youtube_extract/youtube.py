"""
YouTube API utilities for fetching video information and transcripts.
"""

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
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


def get_video_transcript(video_id: str, languages=['en']) -> str | None:
    """
    Fetch the transcript for a YouTube video with fallback logic.
    Priority: 1. Auto-generated, 2. English, 3. First available.
    
    This uses the exact same logic as the working CLI version.

    Args:
        video_id (str): The ID of the YouTube video.
        languages (list): A list of language codes to try for the English fallback.

    Returns:
        str: The video transcript text, or None if not found.
    """
    try:
        logger.info(f"Fetching transcript for video: {video_id}")
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = None

        # 1. Try to find an auto-generated transcript
        logger.info("Looking for auto-generated transcript...")
        for t in transcript_list:
            if t.is_generated:
                transcript = t
                logger.info("Found auto-generated transcript.")
                break
        
        # 2. If not found, try to find a transcript in the preferred languages (e.g., 'en')
        if not transcript:
            logger.info(f"Looking for transcript in preferred language: {languages}")
            try:
                transcript = transcript_list.find_transcript(languages)
                logger.info(f"Found transcript in preferred language: {languages}.")
            except Exception as e:
                logger.info(f"No transcript found in preferred languages: {e}")
                pass  # No transcript found in preferred languages

        # 3. If still not found, fall back to the first available one
        if not transcript:
            logger.info("Looking for first available transcript...")
            try:
                transcript = next(iter(transcript_list))
                logger.info("No preferred transcript found. Falling back to first available.")
            except StopIteration:
                logger.warning("No transcripts available for this video.")
                return None

        # Fetch the actual transcript
        logger.info(f"Fetching transcript content in '{transcript.language_code}' (auto-generated: {transcript.is_generated})")
        raw_transcript = transcript.fetch()
        logger.info(f"Successfully fetched transcript in '{transcript.language_code}' (auto-generated: {transcript.is_generated}).")

        # Format the transcript
        formatter = TextFormatter()
        formatted_transcript = formatter.format_transcript(raw_transcript)
        logger.info(f"Transcript formatted successfully: {len(formatted_transcript)} characters")
        return formatted_transcript

    except Exception as e:
        logger.error(f"Could not retrieve transcript: {e}")
        return f"Could not retrieve transcript: {e}"


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