from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time 
import json

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")  

sp_oauth = SpotifyOAuth(
    client_id=os.getenv("client_id"),
    client_secret=os.getenv("client_secret"),
    redirect_uri="redirect_uri",  
    scope="playlist-modify-public user-library-read"
)

def get_spotify_client():
    """Helper function to get a Spotify client with valid token"""
    if 'token_info' not in session:
        return None
        
    token_info = session['token_info']
    
    if time.time() > token_info['expires_at']:
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        token_info['expires_at'] = int(time.time()) + token_info['expires_in']
        session['token_info'] = token_info
    
    return spotipy.Spotify(auth=token_info['access_token'])

@app.route("/")
def home():
    if 'token_info' in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/login")
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    try:
        token_info = sp_oauth.get_access_token(request.args["code"], as_dict=False)
        if token_info:
            if not isinstance(token_info, dict):
                token_info = {
                    'access_token': token_info,
                    'refresh_token': sp_oauth.get_cached_token().get('refresh_token'),
                    'expires_in': 3600 
                }
            token_info['expires_at'] = int(time.time()) + token_info.get('expires_in', 3600)
            session['token_info'] = token_info
            return redirect(url_for("dashboard"))
        return "Invalid token response", 400
    except Exception as e:
        return f"Authentication failed: {str(e)}", 400

@app.route("/dashboard")
def dashboard():
    if 'token_info' not in session:
        return redirect(url_for("login"))
    
    sp = get_spotify_client()
    user_info = sp.current_user()
    return render_template("dashboard.html", username=user_info['display_name'])

@app.route("/search")
def search():
    sp = get_spotify_client()
    if not sp:
        return jsonify({"error": "Not logged in"}), 401
    
    try:
        query = request.args.get("q")
        results = sp.search(q=query, type="track", limit=10)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/create_playlist", methods=["POST"])
def create_playlist():
    sp = get_spotify_client()
    if not sp:
        return jsonify({"error": "Not logged in"}), 401
    
    try:
        playlist_name = request.form.get("playlist_name")
        if not playlist_name or not playlist_name.strip():
            return jsonify({"error": "Playlist name is required"}), 400

        playlist = sp.user_playlist_create(
            user=sp.current_user()["id"],
            name=playlist_name.strip(),
            public=True,
            description=request.form.get("playlist_description", "").strip()
        )
        
        session['current_playlist_id'] = playlist['id']
        return jsonify({
            "success": True,
            "playlist": {
                "id": playlist['id'],
                "name": playlist['name'],
                "url": playlist['external_urls']['spotify']
            }
        })
    except spotipy.SpotifyException as e:
        return jsonify({"error": f"Spotify API error: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/add_to_playlist", methods=["POST"])
def add_to_playlist():
    sp = get_spotify_client()
    if not sp:
        return jsonify({"error": "Not logged in"}), 401
    
    try:
        # Handle both JSON and form data
        if request.headers.get('Content-Type') == 'application/json':
            data = request.get_json()
            track_uri = data.get('track_uri')
        else:
            track_uri = request.form.get('track_uri')
        
        if not track_uri:
            return jsonify({"error": "Missing track_uri"}), 400
        
        playlist_id = session.get('current_playlist_id')
        if not playlist_id:
            return jsonify({"error": "No active playlist"}), 400
            
        sp.playlist_add_items(playlist_id, [track_uri])
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/finish")
def finish_session():
    if 'current_playlist_id' in session:
        session.pop('current_playlist_id')
    return jsonify({"success": True, "message": "Playlist session cleared"})

if __name__ == "__main__":
    app.run(debug=True)