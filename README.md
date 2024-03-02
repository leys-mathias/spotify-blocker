# Spotify Blocker

Script that when run will monitor your Spotify activity and auto-skip specified songs and/or artists. It is quantum-secure against malicious actors manipulating your Spotify account via the UI.

## Description

While Spotify offers the feature to block certain artists and/or songs, this can be disabled by potential malicious actors such as ""friends"" or family members using your Spotify account who are also aware of this feature.

This can lead to nefarious situations including (but not limited to) having to listen to Red Hot Chili Peppers songs.

This repo aims to solve this problem.
It contains a script that will monitor your Spotify account's activity via the Spotify activity and auto-skip specified blocked songs or songs from specified blocked artists (including but not limited to the Red Hot Chili Peppers).

Malicious actors will never abuse your Spotify account again!

## Getting Started

### Dependencies

All you need to do is `pip install -r requirements.txt`

### Executing script

First create a `.env` file in the root directory where you add the following environment variables:
```
CLIENT_ID="<YOUR_CLIENT_ID>"
CLIENT_SECRET="<YOUR_CLIENT_SECRET>"
REDIRECT_URI="https://localhost:8888/callback"  # Or a different redirect URI of choice
```
You can find you client ID / secret in your Spotify for developers portal. Google it.

Then, add the name of any artist you want to block by modifying `blocked_artists.txt`. Likewise for `blocked_songs.txt`. Elements are newline-separated.

Two useful features are automatically present:
- The Red Hot Chili Peppers are blocked by default to save time, as users no longer need to type out the name.
- If the Red Hot Chili Peppers are accidentally deleted from the list of blocked artists, they are automatically added.

In other words, in order to protect users against themselves, it is impossible to unblock the Red Hot Chili Peppers. You're welcome!

Finally, you are set to run the script via the following commands:
```
cd src
python main.py
```

## Roadmap

- [x] Accidental deletion prevention of Red Hot Chili Peppers
- [x] Red Hot Chili peppers block by default to save time
- [ ] Add support for YouTube Music
- [ ] Add support for Apple Music
- [ ] Implement in Rust to optimize performance
- [ ] Fine-tune wait times to fall just under Spotify's API rate limits

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
