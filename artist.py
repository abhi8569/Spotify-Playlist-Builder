import time


def search_artist(sp, artist_name, auto_select=False):
    """
    Searches for an artist on Spotify.
    
    Args:
        sp: Spotify client object
        artist_name: Name of the artist
        auto_select: If True, automatically selects the first result (top followers)
    
    Returns:
        Artist object if found, None otherwise
    """
    results = sp.search(q=f"artist:{artist_name}", type='artist', limit=5)
    
    if results['artists']['items']:
        # Show top results for user to confirm
        artists = results['artists']['items']
        
        if len(artists) == 1:
            artist = artists[0]
            print(f"Found: {artist['name']} ({artist['followers']['total']:,} followers)")
            return artist
        else:
            # Multiple matches found
            print(f"\nFound {len(artists)} artists:")
            for i, artist in enumerate(artists, 1):
                followers = artist['followers']['total']
                print(f"{i}. {artist['name']} ({followers:,} followers)")
            
            if auto_select:
                # Auto-select the first one (highest followers)
                selected = artists[0]
                print(f"\n→ Auto-selected: {selected['name']} ({selected['followers']['total']:,} followers)")
                return selected
            else:
                # Manual selection
                while True:
                    try:
                        choice = int(input(f"\nSelect artist (1-{len(artists)}) or 0 to skip: "))
                        if choice == 0:
                            return None
                        if 1 <= choice <= len(artists):
                            return artists[choice - 1]
                        print(f"Please enter a number between 0 and {len(artists)}")
                    except ValueError:
                        print("Please enter a valid number")
    
    return None


def get_artist_top_tracks(sp, artist_id, limit=10):
    """
    Gets the top tracks for an artist (up to 10).
    Uses Spotify's dedicated top tracks endpoint.
    
    Args:
        sp: Spotify client object
        artist_id: Spotify artist ID
        limit: Number of tracks to return (max 10)
    
    Returns:
        List of track URIs
    """
    results = sp.artist_top_tracks(artist_id)
    tracks = results['tracks'][:limit]
    
    track_uris = []
    for track in tracks:
        print(f"  - {track['name']}")
        track_uris.append(track['uri'])
    
    return track_uris


def get_all_artist_tracks(sp, artist_id):
    """
    Gets all tracks from all albums by an artist.
    
    Args:
        sp: Spotify client object
        artist_id: Spotify artist ID
    
    Returns:
        List of track dictionaries with 'name', 'uri', and 'popularity'
    """
    tracks = []
    
    # Get all albums
    print("  Fetching albums...")
    albums = []
    results = sp.artist_albums(artist_id, album_type='album,single', limit=50)
    
    while results:
        albums.extend(results['items'])
        if results['next']:
            time.sleep(0.5)  # Small delay between pagination
            results = sp.next(results)
        else:
            break
    
    print(f"  Found {len(albums)} albums/singles")
    
    # Get tracks from each album
    album_ids = [album['id'] for album in albums]
    
    # Process in batches of 20 (Spotify API limit)
    for i in range(0, len(album_ids), 20):
        batch = album_ids[i:i+20]
        albums_data = sp.albums(batch)
        
        for album in albums_data['albums']:
            for track in album['tracks']['items']:
                # Check if artist is in the track (to avoid features)
                track_artists = [artist['id'] for artist in track['artists']]
                if artist_id in track_artists:
                    tracks.append({
                        'name': track['name'],
                        'uri': track['uri'],
                        'popularity': 0  # Will be updated below
                    })
        
        if i + 20 < len(album_ids):
            time.sleep(0.5)  # Delay between batches
    
    # Get popularity for each track (in batches of 50)
    print(f"  Getting popularity for {len(tracks)} tracks...")
    track_ids = [track['uri'].split(':')[2] for track in tracks]
    
    for i in range(0, len(track_ids), 50):
        batch = track_ids[i:i+50]
        tracks_data = sp.tracks(batch)
        
        for j, track_data in enumerate(tracks_data['tracks']):
            if track_data:
                tracks[i + j]['popularity'] = track_data.get('popularity', 0)
        
        if i + 50 < len(track_ids):
            time.sleep(0.5)  # Delay between batches
    
    return tracks


def get_top_n_tracks(sp, artist_id, n):
    """
    Gets the top N tracks by an artist, sorted by popularity.
    
    Args:
        sp: Spotify client object
        artist_id: Spotify artist ID
        n: Number of tracks to return
    
    Returns:
        List of track URIs
    """
    all_tracks = get_all_artist_tracks(sp, artist_id)
    
    # Sort by popularity
    all_tracks.sort(key=lambda x: x['popularity'], reverse=True)
    
    # Take top N
    top_tracks = all_tracks[:n]
    
    print(f"\n  Top {len(top_tracks)} tracks:")
    track_uris = []
    for i, track in enumerate(top_tracks, 1):
        print(f"  {i}. {track['name']} (popularity: {track['popularity']})")
        track_uris.append(track['uri'])
    
    return track_uris


