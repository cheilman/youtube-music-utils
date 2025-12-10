import io
from datetime import timedelta
from unittest.mock import Mock

from youtube_music_utils.models import SongDetails
from youtube_music_utils.playlist import convert_playlist


def test_convert_playlist_basic():
    input_csv = """Playlist Header,Some Value
Value1,Value2

Video Id,Time Added
id1,2021-01-01
"""
    expected_output = """Playlist Header,Some Value
Value1,Value2

VideoId,Title,Artist,Album
id1,Song1,Artist1,Album1
"""

    input_file = io.StringIO(input_csv)
    output_file = io.StringIO()

    mock_client = Mock()
    mock_client.get_song_details.return_value = SongDetails(
        title="Song1", artist="Artist1", album="Album1", video_id="id1", length=timedelta(seconds=100)
    )

    convert_playlist(input_file, output_file, mock_client)

    # Check output, normalizing newlines for cross-platform safety
    assert output_file.getvalue().replace("\r\n", "\n") == expected_output


def test_convert_playlist_fetch_error():
    input_csv = """Video Id
id1
"""
    input_file = io.StringIO(input_csv)
    output_file = io.StringIO()

    mock_client = Mock()
    mock_client.get_song_details.side_effect = Exception("Fetch failed")

    convert_playlist(input_file, output_file, mock_client)

    output = output_file.getvalue().replace("\r\n", "\n")
    assert "VideoId,Title,Artist,Album" in output
    assert "id1,ERROR,ERROR,ERROR" in output
