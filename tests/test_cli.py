from unittest.mock import patch

from youtube_music_utils.cli import main


def test_cli_version(capsys):
    with patch("sys.argv", ["ym-utils", "version"]):
        main()
        captured = capsys.readouterr()
        assert "youtube-music-utils v0.1.0" in captured.out


def test_cli_login():
    with patch(
        "sys.argv",
        [
            "ym-utils",
            "login",
            "--file",
            "test_auth.json",
            "--client-id",
            "foo",
            "--client-secret",
            "bar",
        ],
    ):
        with patch("youtube_music_utils.cli.setup_oauth") as mock_setup:
            main()
            mock_setup.assert_called_once_with(
                filepath="test_auth.json", client_id="foo", client_secret="bar"
            )


def test_cli_help(capsys):
    with patch("sys.argv", ["ym-utils"]):
        main()
        captured = capsys.readouterr()
        assert "usage: " in captured.out
