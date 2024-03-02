"""App configuration variables"""

import os

from dotenv import load_dotenv

load_dotenv()

try:
    CLIENT_ID = os.environ['CLIENT_ID']
except KeyError:
    raise KeyError("CLIENT_ID variable in .env file not set")

try:
    CLIENT_SECRET = os.environ['CLIENT_SECRET']
except KeyError:
    raise KeyError("CLIENT_SECRET variable in .env file not set")

OAUTH_SCOPE = " ".join([
    "user-read-private",
    "user-read-currently-playing",
    "user-read-playback-state",
    "user-modify-playback-state",
])

REDIRECT_URI = os.environ.get("REDIRECT_URI", "https://localhost:8888/callback")

WAIT_SECONDS = 0.5  # Stays on safe side of Spotify's API rate limits
