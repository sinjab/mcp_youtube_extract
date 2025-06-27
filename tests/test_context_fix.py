#!/usr/bin/env python3
"""
Test the fixed context API without environment variable to verify fallback works
"""
import asyncio
import os
import sys
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Load environment variables from .env file
load_dotenv()

async def test_context_fallback():
    """Test context API fallback mechanism"""
    
    # Explicitly remove API key from environment to test fallback
    env = os.environ.copy()
    if "YOUTUBE_API_KEY" in env:
        del env["YOUTUBE_API_KEY"]
    
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_youtube_extract.server"],
        env=env
    )
    
    print("🔍 Testing context API fallback (no env var)...")
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # This should fail gracefully without the context error
                try:
                    result = await session.call_tool("get_yt_video_info", {"video_id": "dQw4w9WgXcQ"})
                    if hasattr(result, 'content'):
                        content = result.content[0].text
                        if "YOUTUBE_API_KEY not configured" in content and "Failed to get context" not in content:
                            print("✅ Context API fix successful! Clean error handling without context errors.")
                        else:
                            print("⚠️  Unexpected error message format")
                    else:
                        print(f"Raw result: {result}")
                        
                except Exception as e:
                    print(f"Error (expected): {e}")
                
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    asyncio.run(test_context_fallback())
