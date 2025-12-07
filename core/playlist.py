from .auth import connect_spotify


def list_user_playlists(sp):
    """
    Lists all playlists for the current user.
    Returns a list of playlist dictionaries with 'name' and 'id'.
    """
    playlists = []
    results = sp.current_user_playlists()
    
    while results:
        for playlist in results['items']:
            playlists.append({
                'name': playlist['name'],
                'id': playlist['id']
            })
        
        # Check if there are more playlists
        if results['next']:
            results = sp.next(results)
        else:
            break
    
    return playlists


def create_playlist(sp, name, description="", public=True):
    """
    Creates a new playlist for the current user.
    
    Args:
        sp: Spotify client object
        name: Name of the playlist
        description: Description of the playlist (optional)
        public: Whether the playlist should be public (default: True)
    
    Returns:
        Playlist ID
    """
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(
        user=user_id,
        name=name,
        public=public,
        description=description
    )
    print(f"Created playlist: {playlist['name']} (ID: {playlist['id']})")
    return playlist['id']


def get_or_create_playlist(sp):
    """
    Interactive function to let user select an existing playlist or create a new one.
    
    Returns:
        Playlist ID
    """
    print("\n=== Playlist Selection ===")
    playlists = list_user_playlists(sp)
    
    if playlists:
        print("\nYour existing playlists:")
        for i, playlist in enumerate(playlists, 1):
            print(f"{i}. {playlist['name']}")
        
        print(f"\n{len(playlists) + 1}. Create a new playlist")
        
        while True:
            try:
                choice = int(input(f"\nSelect a playlist (1-{len(playlists) + 1}): "))
                if 1 <= choice <= len(playlists):
                    selected = playlists[choice - 1]
                    print(f"Selected: {selected['name']}")
                    return selected['id']
                elif choice == len(playlists) + 1:
                    break
                else:
                    print(f"Please enter a number between 1 and {len(playlists) + 1}")
            except ValueError:
                print("Please enter a valid number")
    else:
        print("You don't have any playlists yet.")
    
    # Create new playlist
    name = input("\nEnter the name for the new playlist: ").strip()
    if not name:
        print("Playlist name cannot be empty. Using 'My Playlist' as default.")
        name = "My Playlist"
    
    description = input("Enter a description (optional, press Enter to skip): ").strip()
    
    public_choice = input("Make it public? (y/n, default: y): ").strip().lower()
    public = public_choice != 'n'
    
    return create_playlist(sp, name, description, public)


if __name__ == "__main__":
    try:
        sp = connect_spotify()
        playlist_id = get_or_create_playlist(sp)
        print(f"\nFinal playlist ID: {playlist_id}")
    except Exception as e:
        print(f"Error: {e}")
