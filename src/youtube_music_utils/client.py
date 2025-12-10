from typing import Optional

from ytmusicapi import YTMusic


class Client:
    """
    A wrapper around ytmusicapi.YTMusic to handle initialization and authentication.
    """

    def __init__(self, auth: Optional[str] = None):
        """
        Initialize the YouTube Music client.

        Args:
            auth: Path to the authentication file (oauth.json or browser.json).
                  If None, initializes in unauthenticated mode (public endpoints only).
        """
        self._auth = auth
        self._api = YTMusic(auth=auth)

    @property
    def api(self) -> YTMusic:
        """
        Access the underlying YTMusic instance.
        """
        return self._api

    def login(self, auth_path: str):
        """
        Re-initialize with a new auth file.
        """
        self._auth = auth_path
        self._api = YTMusic(auth=auth_path)
