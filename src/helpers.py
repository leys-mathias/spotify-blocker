"""Helper functions"""

import logging
import re
import sys

from typing import List
from pathlib import Path

LOGGER = logging.getLogger(name="Spotify Blocker")
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def _regexify(value: str) -> re.Pattern:
    """
    Transforms a string value to a compiled RegEx pattern that matches this
    string when it appears as a standalone word or set of words (ignores capitalization).
    
    Args:
        value (str): Input string value.

    Returns:
        re.Pattern: Compiled RegEx pattern.
    """
    pattern = rf"\b({value})\b"
    compiled_pattern = re.compile(pattern, re.IGNORECASE)
    return compiled_pattern

def _read_to_list(filepath: Path) -> List[str]:
    """
    Read lines of file to list.

    Args:
        filepath (Path): File path to read.

    Returns:
        List[str]: List of lines.
    """
    if not filepath.suffix == ".txt":
        raise ValueError(f"Invalid path provided: {str(filepath)}")

    lines = []
    with open(filepath, 'r') as file:
        for line in file:
            cleaned_line = line.strip()
            if cleaned_line:
                lines.append(cleaned_line)

    return lines

def parse_blocked_artists(blocked_artists: Path) -> List[re.Pattern]:
    """
    Parses .txt file of blocked artists and transforms it into a list of RegEx patterns.

    Args:
        blocked_artists (Path): Path to .txt file with blocked artists.

    Returns:
        List[re.Pattern]: RegEx patterns that match artist names.
    """
    if not blocked_artists:
        LOGGER.info("Blocked artists are: Red Hot Chili Peppers")
        return [_regexify("Red Hot Chili Peppers")]

    artists = _read_to_list(blocked_artists)

    if not artists:
        LOGGER.info("Blocked artists are: Red Hot Chili Peppers")
        return [_regexify("Red Hot Chili Peppers")]

    # Extra protection against accidental deletion
    if "Red Hot Chili Peppers" not in artists:
        artists.append("Red Hot Chili Peppers")

    LOGGER.info("Blocked artists are: %s" % ", ".join(artists))

    artist_rgx = [_regexify(artist) for artist in artists]
    return artist_rgx

def parse_blocked_songs(blocked_songs: Path) -> List[re.Pattern]:
    """
    Parses .txt file of blocked songs and transforms it into a list of RegEx patterns.

    Args:
        blocked_songs (Path): Path to .txt file with blocked songs.

    Returns:
        List[re.Pattern]: RegEx patterns that match songs names.
    """
    if not blocked_songs:
        LOGGER.info("No blocked songs")
        return []

    songs = _read_to_list(blocked_songs)

    if not songs:
        LOGGER.info("No blocked songs")
        return []

    LOGGER.info("Blocked artists are: %s" % ", ".join(songs))

    songs_rgx = [_regexify(song) for song in songs]
    return songs_rgx
