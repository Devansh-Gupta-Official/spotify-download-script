import spotipy
from spotipy.oauth2 import SpotifyOAuth   #The SpotifyOAuth class provided by this module is specifically designed for handling the OAuth 2.0 authorization process when interacting with the Spotify API.
from dotenv import load_dotenv
import os
import csv


load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
playlist_link = 'https://open.spotify.com/playlist/00i82lDzMDdiHWNjrIGAyw?si=DzmeuZbeRheqRK2DH6R-OA'
#Extracting playlist uri from link
uri = playlist_link.split("/")[-1].split("?")[0]
def get_tracks(playlist_id,access_token):
    ## Set up Spotipy with the access token
    session = spotipy.Spotify(auth=access_token)
    
    #get list of tracks in a given playlist
    track = session.playlist_tracks(playlist_id)['items']
    return track, session


