from pathlib import Path
from unittest.mock import patch

import pytest

from youtube_music_utils.cli import main


def test_cli_version(capsys):
    with patch("sys.argv", ["ym-utils", "version"]):
        main()
        captured = capsys.readouterr()
        assert "youtube-music-utils v0.1.0" in captured.out


def test_cli_login_with_credentials_creates_new_auth():
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
            mock_setup.assert_called_once_with(filepath="test_auth.json", client_id="foo", client_secret="bar")


def test_cli_login_existing_file_no_credentials_verifies_session(capsys):
    with patch("sys.argv", ["ym-utils", "login", "--file", "existing_auth.json"]):
        with patch.object(Path, "exists", return_value=True):
            with patch("youtube_music_utils.cli.Client") as mock_client:
                main()
                mock_client.assert_called_once_with(auth="existing_auth.json")
                captured = capsys.readouterr()
                assert "Existing session verified successfully." in captured.out


def test_cli_login_existing_file_no_credentials_verification_fails(capsys):
    with patch("sys.argv", ["ym-utils", "login", "--file", "invalid_auth.json"]):
        with patch.object(Path, "exists", return_value=True):
            with patch(
                "youtube_music_utils.cli.Client",
                side_effect=Exception("Invalid auth file"),
            ) as mock_client:
                with pytest.raises(SystemExit) as excinfo:
                    main()
                assert excinfo.value.code == 1
                mock_client.assert_called_once_with(auth="invalid_auth.json")
                captured = capsys.readouterr()
                assert "Error verifying existing session: Invalid auth file" in captured.err
                assert "--client-id and --client-secret to re-authenticate." in captured.err


def test_cli_login_no_file_no_credentials_requires_credentials(capsys):
    with patch("sys.argv", ["ym-utils", "login", "--file", "non_existent.json"]):
        with patch.object(Path, "exists", return_value=False):
            with pytest.raises(SystemExit) as excinfo:
                main()
            assert excinfo.value.code == 1
            captured = capsys.readouterr()
            assert (
                "Error: --client-id and --client-secret are required to set up a new authentication file."
                in captured.err
            )


def test_cli_help(capsys):
    with patch("sys.argv", ["ym-utils"]):
        main()
        captured = capsys.readouterr()
        assert "usage: " in captured.out
