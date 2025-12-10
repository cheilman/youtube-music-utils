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
