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
from zipfile import ZipFile 
import shutil

st.set_page_config(
    page_title="Home",
    page_icon="🎵",
)

#LOADING SPOTIFY ANIMATION
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

#SIDEBAR IMPLEMENTATION
value = st.sidebar.selectbox(label="Select your Link Type",options=["Playlist","Album"],index=None,placeholder="Select an Option")

st.title(":musical_note: SPOTIFY :tm:")
st.header("Convert your Spotify Playlist to MP3 Files")

st.write("")
st.write("")
st.write("")

# ABOUT SECTION
st.sidebar.title("About")
st.sidebar.info(
    "Welcome to the Spotify to MP3 Converter App! This app allows you to convert your Spotify playlists or albums into MP3 files. Simply provide the Spotify playlist or album link, and the app will download the corresponding songs in MP3 format."
)

# HOW TO USE SECTION
st.sidebar.title("How to Use :open_book:")
st.sidebar.markdown("1. Choose the type of link you want to convert: Playlist or Album.\n 2. Enter the Spotify link in the respective input field.\n 3. Click the 'Submit' button to start the conversion process.\n 4. Once the conversion is complete, you can listen to a sample of each song before downloading.\n 5. If you're satisfied with the sample, proceed to download the MP3 files in a zip archive.\n"
)

# ADDITIONAL TIPS SECTION (Optional)
st.sidebar.title("Tips💡")
st.sidebar.write(
    "- Make sure to have a Spotify account and provide valid Spotify links for accurate conversion."
)
st.sidebar.write("- Ensure you have a good internet connection for smooth processing.")
st.sidebar.write("- For any issues or feedback, contact the developer.")

#GETTING .ENV VARIABLES
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
API_KEY=os.getenv("YOUTUBE_API_KEY")

#GETTING ACCESS TOKEN
load_dotenv()
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
    access_token=''
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


#GET URL OF A SONG FROM YOUTUBE
def get_video_url(name):
        youtube=build('youtube','v3',developerKey=API_KEY)
        request = youtube.search().list(part='snippet',type='video',q=name,maxResults=1)
        response=request.execute()
        id = response['items'][0]['id']['videoId']  
        videoURL=f"https://www.youtube.com/watch?v={id}"  
        return videoURL

#DELETING ZIP FILES CONTENT AFTE RUSAGE
def delete_files_in_directory(directory_path):
   try:
     files = os.listdir(directory_path)
     for file in files:
       file_path = os.path.join(directory_path, file)
       if os.path.isfile(file_path):
         os.remove(file_path)
     print("All files deleted successfully.")
   except OSError:
     print("Error occurred while deleting files.")



#IF USER SELECTS ALBUM TYPE LINK
if value=='Album':
    #INPUT ALBUM LINK
    formAlbum = st.form(key='form_album')
    album_link = formAlbum.text_input(label="Enter Spotify Album Link",placeholder='Eg: https://open.spotify.com/album/78bpIziExqiI9qztvNFlQu?si=KD20tppwS-udpQqtY38-hA')
    submitAlbum = formAlbum.form_submit_button(label='Submit')

    #GET ALL ALBUM SONGS NAME FROM URI OF LINK
    def get_album_tracks(album_id,access_token):
            session = spotipy.Spotify(auth=access_token)
            track = session.album_tracks(album_id)['items']
            return track, session

    #IF USER SUBMIT LINKS
    if submitAlbum:
        uriAlbum = album_link.split("/")[-1].split("?")[0]
        #RUN AND GET NAMES OF SONGS
        tracksAlbum,session = get_album_tracks(uriAlbum,ACCESS_TOKEN)

        #INITIALIZE DOWNLOADS FOLDER
        script_directory = os.path.dirname(os.path.abspath(__file__))
        mp3album_directory = os.path.join(script_directory,"downloads_mp3_albums")
        os.makedirs(mp3album_directory, exist_ok=True)

        #PROGRESS BAR
        progress_text = "Operation in progress. Please wait."
        p=0
        bar = st.progress(p,text=progress_text)
        n = len(tracksAlbum)
        for track in tracksAlbum:
                album_name = track['name']    #GET SONG NAME
                album_artists = track['artists'][0]['name']   #GET ARTIST NAME
                keyword=f"{album_name},{album_artists}"  
                url = get_video_url(keyword)   #GET YOUTUBE VIDEO LINK
                video = YouTube(url)           
                try:
                    stream = video.streams.filter(only_audio=True).first()   
                    title = re.sub(r'[^\w\-_\. ]', '_', video.title)    #REMOVE SPECIAL CHARACTERS FROM NAME OF SONG
                    stream.download(output_path=mp3album_directory,filename=f"{title}.mp3")  #DOWNLOAD MP3 FROM LINK
                    file_path = rf"{mp3album_directory}\{title}.mp3"

                    #READING AUDIO FILES TO DISPLAY IN APP
                    audio_file = open(file_path,'rb')
                    audio_read = audio_file.read()
                    st.write(f"{album_name} by {album_artists}")
                    st.audio(audio_read,format='audio/mp3')
                    print(f"Download of {video.title} is completed successfully")
                except:
                    print("An error has occurred")
                    print(url)
                time.sleep(0.5)
                bar=bar.progress(p+1,text=progress_text)
                p+=int(100/n)
        bar=bar.progress(100,text="Completed")
        st.write("")
        st.write("")
        # st.success("Completed")     

        #MAKE ZIP FILE
        script_directory = os.path.dirname(os.path.abspath(__file__))
        zip_directory = os.path.join(script_directory,"mp3_album")
        shutil.make_archive(zip_directory,'zip',mp3album_directory)
        #ADD DOWNLOADS FOLDER CONTENTS TO ZIP FILE
        with open('mp3_album.zip', 'rb') as f:
            zip_album_file=f.read()

        #PROVIDE DOWNLOAD BUTTON TO DOWNLOAD ZIP FILE FROM WEB
            
        col1, col2, col3 = st.columns(3)
        with col2:
            flag = st.download_button(label='Download Zip', data=zip_album_file, file_name='AlbumSongs.zip',type="secondary")  # Defaults to 'application/octet-stream'
            if flag:
                st.write('Thanks for downloading!')

