from datetime import timedelta

from ytmusicapi import YTMusic

from .models import SongDetails


class Client:
    """
    A wrapper around ytmusicapi.YTMusic that always initializes an unauthenticated instance.
    """

    def __init__(self):
        """
        Initialize the YouTube Music client in unauthenticated mode.
        """
        self._api = YTMusic()

    @property
    def api(self) -> YTMusic:
        """
        Access the underlying YTMusic instance.
        """
        return self._api

    def get_song_details(self, video_id: str) -> SongDetails:
        """
        Get structured details for a song.

        Args:
            video_id: The video ID of the song.

        Returns:
            SongDetails object containing title, artist, album, videoId, and length.
        """
        data = self._api.get_song(videoId=video_id)
        video_details = data["videoDetails"]
        microformat = data.get("microformat", {}).get("microformatDataRenderer", {})

        title = video_details["title"]
        artist = video_details["author"]
        length_seconds = int(video_details.get("lengthSeconds", 0))
        length = timedelta(seconds=length_seconds)

        # Album extraction logic
        album = None
        tags = microformat.get("tags", [])
        if tags:
            # Filter out tags that are roughly equal to title or artist
            potential_albums = [tag for tag in tags if tag.lower() != title.lower() and tag.lower() != artist.lower()]
            if potential_albums:
                album = potential_albums[0]

        return SongDetails(
            title=title,
            artist=artist,
            album=album,
            video_id=video_details["videoId"],
            length=length,
        )
