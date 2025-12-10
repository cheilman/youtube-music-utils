from unittest.mock import patch

from youtube_music_utils import Client


def test_client_init_no_auth():
    with patch("youtube_music_utils.client.YTMusic") as mock_yt:
        client = Client()
        mock_yt.assert_called_once_with(auth=None)
        assert client.api == mock_yt.return_value


def test_client_init_with_auth():
    with patch("youtube_music_utils.client.YTMusic") as mock_yt:
        client = Client(auth="auth.json")
        mock_yt.assert_called_once_with(auth="auth.json")
        assert client.api == mock_yt.return_value


def test_client_login():
    with patch("youtube_music_utils.client.YTMusic") as mock_yt:
        client = Client()
        mock_yt.reset_mock()

        client.login("new_auth.json")
        mock_yt.assert_called_with(auth="new_auth.json")
        assert client.api == mock_yt.return_value
