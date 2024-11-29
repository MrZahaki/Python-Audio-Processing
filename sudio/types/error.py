class RefreshError(Exception):
    """Exception raised when a refresh operation encounters an error."""


class DecodeError(Exception):
    """Exception raised when an error occurs during audio decoding."""


class StreamError(Exception):
    """Exception raised for errors related to audio streaming."""
