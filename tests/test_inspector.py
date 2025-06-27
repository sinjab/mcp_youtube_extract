#!/usr/bin/env python3
"""
Test the MCP YouTube Extract server inspector functionality
"""
import asyncio
import os
import sys
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Load environment variables from .env file
load_dotenv()

async def inspect_server():
    """Inspect the MCP YouTube Extract server"""
    
    # Server parameters - using the working command from README
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_youtube_extract.server"],
        env=os.environ.copy()  # Include current environment
    )
    
    print("🔍 Connecting to MCP YouTube Extract server...")
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                print("✅ Connected successfully!")
                
                # Initialize the connection
                await session.initialize()
                print("✅ Session initialized!")
                
                # List available tools
                print("\n📋 Available tools:")
                tools_result = await session.list_tools()
                if hasattr(tools_result, 'tools'):
                    for tool in tools_result.tools:
                        print(f"  • {tool.name}: {tool.description}")
                        if hasattr(tool, 'inputSchema') and tool.inputSchema:
                            schema = tool.inputSchema
                            if 'properties' in schema:
                                print(f"    Parameters:")
                                for param, details in schema['properties'].items():
                                    required = param in schema.get('required', [])
                                    print(f"      - {param}: {details.get('description', 'No description')} {'(required)' if required else ''}")
                else:
                    print("  No tools found")
                
                # List available resources
                print("\n📁 Available resources:")
                try:
                    resources_result = await session.list_resources()
                    if hasattr(resources_result, 'resources') and resources_result.resources:
                        for resource in resources_result.resources:
                            print(f"  • {resource.name}: {resource.description}")
                    else:
                        print("  No resources found")
                except Exception as e:
                    print(f"  Error listing resources: {e}")
                
                # List available prompts
                print("\n💬 Available prompts:")
                try:
                    prompts_result = await session.list_prompts()
                    if hasattr(prompts_result, 'prompts') and prompts_result.prompts:
                        for prompt in prompts_result.prompts:
                            print(f"  • {prompt.name}: {prompt.description}")
                    else:
                        print("  No prompts found")
                except Exception as e:
                    print(f"  Error listing prompts: {e}")
                
                # Test the tool with a sample video ID (if you want to test with a real API key)
                print("\n🧪 Testing tool (without API key):")
                try:
                    result = await session.call_tool("get_yt_video_info", {"video_id": "dQw4w9WgXcQ"})
                    print("Tool result:")
                    if hasattr(result, 'content'):
                        for content in result.content:
                            if hasattr(content, 'text'):
                                print(f"  {content.text[:200]}...")
                            else:
                                print(f"  {content}")
                    else:
                        print(f"  {result}")
                except Exception as e:
                    print(f"  Expected error (no API key): {e}")
                
                print("\n✨ Inspection complete!")
                
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(inspect_server())
