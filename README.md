# MCP YouTube Extract

[![PyPI version](https://badge.fury.io/py/mcp-youtube-extract.svg)](https://badge.fury.io/py/mcp-youtube-extract)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Model Context Protocol (MCP) server for YouTube operations, demonstrating core MCP concepts including tools and logging.

## Features

- **MCP Server**: A fully functional MCP server with:
  - **Tools**: Extract information from YouTube videos including metadata and transcripts
  - **Comprehensive Logging**: Detailed logging throughout the application
  - **Error Handling**: Robust error handling with fallback logic for transcripts
- **YouTube Integration**: Built-in YouTube API capabilities:
  - Extract video information (title, description, channel, publish date)
  - Get video transcripts with intelligent fallback logic
  - Support for both manually created and auto-generated transcripts

## 📦 Available on PyPI

This package is now available on PyPI! You can install it directly with:

```bash
pip install mcp-youtube-extract
```

Visit the package page: [mcp-youtube-extract on PyPI](https://pypi.org/project/mcp-youtube-extract/)

## Installation

### Quick Start (Recommended)

The easiest way to get started is to install from PyPI:

```bash
pip install mcp-youtube-extract
```

Or using pipx (recommended for command-line tools):

```bash
pipx install mcp-youtube-extract
```

This will install the latest version with all dependencies. You can then run the MCP server directly:

```bash
mcp_youtube_extract
```

### Using uv (Development)

For development or if you prefer uv:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install the project
git clone https://github.com/sinjab/mcp_youtube_extract.git
cd mcp_youtube_extract

# Install dependencies (including dev dependencies)
uv sync --dev

# Set up your API key for development
cp .env.example .env
# Edit .env and add your YouTube API key
```

### From source

1. Clone the repository:
   ```bash
   git clone https://github.com/sinjab/mcp_youtube_extract.git
   cd mcp_youtube_extract
   ```

2. Install in development mode:
   ```bash
   uv sync --dev
   ```

## Configuration

### Environment Variables

For **development**, create a `.env` file in the project root with your YouTube API key:

```bash
# YouTube API Configuration
YOUTUBE_API_KEY=your_youtube_api_key_here
```

For **production**, set the environment variable directly in your system:

```bash
export YOUTUBE_API_KEY=your_youtube_api_key_here
```

**Required:**
- `YOUTUBE_API_KEY`: Your YouTube Data API key (required for video metadata)

## Usage

### Running the MCP Server

#### Using PyPI Installation (Recommended)

```bash
# Install from PyPI
pip install mcp-youtube-extract

# Run the server
mcp_youtube_extract
```

#### Using Development Setup

```bash
# Using uv
uv run mcp_youtube_extract

# Or directly
python -m mcp_youtube_extract.server
```

### Running Tests

```bash
# Run all pytest tests
uv run pytest

# Run specific pytest test
uv run pytest tests/test_with_api_key.py

# Run tests with coverage
uv run pytest --cov=src/mcp_youtube_extract --cov-report=term-missing
```

**Note**: The `tests/` directory contains 4 files:
- `test_context_fix.py` - Pytest test for context API fallback functionality
- `test_with_api_key.py` - Pytest test for full functionality with API key  
- `test_youtube_unit.py` - **Unit tests** for core YouTube functionality
- `test_inspector.py` - **Standalone inspection script** (not a pytest test)

**Test Coverage**: The project currently has 62% overall coverage with excellent coverage of core functionality:
- `youtube.py`: 81% coverage (core business logic)
- `logger.py`: 73% coverage (logging utilities)
- `server.py`: 22% coverage (MCP protocol handling)
- `__init__.py`: 100% coverage (package initialization)

### Running the Inspection Script

The `test_inspector.py` file is a standalone script that connects to the MCP server and validates its functionality:

```bash
# Run the inspection script to test server connectivity and functionality
uv run python tests/test_inspector.py
```

This script will:
- Connect to the MCP server
- List available tools, resources, and prompts
- Test the `get_yt_video_info` tool with a sample video
- Validate that the server is working correctly

### Using the YouTube Tool

The server provides one main tool: `get_yt_video_info`

This tool takes a YouTube video ID and returns:
- Video metadata (title, description, channel, publish date)
- Video transcript (with fallback logic for different transcript types)

**Example Usage:**
```python
# Extract video ID from YouTube URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
video_id = "dQw4w9WgXcQ"
result = get_yt_video_info(video_id)
```

### Client Configuration

To use this MCP server with a client, add the following configuration to your client's settings:

#### Using PyPI Installation (Recommended)

```json
{
  "mcpServers": {
    "mcp_youtube_extract": {
      "command": "mcp_youtube_extract",
      "env": {
        "YOUTUBE_API_KEY": "your_youtube_api_key"
      }
    }
  }
}
```

#### Using Development Setup

```json
{
  "mcpServers": {
    "mcp_youtube_extract": {
      "command": "uv",
      "args": [
        "--directory",
        "<your-project-directory>",
        "run",
        "mcp_youtube_extract"
      ],
      "env": {
        "YOUTUBE_API_KEY": "your_youtube_api_key"
      }
    }
  }
}
```

## Development

### Project Structure

```
mcp_youtube_extract/
├── src/
│   └── mcp_youtube_extract/
│       ├── __init__.py
│       ├── server.py          # MCP server implementation
│       ├── youtube.py         # YouTube API utilities
│       └── logger.py          # Logging configuration
├── tests/
│   ├── __init__.py
│   ├── test_context_fix.py    # Context API fallback tests
│   ├── test_inspector.py      # Server inspection tests
│   ├── test_with_api_key.py   # Full functionality tests
│   └── test_youtube_unit.py   # Unit tests for core functionality
├── logs/                      # Application logs
├── .env                       # Environment variables (create from .env.example)
├── .gitignore                 # Git ignore rules (includes coverage files)
├── pyproject.toml
├── LICENSE                    # MIT License
└── README.md
```

### Testing Strategy

The project uses a comprehensive testing approach:

1. **Unit Tests** (`test_youtube_unit.py`): Test core YouTube functionality with mocked APIs
2. **Integration Tests** (`test_context_fix.py`, `test_with_api_key.py`): Test full server functionality
3. **Manual Validation** (`test_inspector.py`): Interactive server inspection tool

### Error Handling

The project includes robust error handling:
- **Graceful API failures**: Returns appropriate error messages instead of crashing
- **Fallback logic**: Multiple strategies for transcript retrieval
- **Consistent error responses**: Standardized error message format
- **Comprehensive logging**: Detailed logs for debugging and monitoring

### Building

```bash
# Install build dependencies
uv add --dev hatch

# Build the package
uv run hatch build
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Getting Started

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

If you encounter any issues or have questions, please:
1. Check the [existing issues](https://github.com/sinjab/mcp_youtube_extract/issues)
2. Create a new issue with detailed information about your problem
3. Include logs and error messages when applicable
