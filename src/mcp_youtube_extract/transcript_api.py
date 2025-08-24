"""
YouTube transcript API utilities for fetching video transcripts using yt-ts-extract.
"""

from yt_ts_extract import (
    get_transcript,
    get_transcript_text,
    get_available_languages,
    YouTubeTranscriptExtractor,
)
from .logger import get_logger

logger = get_logger(__name__)


def get_video_transcript(video_id: str, languages=['en']) -> str | None:
    """
    Fetch the transcript for a YouTube video with fallback logic.
    Priority: 1. Auto-generated, 2. English, 3. First available.
    
    This uses yt-ts-extract which provides robust transcript extraction.

    Args:
        video_id (str): The ID of the YouTube video.
        languages (list): A list of language codes to try for the English fallback.

    Returns:
        str: The video transcript text, or None if not found.
    """
    try:
        logger.info(f"Fetching transcript for video: {video_id}")
        
        # Create extractor with reasonable defaults
        extractor = YouTubeTranscriptExtractor(
            timeout=30,
            max_retries=3,
            backoff_factor=0.75,
            min_delay=2.0
        )
        
        # First, try to get available languages to understand what's available
        try:
            available_langs = get_available_languages(video_id)
            logger.info(f"Available languages: {[lang['code'] for lang in available_langs]}")
        except Exception as e:
            logger.info(f"Could not get available languages: {e}")
            available_langs = []

        # Try to get transcript in preferred language first
        transcript = None
        for lang in languages:
            try:
                logger.info(f"Trying to get transcript in language: {lang}")
                transcript = extractor.get_transcript(video_id, language=lang)
                if transcript:
                    logger.info(f"Successfully got transcript in language: {lang}")
                    break
            except Exception as e:
                logger.info(f"Failed to get transcript in {lang}: {e}")
                continue
        
        # If no transcript found in preferred languages, try to get any available
        if not transcript:
            logger.info("No transcript found in preferred languages, trying any available...")
            try:
                transcript = get_transcript(video_id)
                if transcript:
                    logger.info("Found transcript in any available language")
            except Exception as e:
                logger.info(f"Failed to get any transcript: {e}")
        
        # If still no transcript, try the simple text function as last resort
        if not transcript:
            logger.info("Trying simple transcript text extraction...")
            try:
                text = get_transcript_text(video_id)
                if text:
                    logger.info("Successfully got transcript text")
                    return text
            except Exception as e:
                logger.info(f"Failed to get transcript text: {e}")
        
        # If we have transcript segments, convert to text
        if transcript:
            # Convert segments to plain text
            text_parts = []
            for segment in transcript:
                if isinstance(segment, dict) and 'text' in segment:
                    text_parts.append(segment['text'])
                elif isinstance(segment, str):
                    text_parts.append(segment)
            
            if text_parts:
                formatted_transcript = ' '.join(text_parts)
                logger.info(f"Transcript formatted successfully: {len(formatted_transcript)} characters")
                return formatted_transcript
        
        logger.warning("No transcripts available for this video.")
        return None

    except Exception as e:
        logger.error(f"Could not retrieve transcript: {e}")
        return f"Could not retrieve transcript: {e}"
