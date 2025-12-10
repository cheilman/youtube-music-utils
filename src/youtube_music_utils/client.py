from ytmusicapi import YTMusic


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
