import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def connect_spotify():
    """
    Connects to Spotify using credentials from environment variables.
    Returns a spotipy.Spotify object.
    """
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

    if not client_id or not client_secret or not redirect_uri:
        raise ValueError("Missing Spotify credentials. Please check your .env file.")

    scope = "playlist-modify-public playlist-modify-private"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope
    ))
    
    user = sp.current_user()
    print(f"Connected to Spotify as: {user['display_name']}")
    
    return sp

if __name__ == "__main__":
    try:
        connect_spotify()
    except Exception as e:
        print(f"Error: {e}")
