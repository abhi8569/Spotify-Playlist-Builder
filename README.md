# Spotify Playlist Manager

A Python script to create Spotify playlists and add songs using the Spotify API. Supports adding songs individually or in batch from a text file.

## Features

- 🔐 Authenticate with your Spotify account
- 📋 List existing playlists or create new ones
- 🎵 Add songs individually or in batch
- 📁 Import songs from a text file
- ⏱️ Rate limiting to avoid API throttling

## Prerequisites

- Python 3.7 or higher
- A Spotify account (free or premium)
- Spotify Developer App credentials (Client ID & Client Secret)

## Setup

### 1. Get Spotify API Credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Click **"Create App"**
4. Fill in:
   - App name: (e.g., "Playlist Manager")
   - App description: (e.g., "Personal playlist management")
   - Redirect URI: `http://127.0.0.1:8888/callback`
5. Click **"Save"**
6. Copy your **Client ID** and **Client Secret**

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

1. Open the `.env` file
2. Replace the placeholder values with your credentials:

```
SPOTIPY_CLIENT_ID='your_client_id_here'
SPOTIPY_CLIENT_SECRET='your_client_secret_here'
SPOTIPY_REDIRECT_URI='http://127.0.0.1:8888/callback'
```

## Usage

### Interactive Mode (Add Songs One by One)

```bash
py search.py
```

1. Select or create a playlist
2. Choose option `1` (interactive mode)
3. Enter songs in `"Song Name - Artist"` format
4. Repeat or exit

### Batch Mode (Add from File)

```bash
py search.py
```

1. Select or create a playlist
2. Choose option `2` (file input)
3. Enter the path to your song list file (e.g., `sample_songs.txt`)
4. Confirm to add all songs

### Manual Batch Mode

```bash
py search.py
```

1. Select or create a playlist
2. Choose option `3` (manual batch)
3. Enter songs one per line
4. Press Enter on a blank line to finish

## Song File Format

Create a text file with one song per line in this format:

```
Song Name - Artist
Another Song - Another Artist
Third Song - Third Artist
```

**Example (`sample_songs.txt`):**
```
Shape of You - Ed Sheeran
Blinding Lights - The Weeknd
Levitating - Dua Lipa
```

## Modules

- **`auth.py`** - Handles Spotify authentication
- **`playlist.py`** - Manages playlist creation and selection
- **`search.py`** - Searches and adds songs to playlists
- **`debug_playlists.py`** - Debug tool to list all playlists

## Troubleshooting

### "INVALID_CLIENT" Error
- Ensure your Redirect URI in the Spotify Dashboard **exactly** matches: `http://127.0.0.1:8888/callback`
- Check that Client ID and Secret are correct in `.env`

### "Song not found" Errors
- Verify the artist name is spelled correctly
- Some songs may not be available in your region
- Try using the exact artist name as shown on Spotify

### Playlists Not Showing Up
- Wait a few seconds and try again (API sync delay)
- Ensure you're logged into the correct Spotify account

### Rate Limiting
- The script automatically adds a 3-second delay between songs
- For large playlists (100+ songs), expect ~5-10 minutes processing time

## License

This project is for personal use. Spotify API usage must comply with [Spotify's Terms of Service](https://developer.spotify.com/terms).
