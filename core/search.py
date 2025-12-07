def parse_song_input(song_input):
    """
    Parses song input in "Song Name - Artist" format.
    
    Args:
        song_input: String in format "Song Name - Artist"
    
    Returns:
        Tuple of (song_name, artist_name)
    """
    if ' - ' in song_input:
        parts = song_input.split(' - ', 1)
        return parts[0].strip(), parts[1].strip()
    else:
        # If no artist specified, just return the song name
        return song_input.strip(), None


def search_song(sp, song_name, artist_name=None):
    """
    Searches for a song on Spotify.
    
    Args:
        sp: Spotify client object
        song_name: Name of the song
        artist_name: Name of the artist (optional, for better accuracy)
    
    Returns:
        Track URI if found, None otherwise
    """
    # Build search query
    if artist_name:
        query = f"track:{song_name} artist:{artist_name}"
    else:
        query = f"track:{song_name}"
    
    results = sp.search(q=query, type='track', limit=10)
    
    if results['tracks']['items']:
        # Get the first result (most relevant)
        track = results['tracks']['items'][0]
        
        # If artist was specified, verify it matches (to avoid covers)
        if artist_name:
            track_artists = [artist['name'].lower() for artist in track['artists']]
            if not any(artist_name.lower() in artist for artist in track_artists):
                # Try to find a better match
                for track in results['tracks']['items']:
                    track_artists = [artist['name'].lower() for artist in track['artists']]
                    if any(artist_name.lower() in artist for artist in track_artists):
                        print(f"Found: {track['name']} by {', '.join([a['name'] for a in track['artists']])}")
                        return track['uri']
                # No exact match found
                return None
        
        print(f"Found: {track['name']} by {', '.join([a['name'] for a in track['artists']])}")
        return track['uri']
    
    return None


def add_song_to_playlist(sp, playlist_id, track_uri):
    """
    Adds a song to a playlist.
    
    Args:
        sp: Spotify client object
        playlist_id: ID of the playlist
        track_uri: URI of the track to add
    
    Returns:
        True if successful, False otherwise
    """
    try:
        sp.playlist_add_items(playlist_id, [track_uri])
        print("✓ Song added to playlist successfully!")
        return True
    except Exception as e:
        print(f"✗ Failed to add song: {e}")
        return False


def add_song_interactive(sp, playlist_id):
    """
    Interactive function to add a song to a playlist.
    User provides input in "Song Name - Artist" format.
    
    Args:
        sp: Spotify client object
        playlist_id: ID of the playlist to add to
    """
    print("\n=== Add Song to Playlist ===")
    print("Format: 'Song Name - Artist' (e.g., 'Shape of You - Ed Sheeran')")
    
    song_input = input("\nEnter song: ").strip()
    
    if not song_input:
        print("✗ No song entered.")
        return False
    
    song_name, artist_name = parse_song_input(song_input)
    
    print(f"\nSearching for: {song_name}" + (f" by {artist_name}" if artist_name else ""))
    
    track_uri = search_song(sp, song_name, artist_name)
    
    if track_uri:
        return add_song_to_playlist(sp, playlist_id, track_uri)
    else:
        print(f"✗ Song not found: {song_input}")
        if artist_name:
            print("  Tip: Make sure the artist name is spelled correctly.")
        return False


import time


def add_songs_from_list(sp, playlist_id, song_list):
    """
    Adds multiple songs to a playlist from a list.
    
    Args:
        sp: Spotify client object
        playlist_id: ID of the playlist to add to
        song_list: List of song strings in "Song Name - Artist" format
    
    Returns:
        Tuple of (successful_count, failed_songs)
    """
    successful = 0
    failed = []
    
    print(f"\n=== Adding {len(song_list)} songs to playlist ===\n")
    
    for i, song_input in enumerate(song_list, 1):
        song_input = song_input.strip()
        if not song_input:
            continue
        
        print(f"[{i}/{len(song_list)}] Processing: {song_input}")
        
        song_name, artist_name = parse_song_input(song_input)
        track_uri = search_song(sp, song_name, artist_name)
        
        if track_uri:
            if add_song_to_playlist(sp, playlist_id, track_uri):
                successful += 1
            else:
                failed.append(song_input)
        else:
            print(f"✗ Song not found: {song_input}")
            failed.append(song_input)
        
        # Add delay between songs to avoid rate limiting
        if i < len(song_list):
            print("Waiting 3 seconds...")
            time.sleep(3)
        
        print()  # Blank line between songs
    
    return successful, failed


def read_songs_from_file(file_path):
    """
    Reads songs from a text file.
    Each line should be in "Song Name - Artist" format.
    
    Args:
        file_path: Path to the text file
    
    Returns:
        List of song strings
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            songs = [line.strip() for line in f if line.strip()]
        return songs
    except FileNotFoundError:
        print(f"✗ File not found: {file_path}")
        return []
    except Exception as e:
        print(f"✗ Error reading file: {e}")
        return []


if __name__ == "__main__":
    from core.auth import connect_spotify
    from core.playlist import get_or_create_playlist
    
    try:
        sp = connect_spotify()
        playlist_id = get_or_create_playlist(sp)
        
        print("\n=== Add Songs ===")
        print("Choose an option:")
        print("1. Add songs one by one (interactive)")
        print("2. Add songs from a file")
        print("3. Add songs from manual input (batch)")
        
        choice = input("\nEnter choice (1, 2, or 3): ").strip()
        
        if choice == "2":
            # File input mode
            print("\n=== File Input Mode ===")
            file_path = input("Enter the path to your song list file: ").strip()
            
            # Remove quotes if user wrapped the path in quotes
            file_path = file_path.strip('"').strip("'")
            
            songs = read_songs_from_file(file_path)
            
            if songs:
                print(f"\nFound {len(songs)} songs in file.")
                confirm = input("Proceed to add them? (y/n): ").strip().lower()
                
                if confirm == 'y':
                    successful, failed = add_songs_from_list(sp, playlist_id, songs)
                    
                    print("\n" + "="*50)
                    print(f"✓ Successfully added: {successful}/{len(songs)} songs")
                    
                    if failed:
                        print(f"\n✗ Failed to add ({len(failed)}):")
                        for song in failed:
                            print(f"  - {song}")
            else:
                print("No songs to add.")
        
        elif choice == "3":
            # Manual batch input mode
            print("\n=== Manual Batch Mode ===")
            print("Enter songs in 'Song Name - Artist' format, one per line.")
            print("When done, enter a blank line.\n")
            
            songs = []
            while True:
                song = input(f"Song {len(songs) + 1}: ").strip()
                if not song:
                    break
                songs.append(song)
            
            if songs:
                successful, failed = add_songs_from_list(sp, playlist_id, songs)
                
                print("\n" + "="*50)
                print(f"✓ Successfully added: {successful}/{len(songs)} songs")
                
                if failed:
                    print(f"\n✗ Failed to add ({len(failed)}):")
                    for song in failed:
                        print(f"  - {song}")
            else:
                print("No songs entered.")
        
        else:
            # Interactive mode (one by one)
            while True:
                success = add_song_interactive(sp, playlist_id)
                
                another = input("\nAdd another song? (y/n): ").strip().lower()
                if another != 'y':
                    break
        
        print("\n✓ Done!")
    except Exception as e:
        print(f"Error: {e}")
