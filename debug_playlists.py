from auth import connect_spotify
import time

# Quick debug script to check what playlists are returned
sp = connect_spotify()

print("\n=== Debugging Playlist List ===")

# Add a small delay in case of API sync issues
time.sleep(1)

results = sp.current_user_playlists(limit=50)

print(f"Total playlists found: {results['total']}")
print(f"Items in this batch: {len(results['items'])}\n")

for i, playlist in enumerate(results['items'], 1):
    owner = playlist['owner']['display_name']
    public = "Public" if playlist['public'] else "Private"
    print(f"{i}. {playlist['name']}")
    print(f"   Owner: {owner} | {public} | ID: {playlist['id']}")

print(f"\nShowing {len(results['items'])} of {results['total']} playlists")

# Also check the user info
user = sp.current_user()
print(f"\nLogged in as: {user['display_name']} (ID: {user['id']})")
