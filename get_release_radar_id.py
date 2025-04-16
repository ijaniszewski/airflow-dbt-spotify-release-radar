from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

# Auth manager handles login
sp = Spotify(client_credentials_manager=SpotifyOAuth())

# Fetch and search for Release Radar playlist
playlists = sp.current_user_playlists()
for playlist in playlists["items"]:
    if playlist["name"] == "Release Radar":
        print(f"Found Release Radar! ID: {playlist['id']}")
        break
else:
    print("Release Radar not found.")
