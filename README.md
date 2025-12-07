# Spotify Playlist Manager

A powerful Python tool to create Spotify playlists and add songs or artists using the Spotify API. Features a unified workflow, batch processing, and intelligent artist handling.

## Features

- 🔐 **Authentication**: Securely connect with your Spotify account
- 📋 **Playlist Management**: List existing playlists or create new ones
- 🎵 **Add Songs**:
  - **Interactive**: Add songs one by one by name
  - **Batch File**: Import a list of songs from a text file
  - **Manual Batch**: Paste a list of songs directly
- 🎤 **Add Artists**:
  - **Modes**:
    - **Top 10**: Quickly add the artist's most popular tracks
    - **Top N**: Add a custom number of top tracks (e.g., top 50)
    - **All Songs**: Add every track from the artist's discography
  - **Auto-Select**: Option to automatically pick the most popular artist match (great for batch processing)
  - **Batch File**: Import a list of artists to process sequentially
- 💿 **Add Albums**:
  - Add all tracks from any album
  - **Auto-Select**: Automatically pick best match or choose manually
  - **Batch File**: Import a list of albums to process
  - **Format**: "Album - Artist" for accurate searching
- ⏱️ **Rate Limiting**: Built-in delays to avoid API throttling

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

### 🚀 Unified Workflow (Recommended)

Run the main script to access all features in one place:

```bash
py main.py
```

This will guide you through:
1. **Authentication**
2. **Playlist Selection/Creation**
3. **Main Menu**: Choose to add Songs, Artists, Albums, or Exit

---

### Feature Details

#### 1. Add Songs (by Name)
- **Interactive**: Type song names one by one (e.g., "Shape of You - Ed Sheeran").
- **From File**: Provide a path to a text file with one song per line.
- **Manual Batch**: Copy-paste a list of songs into the terminal.

**Song File Format (`sample_songs.txt`):**
```
Shape of You - Ed Sheeran
Blinding Lights - The Weeknd
Levitating - Dua Lipa
```

#### 2. Add Artists
- **Single Artist**: Type an artist name.
- **Batch from File**: Provide a path to a text file with artist names.

**Artist Modes:**
- **Top 10**: Fast addition of the artist's hits.
- **Top N**: Fetches all songs, sorts by popularity, and picks the top N.
- **All Songs**: Adds everything (can take time for large discographies).

**Auto-Select Feature:**
- You will be asked if you want to **Auto-select the first match**.
- **Yes**: Automatically picks the artist with the most followers (best for batch files).
- **No**: Lets you manually choose from search results (best for obscure artists).

**Artist File Format (`sample_artists.txt`):**
```
The Beatles
Pink Floyd
Led Zeppelin
```

#### 3. Add Albums
- **Single Album**: Type album in "Album - Artist" format.
- **Batch from File**: Provide a path to a text file with album entries.

**Format:** `Album - Artist` (e.g., "Abbey Road - The Beatles")
- Including the artist name ensures accuracy and avoids ambiguity.

**Auto-Select Feature:**
- **Yes**: Automatically picks the first match (fastest).
- **No**: Shows all matches, you choose manually.

**Album File Format (`sample_albums.txt`):**
```
Abbey Road - The Beatles
The Dark Side of the Moon - Pink Floyd
Thriller - Michael Jackson
```

---

### Advanced Usage (Individual Scripts)

You can run individual modules directly if you prefer:

- **`py search.py`**: Just for adding songs.
- **`py artist.py`**: Just for adding artists.
- **`py album.py`**: Just for adding albums.
- **`py playlist.py`**: To list or create playlists.

## Modules

- **`main.py`**: Main entry point (Recommended).
- **`auth.py`**: Handles Spotify authentication.
- **`playlist.py`**: Manages playlist operations.
- **`search.py`**: Song search and addition logic.
- **`artist.py`**: Artist search and addition logic.
- **`album.py`**: Album search and addition logic.
- **`debug_playlists.py`**: Debug tool to see raw playlist data.

## Troubleshooting

### "INVALID_CLIENT" Error
- Ensure Redirect URI in Dashboard matches `.env` exactly (`http://127.0.0.1:8888/callback`).

### "Song/Artist Not Found"
- Check spelling.
- Try adding the artist name to the search (e.g., "Song - Artist").

### Rate Limiting
- The script has built-in delays (3s) between additions.
- Adding "All Songs" for a huge artist might take a few minutes.

## License

This project is for personal use. Spotify API usage must comply with [Spotify's Terms of Service](https://developer.spotify.com/terms).
