// API helper function
async function apiCall(endpoint, data) {
    const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    return await response.json();
}

// Create playlist
async function createPlaylist() {
    const name = document.getElementById('newPlaylistName').value.trim();
    const description = document.getElementById('newPlaylistDesc').value.trim();
    const isPublic = document.getElementById('newPlaylistPublic').checked;

    if (!name) {
        alert('Please enter a playlist name');
        return;
    }

    try {
        const result = await apiCall('/api/playlists/create', {
            name,
            description,
            public: isPublic
        });

        if (result.success) {
            alert('Playlist created successfully!');
            location.reload();  // Reload to show new playlist
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        alert('Error creating playlist: ' + error);
    }
}

// Add songs
async function addSongs() {
    if (!window.selectedPlaylistId) {
        alert('Please select a playlist first');
        return;
    }

    const songsText = document.getElementById('songsInput').value.trim();
    if (!songsText) {
        alert('Please enter some songs');
        return;
    }

    const songs = songsText.split('\n').filter(s => s.trim());

    // Show progress
    document.getElementById('songsProgress').style.display = 'block';
    document.getElementById('songsResult').innerHTML = '';
    document.getElementById('addSongsBtn').disabled = true;

    try {
        const result = await apiCall('/api/add-songs', {
            playlist_id: window.selectedPlaylistId,
            songs
        });

        document.getElementById('songsProgress').style.display = 'none';
        document.getElementById('addSongsBtn').disabled = false;

        if (result.success) {
            let html = `<div class="alert alert-success">
                ✓ Successfully added ${result.added} out of ${result.total} songs
            </div>`;

            if (result.failed.length > 0) {
                html += `<div class="alert alert-warning">
                    Failed to add ${result.failed.length} songs:<br>
                    <small>${result.failed.join('<br>')}</small>
                </div>`;
            }

            document.getElementById('songsResult').innerHTML = html;
            document.getElementById('songsInput').value = '';
        } else {
            document.getElementById('songsResult').innerHTML = `<div class="alert alert-danger">Error: ${result.error}</div>`;
        }
    } catch (error) {
        document.getElementById('songsProgress').style.display = 'none';
        document.getElementById('addSongsBtn').disabled = false;
        document.getElementById('songsResult').innerHTML = `<div class="alert alert-danger">Error: ${error}</div>`;
    }
}

// Add artists (batch)
async function addArtists() {
    if (!window.selectedPlaylistId) {
        alert('Please select a playlist first');
        return;
    }

    const artistsText = document.getElementById('artistsInput').value.trim();
    if (!artistsText) {
        alert('Please enter some artist names');
        return;
    }

    const artists = artistsText.split('\n').filter(a => a.trim());
    const mode = document.getElementById('artistMode').value;
    let customN = null;
    if (mode === 'topn') {
        customN = parseInt(document.getElementById('customN').value);
    }

    // Show progress
    document.getElementById('artistProgress').style.display = 'block';
    document.getElementById('artistResult').innerHTML = '';
    document.getElementById('addArtistBtn').disabled = true;

    try {
        let totalAdded = 0;
        let results = [];

        for (let i = 0; i < artists.length; i++) {
            const artist = artists[i].trim();
            if (!artist) continue;

            document.getElementById('artistProgress').innerHTML = `
                <div class="progress">
                    <div class="progress-bar progress-bar-striped progress-bar-animated" style="width: 100%"></div>
                </div>
                <p class="text-muted mt-2">Processing ${i + 1} of ${artists.length}: ${artist}</p>
            `;

            const result = await apiCall('/api/add-artist', {
                playlist_id: window.selectedPlaylistId,
                artist_name: artist,
                mode,
                custom_n: customN,
                auto_select: true
            });

            if (result.success) {
                totalAdded += result.added;
                results.push(`✓ ${artist}: ${result.added} songs`);
            } else {
                results.push(`✗ ${artist}: ${result.error}`);
            }
        }

        document.getElementById('artistProgress').style.display = 'none';
        document.getElementById('addArtistBtn').disabled = false;

        let html = `<div class="alert alert-success">
            ✓ Successfully added ${totalAdded} total songs from ${artists.length} artists
        </div>`;

        html += '<div class="alert alert-info"><small>' + results.join('<br>') + '</small></div>';

        document.getElementById('artistResult').innerHTML = html;
        document.getElementById('artistsInput').value = '';
    } catch (error) {
        document.getElementById('artistProgress').style.display = 'none';
        document.getElementById('addArtistBtn').disabled = false;
        document.getElementById('artistResult').innerHTML = `<div class="alert alert-danger">Error: ${error}</div>`;
    }
}

// Add albums (batch)
async function addAlbums() {
    if (!window.selectedPlaylistId) {
        alert('Please select a playlist first');
        return;
    }

    const albumsText = document.getElementById('albumsInput').value.trim();
    if (!albumsText) {
        alert('Please enter some albums');
        return;
    }

    const albums = albumsText.split('\n').filter(a => a.trim());

    // Show progress
    document.getElementById('albumProgress').style.display = 'block';
    document.getElementById('albumResult').innerHTML = '';
    document.getElementById('addAlbumBtn').disabled = true;

    try {
        let totalAdded = 0;
        let results = [];

        for (let i = 0; i < albums.length; i++) {
            const album = albums[i].trim();
            if (!album) continue;

            document.getElementById('albumProgress').innerHTML = `
                <div class="progress">
                    <div class="progress-bar progress-bar-striped progress-bar-animated" style="width: 100%"></div>
                </div>
                <p class="text-muted mt-2">Processing ${i + 1} of ${albums.length}: ${album}</p>
            `;

            const result = await apiCall('/api/add-album', {
                playlist_id: window.selectedPlaylistId,
                album_input: album,
                auto_select: true
            });

            if (result.success) {
                totalAdded += result.added;
                results.push(`✓ ${album}: ${result.added} tracks`);
            } else {
                results.push(`✗ ${album}: ${result.error}`);
            }
        }

        document.getElementById('albumProgress').style.display = 'none';
        document.getElementById('addAlbumBtn').disabled = false;

        let html = `<div class="alert alert-success">
            ✓ Successfully added ${totalAdded} total tracks from ${albums.length} albums
        </div>`;

        html += '<div class="alert alert-info"><small>' + results.join('<br>') + '</small></div>';

        document.getElementById('albumResult').innerHTML = html;
        document.getElementById('albumsInput').value = '';
    } catch (error) {
        document.getElementById('albumProgress').style.display = 'none';
        document.getElementById('addAlbumBtn').disabled = false;
        document.getElementById('albumResult').innerHTML = `<div class="alert alert-danger">Error: ${error}</div>`;
    }
}
