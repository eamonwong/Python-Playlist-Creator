let isCreatingPlaylist = false;

document.getElementById("create-playlist-btn").addEventListener("click", async function() {
    if (isCreatingPlaylist) return;
    
    const btn = this;
    const playlistName = document.getElementById("playlist-name").value.trim();
    const playlistDesc = document.getElementById("playlist-desc").value.trim();
    
    if (!playlistName) {
        alert("Please enter a valid playlist name");
        return;
    }

    isCreatingPlaylist = true;
    btn.disabled = true;
    btn.textContent = "Creating...";
    
    try {
        const formData = new URLSearchParams();
        formData.append("playlist_name", playlistName);
        if (playlistDesc) formData.append("playlist_description", playlistDesc);

        const response = await fetch("/create_playlist", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: formData
        });
        
        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.error || "Failed to create playlist");
        }
        
        alert(`Successfully created playlist: ${result.playlist.name}`);
    } catch (error) {
        alert(error.message);
    } finally {
        btn.disabled = false;
        btn.textContent = "Create Playlist";
        isCreatingPlaylist = false;
    }
});

// ===== SONG SEARCH =====
async function searchSong() {
    const query = document.getElementById("song-search").value;
    if (!query) return;

    const resultsDiv = document.getElementById("search-results");
    resultsDiv.innerHTML = "<p>Searching...</p>";

    try {
        const response = await fetch(`/search?q=${encodeURIComponent(query)}`);
        const results = await response.json();
        resultsDiv.innerHTML = "";
        
        results.tracks.items.forEach((track, index) => {
            const trackElement = document.createElement("div");
            trackElement.className = "track";
            trackElement.innerHTML = `
                <p>${index + 1}. <strong>${track.name}</strong> by ${track.artists.map(a => a.name).join(", ")}</p>
                <button onclick="addToPlaylist('${track.uri}')">Add to Playlist</button>
            `;
            resultsDiv.appendChild(trackElement);
        });
    } catch (error) {
        resultsDiv.innerHTML = `<p class="error">Error: ${error.message}</p>`;
    }
}

async function addToPlaylist(trackUri) {
    try {
        const response = await fetch("/add_to_playlist", {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                track_uri: trackUri
            })
        });
        
        const result = await response.json();
        if (result.success) {
            alert("Song added successfully!");
        } else {
            alert("Error: " + (result.error || "Failed to add song"));
        }
    } catch (error) {
        alert("Failed to add song: " + error);
    }
}

document.getElementById("finish-btn").addEventListener("click", function() {
    if (confirm("Playlist completed! 🎉\nReady to finish?")) {
        fetch("/finish")
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById("playlist-name").value = "";
                    document.getElementById("playlist-desc").value = "";
                    document.getElementById("search-results").innerHTML = "";
                    alert("You're all set! You'll stay logged in to create more playlists.");
                }
            });
    }
});

document.getElementById("song-search").addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        searchSong();
    }
});