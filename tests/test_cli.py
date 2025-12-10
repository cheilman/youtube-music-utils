from datetime import timedelta
from unittest.mock import patch

from youtube_music_utils.cli import main
from youtube_music_utils.models import SongDetails


def test_cli_version(capsys):
    with patch("sys.argv", ["ym-utils", "version"]):
        main()
        captured = capsys.readouterr()
        assert "youtube-music-utils v0.1.0" in captured.out


def test_cli_help(capsys):
    with patch("sys.argv", ["ym-utils"]):
        main()
        captured = capsys.readouterr()
        assert "usage: " in captured.out


def test_cli_get_song(capsys):
    mock_details = SongDetails(
        title="Test Title", artist="Test Artist", album="Test Album", video_id="test_id", length=timedelta(seconds=180)
    )
    with patch("sys.argv", ["ym-utils", "get-song", "test_id"]):
        with patch("youtube_music_utils.cli.Client") as mock_client_cls:
            mock_client = mock_client_cls.return_value
            mock_client.get_song_details.return_value = mock_details

            main()

            mock_client.get_song_details.assert_called_once_with(video_id="test_id")
            captured = capsys.readouterr()
            assert "Test Title" in captured.out
            assert "Test Album" in captured.out
