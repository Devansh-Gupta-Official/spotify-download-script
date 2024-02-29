import streamlit as st
from pytube import YouTube
import requests
import base64
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth 
import os
import csv
from googleapiclient.discovery import build
import pandas as pd
import re
import time
import json
from streamlit_lottie import st_lottie

st.set_page_config(
    page_title="Hello",
    page_icon="🏠",
)

def load_animations(filepath:str):
    with open(filepath,'r',encoding="utf8") as f:
        return json.load(f)

spotify = load_animations("spotify.json")

with st.sidebar:
    st_lottie(
        spotify,
        speed=1,
        reverse=False,
        loop=True,
        quality='medium',
        height=None,
        width=None,
        key="spotify"
    )



value = st.sidebar.selectbox(label="Select your Link Type",options=["Playlist","Album"],index=None,placeholder="Select an Option")

st.title(":musical_note: SPOTIFY")
st.header("Convert your Spotify Playlist to MP3 Files")

st.write("")
st.write("")
st.write("")

if value=='Album':
    st.write("Album")

else:
    form = st.form(key='form_playlist')
    playlist_link = form.text_input(label="Enter Spotify Playlist Link",placeholder='Eg: https://open.spotify.com/playlist/00i82lDzMDdiHWNjrIGAyw?si=DzmeuZbeRheqRK2DH6R-OA')
    submit = form.form_submit_button(label='Submit')


    if submit:
        load_dotenv()

        CLIENT_ID = os.getenv("CLIENT_ID")
        CLIENT_SECRET = os.getenv("CLIENT_SECRET")

        client_credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"    
        encoded_client_creds = base64.b64encode(client_credentials.encode())

        auth_url = 'https://accounts.spotify.com/api/token'


        headers={
            'Authorization':f"Basic {encoded_client_creds.decode()}"
        }

        form={
            'grant_type':'client_credentials'
        }

        response = requests.post(auth_url,data=form,headers=headers)


        if response.status_code==200:
            access_token=response.json()['access_token']
            print("sucessful")
        else:
            print("error")

        os.environ['ACCESS_TOKEN'] = access_token

        with open('.env', 'r') as f:
            lines = f.readlines()

        updated_lines = []
        found_access_token = False
        for line in lines:
            if line.startswith('ACCESS_TOKEN='):
                updated_lines.append(f'ACCESS_TOKEN="{access_token}"\n')
                found_access_token = True
            else:
                updated_lines.append(line)

        if not found_access_token:
            updated_lines.append(f'ACCESS_TOKEN="{access_token}"\n')

        with open('.env', 'w') as f:
            f.writelines(updated_lines)


        ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")


        uri = playlist_link.split("/")[-1].split("?")[0]


        # API_KEY=os.getenv("YOUTUBE_API_KEY")

        def get_tracks(playlist_id,access_token):
            
            session = spotipy.Spotify(auth=access_token)
            track = session.playlist_tracks(playlist_id)['items']
            return track, session

        # def get_video_url(name):
        #     youtube=build('youtube','v3',developerKey=API_KEY)
        #     request = youtube.search().list(part='snippet',type='video',q=name,maxResults=1)
        #     response=request.execute()
        #     id = response['items'][0]['id']['videoId']  
        #     videoURL=f"https://www.youtube.com/watch?v={id}"  
        #     return videoURL

        tracks,session = get_tracks(uri,ACCESS_TOKEN)

        # script_directory = os.path.dirname(os.path.abspath(__file__))
        # mp3_directory = os.path.join(script_directory,"downloads_mp3")
        # os.makedirs(mp3_directory, exist_ok=True)

        progress_text = "Operation in progress. Please wait."
        p=0
        bar = st.progress(p,text=progress_text)

        n = len(tracks)

        for track in tracks:
                # name = track['track']['name']     
                # artists = ','.join(artist['name'] for artist in track['track']['artists'])  
                # keyword=f"{name},{artists}"  
                # url = get_video_url(keyword)
                # video = YouTube(url)           
                # try:
                #     stream = video.streams.filter(only_audio=True).first()
                #     title = re.sub(r'[^\w\-_\. ]', '_', video.title)
                #     stream.download(output_path=mp3_directory,filename=f"{title}.mp3")
                #     print(f"Download of Song {video.title} is completed successfully")
                # except:
                #     print("An error has occurred")
                #     print(url)
                time.sleep(0.5)
                bar=bar.progress(p+1,text=progress_text)
                p+=int(100/n)
        bar=bar.progress(100)
        st.success("Completed")
        mp3 = load_animations("mp3.json")
        with st.sidebar:
                st_lottie(
                        mp3,
                        speed=1,
                        reverse=False,
                        loop=True,
                        quality='medium',
                        height=None,
                        width=None,
                        key="mp3"
                    )














# import auth
# import spotify
# import youtube
# import downloading_mp3

# auth.run()
# spotify.run()
# youtube.run()
# downloading_mp3.run()