from datetime import timedelta
from unittest.mock import patch

from youtube_music_utils import Client
from youtube_music_utils.models import SongDetails


def test_client_init_unauthenticated():
    with patch("youtube_music_utils.client.YTMusic") as mock_yt:
        client = Client()
        mock_yt.assert_called_once_with()
        assert client.api == mock_yt.return_value


def test_get_song_details():
    mock_response = {
        "videoDetails": {
            "videoId": "test_id",
            "title": "Test Title",
            "author": "Test Artist",
            "lengthSeconds": "180",
        },
        "microformat": {"microformatDataRenderer": {"tags": ["Test Artist", "Test Album", "Test Title"]}},
    }

    with patch("youtube_music_utils.client.YTMusic") as mock_yt_cls:
        mock_yt = mock_yt_cls.return_value
        mock_yt.get_song.return_value = mock_response

        client = Client()
        details = client.get_song_details("test_id")

        mock_yt.get_song.assert_called_once_with(videoId="test_id")
        assert details == SongDetails(
            title="Test Title",
            artist="Test Artist",
            album="Test Album",
            video_id="test_id",
            length=timedelta(seconds=180),
        )


def test_get_song_details_no_album_tags():
    mock_response = {
        "videoDetails": {
            "videoId": "test_id",
            "title": "Test Title",
            "author": "Test Artist",
            "lengthSeconds": "180",
        },
        "microformat": {"microformatDataRenderer": {"tags": ["Test Artist", "Test Title"]}},
    }

    with patch("youtube_music_utils.client.YTMusic") as mock_yt_cls:
        mock_yt = mock_yt_cls.return_value
        mock_yt.get_song.return_value = mock_response

        client = Client()
        details = client.get_song_details("test_id")

        assert details.album is None
