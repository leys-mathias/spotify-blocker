"""Auto-skip Spotify artists / songs"""

import os
import time

from config import BLOCKED_ARTISTS_RGX, BLOCKED_SONGS_RGX, WAIT_SECONDS
from typing import Dict

import spotipy

from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

_auth_manager = SpotifyOAuth(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    redirect_uri=os.getenv('REDIRECT_URI'),
    scope=" ".join(
        ["user-read-private",
        "user-read-currently-playing",
        "user-read-playback-state",
        "user-modify-playback-state",]
    ),
)

spotify_client = spotipy.Spotify(auth_manager=_auth_manager)

def is_blocked_artist(current_track: Dict) -> bool:
    """
    Checks whether the provided track contains a blocked artist.

    Args:
        current_track (Dict): Currently playing track Dict object.
    
    Returns:
        bool: Whether or not Spotify is playing a blocked artist.
    """
    try:
        artists = current_track['item']['artists']
    except:
        return False

    if not artists:
        return False

    return any(
        any(
            blocked_artist_rgx.search(artist['name'])
            for blocked_artist_rgx in BLOCKED_ARTISTS_RGX
        )
        for artist in artists
    )

def is_blocked_song(current_track: Dict) -> bool:
    """
    Checks whether the provided track contains a blocked song.

    Args:
        current_track (Dict): Currently playing track Dict object.
    
    Returns:
        bool: Whether or not Spotify is playing a blocked song.
    """
    try:
        song = current_track['item']['name']
    except:
        return False

    if not song:
        return False

    return any(
        blocked_song_rgx.search(song)
        for blocked_song_rgx in BLOCKED_SONGS_RGX
    )

def should_skip_song(spotify_client: spotipy.Spotify) -> bool:
    """Determines whether or not to skip the current Spotify song.

    Args:
        spotify_client (spotipy.Spotify): Spotify client object.

    Returns:
        bool: Whether or not to skip the current song.
    """
    current_track = spotify_client.current_playback()
    return (
        is_blocked_artist(current_track)
        or is_blocked_song(current_track)
    )


if __name__ == '__main__':
    while True:
        time.sleep(WAIT_SECONDS)
        if should_skip_song(spotify_client):
            spotify_client.next_track()