def add_artist_songs_to_playlist(sp, playlist_id, artist_name, mode='top10', custom_n=None, auto_select=False):
    """
    Adds songs from an artist to a playlist.
    
    Args:
        sp: Spotify client object
        playlist_id: ID of the playlist
        artist_name: Name of the artist
        mode: 'top10', 'topn', or 'all'
        custom_n: Number of songs if mode is 'topn'
        auto_select: If True, automatically selects first artist match
    
    Returns:
        Number of songs added
    """
    print(f"\nSearching for artist: {artist_name}")
    artist = search_artist(sp, artist_name, auto_select=auto_select)
    
    if not artist:
        print(f"✗ Artist not found: {artist_name}")
        return 0
    
    artist_id = artist['id']
    artist_name = artist['name']
    
    print(f"\nFetching songs from {artist_name}...")
    
    if mode == 'top10':
        track_uris = get_artist_top_tracks(sp, artist_id, limit=10)
    elif mode == 'topn':
        if not custom_n or custom_n <= 0:
            print("✗ Invalid number specified")
            return 0
        track_uris = get_top_n_tracks(sp, artist_id, custom_n)
    elif mode == 'all':
        all_tracks = get_all_artist_tracks(sp, artist_id)
        track_uris = [track['uri'] for track in all_tracks]
        print(f"\n  All {len(track_uris)} tracks will be added")
    else:
        print("✗ Invalid mode")
        return 0
    
    if not track_uris:
        print("✗ No tracks found")
        return 0
    
    print(f"\nAdding {len(track_uris)} songs to playlist...")
    
    # Add in batches of 100 (Spotify limit)
    added = 0
    for i in range(0, len(track_uris), 100):
        batch = track_uris[i:i+100]
        try:
            sp.playlist_add_items(playlist_id, batch)
            added += len(batch)
            print(f"✓ Added {len(batch)} songs ({added}/{len(track_uris)})")
            
            if i + 100 < len(track_uris):
                time.sleep(2)  # Delay between batches
        except Exception as e:
            print(f"✗ Error adding batch: {e}")
    
    return added


def add_artists_from_file(sp, playlist_id, file_path, mode='top10', custom_n=None, auto_select=False):
    """
    Adds songs from multiple artists listed in a file.
    
    Args:
        sp: Spotify client object
        playlist_id: ID of the playlist
        file_path: Path to file with artist names (one per line)
        mode: 'top10', 'topn', or 'all'
        custom_n: Number of songs per artist if mode is 'topn'
        auto_select: If True, automatically selects first artist match
    
    Returns:
        Total number of songs added
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            artists = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"✗ File not found: {file_path}")
        return 0
    except Exception as e:
        print(f"✗ Error reading file: {e}")
        return 0
    
    if not artists:
        print("✗ No artists found in file")
        return 0
    
    print(f"\n=== Processing {len(artists)} artists ===\n")
    
    total_added = 0
    for i, artist in enumerate(artists, 1):
        print(f"\n[{i}/{len(artists)}] Processing: {artist}")
        print("-" * 50)
        
        added = add_artist_songs_to_playlist(sp, playlist_id, artist, mode, custom_n, auto_select=auto_select)
        total_added += added
        
        if i < len(artists):
            print("\nWaiting 3 seconds before next artist...")
            time.sleep(3)
    
    return total_added


if __name__ == "__main__":
    from auth import connect_spotify
    from playlist import get_or_create_playlist
    
    try:
        sp = connect_spotify()
        playlist_id = get_or_create_playlist(sp)
        
        print("\n=== Add Songs by Artist ===")
        print("1. Single artist")
        print("2. Multiple artists from file")
        
        choice = input("\nEnter choice (1 or 2): ").strip()
        
        if choice == "2":
            file_path = input("Enter the path to your artist list file: ").strip()
            file_path = file_path.strip('"').strip("'")
        
        print("\nSelect mode:")
        print("1. Top 10 songs (fast)")
        print("2. Top N songs (custom number)")
        print("3. All songs (may be slow for prolific artists)")
        
        mode_choice = input("\nEnter mode (1, 2, or 3): ").strip()
        
        mode = 'top10'
        custom_n = None
        
        if mode_choice == "2":
            mode = 'topn'
            custom_n = int(input("How many top songs? "))
        elif mode_choice == "3":
            mode = 'all'
        
        if choice == "2":
            total = add_artists_from_file(sp, playlist_id, file_path, mode, custom_n)
            print(f"\n✓ Total songs added: {total}")
        else:
            artist_name = input("\nEnter artist name: ").strip()
            added = add_artist_songs_to_playlist(sp, playlist_id, artist_name, mode, custom_n)
            print(f"\n✓ Added {added} songs")
        
        print("\n✓ Done!")
    except Exception as e:
        print(f"Error: {e}")
