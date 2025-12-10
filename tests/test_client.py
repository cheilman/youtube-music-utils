from unittest.mock import patch

from youtube_music_utils import Client


def test_client_init_unauthenticated():
    with patch("youtube_music_utils.client.YTMusic") as mock_yt:
        client = Client()
        mock_yt.assert_called_once_with()
        assert client.api == mock_yt.return_value
