"""
YouTube MCP Server

A simple MCP server that fetches YouTube video information and transcripts.
"""

import os
from mcp.server.fastmcp import FastMCP
from .youtube import get_video_info, get_video_transcript, format_video_info
from .logger import get_logger

logger = get_logger(__name__)

# Create the MCP server
mcp = FastMCP("YouTube Video Analyzer")

@mcp.tool()
def get_yt_video_info(video_id: str) -> str:
    """
    Fetch YouTube video information and transcript.
    
    Args:
        video_id: The YouTube video ID (e.g., 'dQw4w9WgXcQ' from https://youtube.com/watch?v=dQw4w9WgXcQ)
    
    Returns:
        A formatted string containing video information and transcript
    """
    logger.info(f"MCP tool called: get_yt_video_info with video_id: {video_id}")
    
    # Try to get API key from environment variable first, then from context
    api_key = os.getenv("YOUTUBE_API_KEY")
    
    if not api_key:
        logger.error("YOUTUBE_API_KEY not configured in server settings")
        return "Error: YOUTUBE_API_KEY not configured. Please set it in the server configuration."
    
    logger.info("API_KEY found successfully")
    result = []
    
    try:
        # Get video information
        logger.info(f"Processing video: {video_id}")
        video_info = get_video_info(api_key, video_id)
        result.append("=== VIDEO INFORMATION ===")
        result.append(format_video_info(video_info))
        result.append("")
        
        # Get transcript
        transcript = get_video_transcript(video_id)
        result.append("=== TRANSCRIPT ===")
        if transcript and not transcript.startswith("Transcript error:") and not transcript.startswith("Could not retrieve"):
            result.append(transcript)
            logger.info(f"Successfully processed video {video_id} with transcript")
        else:
            if transcript and (transcript.startswith("Transcript error:") or transcript.startswith("Could not retrieve")):
                result.append(f"Transcript issue: {transcript}")
                logger.warning(f"Transcript issue for video {video_id}: {transcript}")
            else:
                result.append("No transcript available for this video.")
                logger.warning(f"Video {video_id} processed but no transcript available")
        
        final_result = "\n".join(result)
        logger.debug(f"Tool execution completed for video {video_id}, result length: {len(final_result)} characters")
        return final_result
        
    except Exception as e:
        logger.error(f"Error processing video {video_id}: {e}", exc_info=True)
        return f"Error processing video {video_id}: {str(e)}"

def main():
    """Main entry point for the MCP server."""
    logger.info("Starting YouTube MCP Server")
    try:
        mcp.run()
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
