# Spotify Playlist Creator 🎵
A Python-Flask web app that lets you create and manage Spotify playlists effortlessly. Search songs, build playlists, and enjoy a seamless music curation experience, all while keeping your Spotify credentials secure! 

# Features ✨
## 🎨 User-Friendly Interface
- Web-based dashboard for easy playlist management
- Clean, intuitive design with Spotify's vibrant green theme

## 🎧 Smart Playlist Tools
- Create playlists with custom names/descriptions
- Search & add 10 songs at once (improved from original 4)
- One-click "Finish" to clear session without logging out

## 🔐Spotify API Integration
- Secure OAuth2 Authentication using your API credentials (client ID and secret)
- Token Management: Auto-refreshes expired tokens without user intervention
- Scoped Permissions: Only requests playlist-modify-public and user-library-read access
- Encrypted Sessions: All API calls use HTTPS with Spotify's encrypted endpoints

## ⚡ Technical Highlights
- Handles token expiration automatically
- Prevents duplicate playlist creation
- Clear error messages for smooth troubleshooting

# Technologies Used 🛠️
| Component	| Description |
| ---- | ---- |
| Python | Core backend logic and API interactions |
| Flask	 | Web framework for the dashboard interface |
| Spotipy |	Python library for Spotify Web API integration |
| Spotify API	| Fetch songs, create playlists, and manage user libraries |
| OAuth2 |	Secure authentication flow |
| JavaScript	| Dynamic frontend interactions (search, add songs) |

# Why This Project? 🎯
## The Problem:
Manually creating playlists on Spotify can be tedious. As a music lover and programmer, I wanted to:
- Automate playlist curation while keeping creative control
- Improve the search experience (expanded from 4 to 10 results)
- Add session management so users can create multiple playlists without re-logging in

## Key Improvements:
- ✅ Finish Button: Clears playlist data without logging out (unlike traditional logout)
- ✅ Enhanced Search: More results (10 vs original 4) for better song discovery
- ✅ Error Handling: Friendly alerts for expired tokens or missing playlist

# Security Notes 🔐
**Critical: Protect Your Credentials**

```bash
.env Example (NEVER commit this file!) 
SPOTIPY_CLIENT_ID=your_client_id_here 
SPOTIPY_CLIENT_SECRET=your_client_secret_here 
FLASK_SECRET_KEY=a_random_string_here 
SPOTIPY_REDIRECT_URI=your_spotipy_redirect_uri_here
```

1. Add .env to .gitignore

```bash
echo ".env" >> .gitignore
```

2. Spotify Dashboard Setup
- Register your app at Spotify Developer Dashboard
- Whitelist your redirect URI 

3. Token Safety
- Access tokens auto-expire in 1 hour
- Refresh tokens are stored securely in server sessions

---

https://github.com/user-attachments/assets/a30d0f5e-60fb-479e-8344-4fdb7fe47dbb

