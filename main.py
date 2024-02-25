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


tracks,session = get_tracks(uri,ACCESS_TOKEN)

#INITIALIZE A CSV FILE IN WHICH YOU COPY ALL INFO REGARDING A TRACK
with open("track.csv", "w", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Name","Artist","Album Name","Album Release Date"])


    for track in tracks:
        name = track['track']['name']     #TRACK NAME
        # #Main Artist
        # artist_uri = track["track"]["artists"][0]["uri"]
        # artist_info = sp.artist(artist_uri)
        # #Name, popularity, genre
        # artist_name = track["track"]["artists"][0]["name"]
        # artist_pop = artist_info["popularity"]
        # artist_genres = artist_info["genres"]
        artists = ','.join(artist['name'] for artist in track['track']['artists'])   #ARTISTS NAME
        album_name = track['track']['album']['name']    #ALBUM NAME
        track_popularity = track["track"]["popularity"]      #TRACK POPULARITY

        album_id = track['track']['album']['id']    #ALBUM ID
        track_id = track['track']['id']     #TRACK ID
        #extracting other features (not of use)
        features=session.audio_features(track_id)[0]
        album_release_date = session.album(album_id)['release_date']     #ALBUM RELEASE DATE

        # danceability = features['danceability']
        # energy = features['energy']
        # key = features['key']
        # loudness = features['loudness']
        # mode=features['mode']
        # speechiness = features['speechiness']
        # acousticness = features['acousticness']
        # intstrumentalness = features['intstrumentalness']
        # liveness = features['liveness']
        # valence = features['valence']
        # tempo = features['tempo']

        writer.writerow([name,artists,album_name,album_release_date])
