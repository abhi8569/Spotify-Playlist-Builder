# Spotify Playlist Manager

A powerful Python tool to create Spotify playlists and add songs, artists, or albums using the Spotify API. Features both CLI and Web UI with batch processing and intelligent search.

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
- 🌐 **Dual Interface**: Use CLI or modern Web UI
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
   - Redirect URIs: Add **BOTH**:
     - `http://127.0.0.1:8888/callback` (for CLI)
     - `http://127.0.0.1:5000/callback` (for Web UI)
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
SPOTIPY_REDIRECT_URI_WEB='http://127.0.0.1:5000/callback'
FLASK_SECRET_KEY='your-random-secret-key-here'
```

## Usage

### 🌐 Web UI (Recommended)

Modern, visual interface accessible from any browser.

**Start the server:**
```bash
python web/app.py
```

**Access:**
1. Open browser to `http://127.0.0.1:5000`
2. Click **"Login with Spotify"**
3. Select or create a playlist
4. Use tabs to add Songs, Artists, or Albums

**Features:**
- ✅ Point-and-click interface
- ✅ Real-time progress
- ✅ Works on any OS
- ✅ Paste batch lists easily
- ✅ Auto-select enabled for speed

---

### 💻 CLI (Command Line)

Terminal-based interface for automation and scripting.

**Run the main script:**
```bash
py main.py
```

**Workflow:**
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

## Project Structure

```
spotify-playlist/
├── core/              # Core business logic
│   ├── auth.py       # Spotify authentication
│   ├── search.py     # Song search and addition
│   ├── artist.py     # Artist operations
│   ├── album.py      # Album operations
│   └── playlist.py   # Playlist management
├── web/              # Flask web application
│   ├── app.py        # Flask routes
│   ├── templates/    # HTML templates
│   └── static/       # CSS & JavaScript
├── main.py           # CLI entry point
├── debug_playlists.py # Debug tool
├── sample_*.txt      # Example files
├── .env              # Your credentials
└── requirements.txt  # Dependencies
```

## CLI vs Web Comparison

| Feature | CLI | Web UI |
|---------|-----|--------|
| **Interface** | Terminal | Browser |
| **Ease of Use** | Commands | Point & Click |
| **Batch Operations** | File upload | Paste text |
| **Artist Selection** | Manual or Auto | Auto (faster) |
| **Best For** | Automation, Scripts | Interactive use |
| **OS Requirement** | Python | Python + Browser |

## Troubleshooting

### "INVALID_CLIENT" Error
- Ensure Redirect URIs in Dashboard match `.env` exactly:
  - CLI: `http://127.0.0.1:8888/callback`
  - Web: `http://127.0.0.1:5000/callback`

### "Song/Artist/Album Not Found"
- Check spelling.
- For songs: Use "Song - Artist" format
- For albums: Use "Album - Artist" format

### Web UI Not Loading
- Check Flask is running: `python web/app.py`
- Verify port 5000 is not in use
- Check `.env` has `SPOTIPY_REDIRECT_URI_WEB` and `FLASK_SECRET_KEY`

### Rate Limiting
- The script has built-in delays (3s) between additions.
- Adding "All Songs" for a huge artist might take several minutes.
- Web UI auto-selects artists for faster batch processing.

## Docker Deployment

### Quick Start (Using Docker Hub)

1. Create a `.env` file with your Spotify credentials (see Environment Variables below)
2. Run:

```bash
docker-compose up -d
```

Access at: `http://127.0.0.1:5000`

### Pull from Docker Hub

```bash
# Pull the image
docker pull thedevabi/spotify-playlist-manager:latest

# Run the container
docker run -d \
  --name spotify-playlist-manager \
  -p 5000:5000 \
  --env-file .env \
  thedevabi/spotify-playlist-manager:latest
```

### Build Locally (Alternative)

```bash
# Build the image
docker build -t spotify-playlist-manager .

# Run the container
docker run -d \
  --name spotify-playlist-manager \
  -p 5000:5000 \
  --env-file .env \
  spotify-playlist-manager
```

### Development Mode (with hot reload)

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

### Environment Variables

Create a `.env` file in the project root:
```
SPOTIPY_CLIENT_ID='your_client_id'
SPOTIPY_CLIENT_SECRET='your_client_secret'
SPOTIPY_REDIRECT_URI='http://127.0.0.1:8888/callback'
SPOTIPY_REDIRECT_URI_WEB='http://127.0.0.1:5000/callback'
FLASK_SECRET_KEY='your-secret-key'
```

> ⚠️ **Security:** Never commit `.env` to version control or include it in Docker images.

### Docker Files

- **`Dockerfile`**: Production image with gunicorn
- **`docker-compose.yml`**: Pull from Docker Hub
- **`docker-compose.dev.yml`**: Development with hot reload
- **`.dockerignore`**: Excludes secrets and unnecessary files

## License

This project is for personal use. Spotify API usage must comply with [Spotify's Terms of Service](https://developer.spotify.com/terms).
