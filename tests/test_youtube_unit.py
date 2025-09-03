import pytest
from unittest.mock import patch, MagicMock
from src.mcp_youtube_extract import youtube

# Test get_video_info
@patch('src.mcp_youtube_extract.google_api.yt_get_video_info')
def test_get_video_info_success(mock_yt_get_video_info):
    mock_yt_get_video_info.return_value = {
        'title': 'Test Title',
        'channel_name': 'Test Channel',
        'publication_date': '2020-01-01T00:00:00Z',
        'description': 'Test Description',
        'views': 1000000
    }
    result = youtube.get_video_info('fake_api_key', 'fake_video_id')
    assert result['title'] == 'Test Title'

@patch('src.mcp_youtube_extract.google_api.yt_get_video_info')
def test_get_video_info_not_found(mock_yt_get_video_info):
    mock_yt_get_video_info.return_value = None
    result = youtube.get_video_info('fake_api_key', 'fake_video_id')
    assert result is None

@patch('src.mcp_youtube_extract.google_api.yt_get_video_info', side_effect=Exception('API error'))
def test_get_video_info_error(mock_yt_get_video_info):
    result = youtube.get_video_info('fake_api_key', 'fake_video_id')
    assert result is None

# Test get_video_transcript - Updated for yt-ts-extract
@patch('src.mcp_youtube_extract.transcript_api.get_transcript')
@patch('src.mcp_youtube_extract.transcript_api.get_transcript_text')
@patch('src.mcp_youtube_extract.transcript_api.get_available_languages')
@patch('src.mcp_youtube_extract.transcript_api.YouTubeTranscriptExtractor')
def test_get_video_transcript_success(mock_extractor_class, mock_get_langs, mock_get_text, mock_get_transcript):
    # Mock the extractor instance
    mock_extractor = MagicMock()
    mock_extractor_class.return_value = mock_extractor
    
    # Mock available languages
    mock_get_langs.return_value = [{'code': 'en'}]
    
    # Mock transcript segments
    mock_transcript = [{'text': 'Hello world'}]
    mock_extractor.get_transcript.return_value = mock_transcript
    
    result = youtube.get_video_transcript('fake_video_id')
    assert 'Hello world' in result

@patch('src.mcp_youtube_extract.transcript_api.get_transcript')
@patch('src.mcp_youtube_extract.transcript_api.get_transcript_text')
@patch('src.mcp_youtube_extract.transcript_api.get_available_languages')
@patch('src.mcp_youtube_extract.transcript_api.YouTubeTranscriptExtractor')
def test_get_video_transcript_no_transcript(mock_extractor_class, mock_get_langs, mock_get_text, mock_get_transcript):
    # Mock the extractor instance
    mock_extractor = MagicMock()
    mock_extractor_class.return_value = mock_extractor
    
    # Mock available languages
    mock_get_langs.return_value = []
    
    # Mock all transcript methods to return None/empty
    mock_extractor.get_transcript.return_value = None
    mock_get_transcript.return_value = None
    mock_get_text.return_value = None
    
    result = youtube.get_video_transcript('fake_video_id')
    assert result is None

@patch('src.mcp_youtube_extract.transcript_api.get_transcript')
@patch('src.mcp_youtube_extract.transcript_api.get_transcript_text')
@patch('src.mcp_youtube_extract.transcript_api.get_available_languages')
@patch('src.mcp_youtube_extract.transcript_api.YouTubeTranscriptExtractor')
def test_get_video_transcript_error(mock_extractor_class, mock_get_langs, mock_get_text, mock_get_transcript):
    # Mock the extractor class to raise an exception
    mock_extractor_class.side_effect = Exception('API error')
    
    result = youtube.get_video_transcript('fake_video_id')
    assert 'Could not retrieve transcript' in result

# Test format_video_info
def test_format_video_info_success():
    video_info = {
        'title': 'Test Title',
        'channel_name': 'Test Channel',
        'publication_date': '2020-01-01T00:00:00Z',
        'description': 'Test Description',
        'views': 1000000
    }
    result = youtube.format_video_info(video_info)
    assert 'Test Title' in result
    assert 'Test Channel' in result
    assert '2020-01-01T00:00:00Z' in result
    assert 'Test Description' in result
    assert '1,000,000' in result

def test_format_video_info_none():
    result = youtube.format_video_info(None)
    assert 'Video not found' in result 