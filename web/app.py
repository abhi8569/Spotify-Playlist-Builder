from flask import Flask, render_template, redirect, url_for, request, session, jsonify
import os
import sys
from pathlib import Path

# Add parent directory to path to import core modules
sys.path.append(str(Path(__file__).parent.parent))

from core.auth import connect_spotify
from core.playlist import list_user_playlists, create_playlist
from core.search import parse_song_input, search_song, add_song_to_playlist, add_songs_from_list
from core.artist import search_artist, add_artist_songs_to_playlist
from core.album import parse_album_input, search_album, add_album_to_playlist

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')

app =Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Spotify OAuth configuration
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI_WEB', 'http://127.0.0.1:5000/callback')
SCOPE = 'playlist-modify-public playlist-modify-private'


def get_spotify_client():
    """Get authenticated Spotify client from session."""
    token_info = session.get('token_info')
    if not token_info:
        return None
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    return sp


@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')


@app.route('/login')
def login():
    """Initiate Spotify OAuth flow."""
    sp_oauth = SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE,
        cache_path=None  # Don't use file cache for web
    )
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/callback')
def callback():
    """Handle Spotify OAuth callback."""
    sp_oauth = SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE,
        cache_path=None
    )
    
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    """Main dashboard."""
    sp = get_spotify_client()
    if not sp:
        return redirect(url_for('login'))
    
    try:
        user = sp.current_user()
        playlists = list_user_playlists(sp)
        return render_template('dashboard.html', user=user, playlists=playlists)
    except Exception as e:
        return f"Error: {e}", 500


@app.route('/api/playlists', methods=['GET'])
def get_playlists():
    """API endpoint to get user playlists."""
    sp = get_spotify_client()
    if not sp:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        playlists = list_user_playlists(sp)
        return jsonify({'playlists': playlists})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/playlists/create', methods=['POST'])
def create_playlist_api():
    """API endpoint to create a new playlist."""
    sp = get_spotify_client()
    if not sp:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    name = data.get('name', 'My Playlist')
    description = data.get('description', '')
    public = data.get('public', True)
    
    try:
        playlist_id = create_playlist(sp, name, description, public)
        return jsonify({'success': True, 'playlist_id': playlist_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/add-songs', methods=['POST'])
def add_songs_api():
    """API endpoint to add songs to a playlist."""
    sp =get_spotify_client()
    if not sp:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    playlist_id = data.get('playlist_id')
    songs = data.get('songs', [])
    
    if not playlist_id or not songs:
        return jsonify({'error': 'Missing playlist_id or songs'}), 400
    
    try:
        # Process songs without the interactive parts
        successful = 0
        failed = []
        
        for song_input in songs:
            song_name, artist_name = parse_song_input(song_input.strip())
            track_uri = search_song(sp, song_name, artist_name)
            
            if track_uri:
                if add_song_to_playlist(sp, playlist_id, track_uri):
                    successful += 1
                else:
                    failed.append(song_input)
            else:
                failed.append(song_input)
        
        return jsonify({
            'success': True,
            'added': successful,
            'failed': failed,
            'total': len(songs)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/add-artist', methods=['POST'])
def add_artist_api():
    """API endpoint to add songs from an artist."""
    sp = get_spotify_client()
    if not sp:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    playlist_id = data.get('playlist_id')
    artist_name = data.get('artist_name')
    mode = data.get('mode', 'top10')
    custom_n = data.get('custom_n')
    auto_select = data.get('auto_select', True)  # Default to auto for web
    
    if not playlist_id or not artist_name:
        return jsonify({'error': 'Missing playlist_id or artist_name'}), 400
    
    try:
        added = add_artist_songs_to_playlist(sp, playlist_id, artist_name, mode, custom_n, auto_select)
        return jsonify({
            'success': True,
            'added': added
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/add-album', methods=['POST'])
def add_album_api():
    """API endpoint to add tracks from an album."""
    sp = get_spotify_client()
    if not sp:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    playlist_id = data.get('playlist_id')
    album_input = data.get('album_input')
    auto_select = data.get('auto_select', True)  # Default to auto for web
    
    if not playlist_id or not album_input:
        return jsonify({'error': 'Missing playlist_id or album_input'}), 400
    
    try:
        added = add_album_to_playlist(sp, playlist_id, album_input, auto_select)
        return jsonify({
            'success': True,
            'added': added
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/logout')
def logout():
    """Clear session and logout."""
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
