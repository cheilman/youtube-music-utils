import json
from unittest.mock import patch

from youtube_music_utils.cli import main


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
    mock_result = {"videoDetails": {"title": "Test Song"}}
    with patch("sys.argv", ["ym-utils", "get-song", "test_id"]):
        with patch("youtube_music_utils.cli.Client") as mock_client_cls:
            mock_client = mock_client_cls.return_value
            mock_client.api.get_song.return_value = mock_result

            main()

            mock_client.api.get_song.assert_called_once_with(videoId="test_id")
            captured = capsys.readouterr()
            assert json.dumps(mock_result, indent=2) in captured.out
