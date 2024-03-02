"""App configuration variables"""

from helpers import regexify

_BLOCKED_ARTISTS = [
    "Red Hot Chili Peppers",  # Comes pre-blocked for obvious reasons
]
BLOCKED_ARTISTS_RGX = [regexify(artist_name) for artist_name in _BLOCKED_ARTISTS]

_BLOCKED_SONGS = []
BLOCKED_SONGS_RGX = [regexify(song_name) for song_name in _BLOCKED_SONGS]

WAIT_SECONDS = 0.5  # Stays on safe side of Spotify's API rate limits
