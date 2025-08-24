"""
YouTube transcript API utilities for fetching video transcripts.
"""

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from .logger import get_logger

logger = get_logger(__name__)


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
