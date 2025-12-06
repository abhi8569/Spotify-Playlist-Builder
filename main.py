from auth import connect_spotify
from playlist import get_or_create_playlist
from search import add_song_interactive, add_songs_from_list, read_songs_from_file
from artist import add_artist_songs_to_playlist, add_artists_from_file


def main():
    """
    Main entry point for Spotify Playlist Manager.
    """
    print("=" * 60)
    print("          SPOTIFY PLAYLIST MANAGER")
    print("=" * 60)
    
    try:
        # Step 1: Authenticate
        sp = connect_spotify()
        
        # Step 2: Select or create playlist
        playlist_id = get_or_create_playlist(sp)
        
        # Step 3: Add songs or artists
        while True:
            print("\n" + "=" * 60)
            print("WHAT WOULD YOU LIKE TO ADD?")
            print("=" * 60)
            print("1. Add songs (by name)")
            print("2. Add songs by artist")
            print("3. Exit")
            
            choice = input("\nEnter choice (1, 2, or 3): ").strip()
            
            if choice == "1":
                # Add songs workflow
                add_songs_workflow(sp, playlist_id)
            
            elif choice == "2":
                # Add artists workflow
                add_artists_workflow(sp, playlist_id)
            
            elif choice == "3":
                print("\n✓ Done! Enjoy your playlist!")
                break
            
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nError: {e}")


def add_songs_workflow(sp, playlist_id):
    """
    Workflow for adding songs by name.
    """
    print("\n" + "-" * 60)
    print("ADD SONGS BY NAME")
    print("-" * 60)
    print("1. Add songs one by one (interactive)")
    print("2. Add songs from a file")
    print("3. Add songs from manual input (batch)")
    print("4. Back to main menu")
    
    choice = input("\nEnter choice (1, 2, 3, or 4): ").strip()
    
    if choice == "1":
        # Interactive mode
        while True:
            add_song_interactive(sp, playlist_id)
            another = input("\nAdd another song? (y/n): ").strip().lower()
            if another != 'y':
                break
    
    elif choice == "2":
        # File input mode
        print("\n=== File Input Mode ===")
        file_path = input("Enter the path to your song list file: ").strip()
        file_path = file_path.strip('"').strip("'")
        
        songs = read_songs_from_file(file_path)
        
        if songs:
            print(f"\nFound {len(songs)} songs in file.")
            confirm = input("Proceed to add them? (y/n): ").strip().lower()
            
            if confirm == 'y':
                successful, failed = add_songs_from_list(sp, playlist_id, songs)
                
                print("\n" + "=" * 50)
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
            
            print("\n" + "=" * 50)
            print(f"✓ Successfully added: {successful}/{len(songs)} songs")
            
            if failed:
                print(f"\n✗ Failed to add ({len(failed)}):")
                for song in failed:
                    print(f"  - {song}")
        else:
            print("No songs entered.")
    
    elif choice == "4":
        return
    
    else:
        print("Invalid choice.")


def add_artists_workflow(sp, playlist_id):
    """
    Workflow for adding songs by artist.
    """
    print("\n" + "-" * 60)
    print("ADD SONGS BY ARTIST")
    print("-" * 60)
    print("1. Single artist")
    print("2. Multiple artists from file")
    print("3. Back to main menu")
    
    choice = input("\nEnter choice (1, 2, or 3): ").strip()
    
    if choice == "3":
        return
    
    # Ask about artist selection preference
    print("\nWhen multiple artists match:")
    print("1. Auto-select first match (highest followers)")
    print("2. Let me choose manually")
    
    auto_choice = input("\nEnter choice (1 or 2, default: 2): ").strip()
    auto_select = (auto_choice == "1")
    
    # Get mode selection
    print("\nSelect mode:")
    print("1. Top 10 songs (fast)")
    print("2. Top N songs (custom number)")
    print("3. All songs (may be slow for prolific artists)")
    
    mode_choice = input("\nEnter mode (1, 2, or 3): ").strip()
    
    mode = 'top10'
    custom_n = None
    
    if mode_choice == "2":
        mode = 'topn'
        while True:
            try:
                custom_n = int(input("How many top songs? "))
                if custom_n > 0:
                    break
                print("Please enter a positive number.")
            except ValueError:
                print("Please enter a valid number.")
    elif mode_choice == "3":
        mode = 'all'
    
    # Process artists
    if choice == "1":
        # Single artist
        artist_name = input("\nEnter artist name: ").strip()
        if artist_name:
            added = add_artist_songs_to_playlist(sp, playlist_id, artist_name, mode, custom_n, auto_select=auto_select)
            print(f"\n✓ Added {added} songs")
    
    elif choice == "2":
        # Multiple artists from file
        file_path = input("\nEnter the path to your artist list file: ").strip()
        file_path = file_path.strip('"').strip("'")
        
        total = add_artists_from_file(sp, playlist_id, file_path, mode, custom_n, auto_select=auto_select)
        print(f"\n✓ Total songs added: {total}")
    
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