#IF USER SELECTS PLAYLIST TYPE LINK
elif value=='Playlist':
    form = st.form(key='form_playlist')
    playlist_link = form.text_input(label="Enter Spotify Playlist Link",placeholder='Eg: https://open.spotify.com/playlist/00i82lDzMDdiHWNjrIGAyw?si=DzmeuZbeRheqRK2DH6R-OA')
    submitPlaylist = form.form_submit_button(label='Submit')

    #GET ALL PLAYLIST SONGS NAME FROM URI OF LINK
    def get_tracks(playlist_id,access_token):
            session = spotipy.Spotify(auth=access_token)
            track = session.playlist_tracks(playlist_id)['items']
            return track, session

    #IF USER SUBMITS LINK
    if submitPlaylist:
        uri = playlist_link.split("/")[-1].split("?")[0]
        tracks,session = get_tracks(uri,ACCESS_TOKEN)

        script_directory = os.path.dirname(os.path.abspath(__file__))
        mp3playlist_directory = os.path.join(script_directory,"downloads_mp3_playlist")
        os.makedirs(mp3playlist_directory, exist_ok=True)

        progress_text = "Operation in progress. Please wait."
        p=0
        bar = st.progress(p,text=progress_text)
        n = len(tracks)
        for track in tracks:
                name = track['track']['name']     
                artists = ', '.join(artist['name'] for artist in track['track']['artists'])  
                keyword=f"{name},{artists}"  
                url = get_video_url(keyword)
                video = YouTube(url)           
                try:
                    stream = video.streams.filter(only_audio=True).first()
                    title = re.sub(r'[^\w\-_\. ]', '_', video.title)
                    stream.download(output_path=mp3playlist_directory,filename=f"{title}.mp3")
                    file_path_playlist = rf"{mp3playlist_directory}\{title}.mp3"
                    #READING AUDIO FILES TO DISPLAY IN APP
                    audio_file = open(file_path_playlist,'rb')
                    audio_read = audio_file.read()
                    st.write(f"{name} by {artists}")
                    st.audio(audio_read,format='audio/mp3')
                    print(f"Download of {video.title} is completed successfully")
                except:
                    print("An error has occurred")
                    print(url)
                time.sleep(0.5)
                bar=bar.progress(p+1,text=progress_text)
                p+=int(100/n)
        bar=bar.progress(100,text="Completed")
        st.write("")
        st.write("")
        # st.success("Completed")
        script_directory = os.path.dirname(os.path.abspath(__file__))
        zip_directory = os.path.join(script_directory,"mp3_playlist")

        shutil.make_archive(zip_directory,'zip',mp3playlist_directory)

        with open('mp3_playlist.zip', 'rb') as f:
            zip_file=f.read()

        
        col1, col2, col3 = st.columns([2.5,2,1.5])
        with col2:
            flag = st.download_button(label='Download Zip', data=zip_file, file_name='PlaylistSongs.zip',type="secondary")  # Defaults to 'application/octet-stream'
            if flag:
                st.write('Thanks for downloading!')
        
        

else:
    st.header(':arrow_left: Please Select the type of Link')
