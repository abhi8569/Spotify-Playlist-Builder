import time


def parse_album_input(album_input):
    """
    Parses album input in "Album - Artist" format.
    
    Args:
        album_input: String in format "Album - Artist"
    
    Returns:
        Tuple of (album_name, artist_name)
    """
    if ' - ' in album_input:
        parts = album_input.split(' - ', 1)
        return parts[0].strip(), parts[1].strip()
    else:
        # If no artist specified, just return the album name
        return album_input.strip(), None


def search_album(sp, album_name, artist_name=None, auto_select=False):
    """
    Searches for an album on Spotify.
    
    Args:
        sp: Spotify client object
        album_name: Name of the album
        artist_name: Name of the artist (optional, for better accuracy)
        auto_select: If True, automatically selects the first result
    
    Returns:
        Album object if found, None otherwise
    """
    # Build search query
    if artist_name:
        query = f"album:{album_name} artist:{artist_name}"
    else:
        query = f"album:{album_name}"
    
    results = sp.search(q=query, type='album', limit=5)
    
    if results['albums']['items']:
        albums = results['albums']['items']
        
        if len(albums) == 1:
            album = albums[0]
            artist_names = ', '.join([artist['name'] for artist in album['artists']])
            print(f"Found: {album['name']} by {artist_names} ({album['total_tracks']} tracks)")
            return album
        else:
            # Multiple matches found
            print(f"\nFound {len(albums)} albums:")
            for i, album in enumerate(albums, 1):
                artist_names = ', '.join([artist['name'] for artist in album['artists']])
                print(f"{i}. {album['name']} by {artist_names} ({album['total_tracks']} tracks)")
            
            if auto_select:
                # Auto-select the first one
                selected = albums[0]
                artist_names = ', '.join([artist['name'] for artist in selected['artists']])
                print(f"\n→ Auto-selected: {selected['name']} by {artist_names}")
                return selected
            else:
                # Manual selection
                while True:
                    try:
                        choice = int(input(f"\nSelect album (1-{len(albums)}) or 0 to skip: "))
                        if choice == 0:
                            return None
                        if 1 <= choice <= len(albums):
                            return albums[choice - 1]
                        print(f"Please enter a number between 0 and {len(albums)}")
                    except ValueError:
                        print("Please enter a valid number")
    
    return None


def get_album_tracks(sp, album_id):
    """
    Gets all tracks from an album.
    
    Args:
        sp: Spotify client object
        album_id: Spotify album ID
    
    Returns:
        List of track URIs
    """
    track_uris = []
    results = sp.album_tracks(album_id)
    
    while results:
        for track in results['items']:
            print(f"  - {track['name']}")
            track_uris.append(track['uri'])
        
        if results['next']:
            time.sleep(0.5)
            results = sp.next(results)
        else:
            break
    
    return track_uris


def add_album_to_playlist(sp, playlist_id, album_input, auto_select=False):
    """
    Adds all tracks from an album to a playlist.
    
    Args:
        sp: Spotify client object
        playlist_id: ID of the playlist
        album_input: Album string in "Album - Artist" format
        auto_select: If True, automatically selects first album match
    
    Returns:
        Number of tracks added
    """
    album_name, artist_name = parse_album_input(album_input)
    
    print(f"\nSearching for album: {album_name}" + (f" by {artist_name}" if artist_name else ""))
    album = search_album(sp, album_name, artist_name, auto_select=auto_select)
    
    if not album:
        print(f"✗ Album not found: {album_input}")
        return 0
    
    album_id = album['id']
    album_name = album['name']
    artist_names = ', '.join([artist['name'] for artist in album['artists']])
    
    print(f"\nFetching tracks from {album_name} by {artist_names}...")
    track_uris = get_album_tracks(sp, album_id)
    
    if not track_uris:
        print("✗ No tracks found")
        return 0
    
    print(f"\nAdding {len(track_uris)} tracks to playlist...")
    
    try:
        sp.playlist_add_items(playlist_id, track_uris)
        print(f"✓ Added {len(track_uris)} tracks")
        return len(track_uris)
    except Exception as e:
        print(f"✗ Error adding tracks: {e}")
        return 0


def add_albums_from_file(sp, playlist_id, file_path, auto_select=False):
    """
    Adds tracks from multiple albums listed in a file.
    
    Args:
        sp: Spotify client object
        playlist_id: ID of the playlist
        file_path: Path to file with album entries (one per line)
        auto_select: If True, automatically selects first album match
    
    Returns:
        Total number of tracks added
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            albums = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"✗ File not found: {file_path}")
        return 0
    except Exception as e:
        print(f"✗ Error reading file: {e}")
        return 0
    
    if not albums:
        print("✗ No albums found in file")
        return 0
    
    print(f"\n=== Processing {len(albums)} albums ===\n")
    
    total_added = 0
    for i, album in enumerate(albums, 1):
        print(f"\n[{i}/{len(albums)}] Processing: {album}")
        print("-" * 50)
        
        added = add_album_to_playlist(sp, playlist_id, album, auto_select=auto_select)
        total_added += added
        
        if i < len(albums):
            print("\nWaiting 3 seconds before next album...")
            time.sleep(3)
    
    return total_added


if __name__ == "__main__":
    from core.auth import connect_spotify
    from core.playlist import get_or_create_playlist
    
    try:
        sp = connect_spotify()
        playlist_id = get_or_create_playlist(sp)
        
        print("\n=== Add Albums ===")
        print("1. Single album")
        print("2. Multiple albums from file")
        
        choice = input("\nEnter choice (1 or 2): ").strip()
        
        # Ask about auto-select
        print("\nWhen multiple albums match:")
        print("1. Auto-select first match")
        print("2. Let me choose manually")
        
        auto_choice = input("\nEnter choice (1 or 2, default: 2): ").strip()
        auto_select = (auto_choice == "1")
        
        if choice == "2":
            file_path = input("\nEnter the path to your album list file: ").strip()
            file_path = file_path.strip('"').strip("'")
            
            total = add_albums_from_file(sp, playlist_id, file_path, auto_select=auto_select)
            print(f"\n✓ Total tracks added: {total}")
        else:
            album_input = input("\nEnter album in 'Album - Artist' format: ").strip()
            added = add_album_to_playlist(sp, playlist_id, album_input, auto_select=auto_select)
            print(f"\n✓ Added {added} tracks")
        
        print("\n✓ Done!")
    except Exception as e:
        print(f"Error: {e}")
