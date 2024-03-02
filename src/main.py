"""Auto-skip Spotify artists / songs"""

import argparse
import logging
import re
import time

from config import CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI, WAIT_SECONDS
from helpers import parse_blocked_artists, parse_blocked_songs

from pathlib import Path
from typing import Dict, List

import spotipy
from spotipy.oauth2 import SpotifyOAuth

PARSER = argparse.ArgumentParser("Spotify blocker arguments")
PARSER.add_argument('--blocked_artists', type=Path, required=False, default="blocked_artists.txt", help='Path to blocked artists')
PARSER.add_argument('--blocked_songs', type=Path, required=False, default="blocked_songs.txt", help='Path to blocked songs')

ARGS = PARSER.parse_args()

LOGGER = logging.getLogger(name="Spotify Blocker")
LOGGER.setLevel("info")

def is_blocked_artist(current_track: Dict, blocked_artists: List[re.Pattern]) -> bool:
    """
    Checks whether the provided track contains a blocked artist.

    Args:
        current_track (Dict): Currently playing track Dict object.
        blocked_artists (List[re.Pattern]): Specified blocked artists.
    
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
            blocked_artist.search(artist['name'])
            for blocked_artist in blocked_artists
        )
        for artist in artists
    )

def is_blocked_song(current_track: Dict, blocked_songs: List[re.Pattern]) -> bool:
    """
    Checks whether the provided track contains a blocked song.

    Args:
        current_track (Dict): Currently playing track Dict object.
        blocked_songs (List[re.Pattern]): Specified blocked songs.
    
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
        blocked_song.search(song)
        for blocked_song in blocked_songs
    )

def is_blocked(
        *,
        spotify_client: spotipy.Spotify,
        blocked_artists: List[re.Pattern],
        blocked_songs: List[re.Pattern],
    ) -> bool:
    """
    Determines whether or not to skip the current Spotify song.

    Args:
        spotify_client (spotipy.Spotify): Spotify client object.

    Returns:
        bool: Whether or not to skip the current song.
    """
    current_track = spotify_client.current_playback()
    return (
        is_blocked_artist(current_track, blocked_artists)
        or is_blocked_song(current_track, blocked_songs)
    )

def main() -> None:
    LOGGER.info("Application started...")
    blocked_artists = parse_blocked_artists(ARGS.blocked_artists)
    blocked_songs = parse_blocked_songs(ARGS.blocked_songs)

    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=OAUTH_SCOPE,
    )

    spotify_client = spotipy.Spotify(auth_manager=auth_manager)

    while True:
        time.sleep(WAIT_SECONDS)

        should_skip_song = is_blocked(
            spotify_client=spotify_client,
            blocked_artists=blocked_artists,
            blocked_songs=blocked_songs,
        )

        if should_skip_song:
            LOGGER.info("Saved your ears from a song")
            spotify_client.next_track()
            time.sleep(0.5)  # Brief cool-down period: otherwise it can skip the next song as well

if __name__ == '__main__':
    main()
