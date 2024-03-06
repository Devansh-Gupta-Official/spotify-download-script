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

import classify
import authorization
import link
import delete
import tracks
import zipp

st.set_page_config(
    page_title="Home",
    page_icon="🎵",
)
# st.markdown(""" <style> .font {
# font-size:50px ; font-family: 'Sans-serif'; color: #F2F2F2;} 
# </style> """, unsafe_allow_html=True)
# st.markdown('<h1 class="font">🎵 SPOTIFY ™️</h1>',unsafe_allow_html=True)
st.title(":musical_note: SPOTIFY")
st.header("Convert your Spotify Playlist to MP3 Files")

st.write("")
st.write("")
st.write("")

#TAKING IN USER INPUT
form = st.form(key='form')
playlist_link = form.text_input(label="Enter Link",placeholder='Eg: https://open.spotify.com/album/78bpIziExqiI9qztvNFlQu?si=KD20tppwS-udpQqtY38-hA')
submit = form.form_submit_button(label='Submit')

#CHECKING IF LINK ENTERED IS SPOTIFY OR APPLE MUSIC
link_type = classify.identify_link(playlist_link)
    
#LOADING ANIMATIONS BASED ON RESULTS
if link_type=="spotify_playlist" or link_type=="spotify_album":
    
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
    
    #GETTING .ENV VARIABLES
    authorization.get_access_token()

    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    API_KEY=os.getenv("YOUTUBE_API_KEY")

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
    if link_type=='spotify_album':

        #CLEARING DOWNLOADS FOLDER AND ZIP FILE
        script_directory = os.path.dirname(os.path.abspath(__file__))
        zip_to_delete =  os.path.join(script_directory,"mp3.zip")
        directory_to_delete =  os.path.join(script_directory,"downloads")

        delete.delete_files_in_directory(directory_to_delete)
        delete.delete_files_in_directory(zip_to_delete)

        #IF USER SUBMIT LINKS
        if submit:
            uriAlbum = playlist_link.split("/")[-1].split("?")[0]
            #RUN AND GET NAMES OF SONGS
            tracksAlbum,session = tracks.get_album_tracks(uriAlbum,ACCESS_TOKEN)

            #INITIALIZE DOWNLOADS FOLDER
            script_directory = os.path.dirname(os.path.abspath(__file__))
            mp3_directory = os.path.join(script_directory,"downloads")
            os.makedirs(mp3_directory, exist_ok=True)

            #PROGRESS BAR
            progress_text = "Operation in progress. Please wait."
            p=0
            bar = st.progress(p,text=progress_text)
            n = len(tracksAlbum)
            for track in tracksAlbum:
                    album_name = track['name']    #GET SONG NAME
                    album_artists = track['artists'][0]['name']   #GET ARTIST NAME
                    keyword=f"{album_name},{album_artists}"  
                    url = link.get_video_url(keyword)   #GET YOUTUBE VIDEO LINK
                    video = YouTube(url)           
                    try:
                        stream = video.streams.filter(only_audio=True).first()   
                        title = re.sub(r'[^\w\-_\. ]', '_', video.title)    #REMOVE SPECIAL CHARACTERS FROM NAME OF SONG
                        stream.download(output_path=mp3_directory,filename=f"{title}.mp3")  #DOWNLOAD MP3 FROM LINK
                        file_path = rf"{mp3_directory}\{title}.mp3"

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
            zip_directory = os.path.join(script_directory,"mp3")
            shutil.make_archive(zip_directory,'zip',mp3_directory)
            #ADD DOWNLOADS FOLDER CONTENTS TO ZIP FILE
            with open('mp3.zip', 'rb') as f:
                zip_album_file=f.read()

            #PROVIDE DOWNLOAD BUTTON TO DOWNLOAD ZIP FILE FROM WEB
            col1, col2, col3 = st.columns(3)
            with col2:
                flag = st.download_button(label='Download Zip', data=zip_album_file, file_name='songs.zip',type="secondary")  # Defaults to 'application/octet-stream'
                if flag:
                    st.write('Thanks for downloading!')

    #IF USER SELECTS PLAYLIST TYPE LINK
    if link_type=='spotify_playlist':
        #CLEARING DOWNLOADS FOLDER AND ZIP FILE
        script_directory = os.path.dirname(os.path.abspath(__file__))
        zip_to_delete =  os.path.join(script_directory,"mp3.zip")
        directory_to_delete =  os.path.join(script_directory,"downloads")

        try:
            os.remove(zip_to_delete)
        except:
            print(f"The specified file does not exist.")

        try:
            shutil.rmtree(directory_to_delete)
        except:
            print(f"The specified file does not exist.")

        #GET ALL PLAYLIST SONGS NAME FROM URI OF LINK
        def get_tracks(playlist_id,access_token):
                session = spotipy.Spotify(auth=access_token)
                track = session.playlist_tracks(playlist_id)['items']
                return track, session

        #IF USER SUBMITS LINK
        if submit:
            uri = playlist_link.split("/")[-1].split("?")[0]
            tracks,session = tracks.get_tracks(uri,ACCESS_TOKEN)

            script_directory = os.path.dirname(os.path.abspath(__file__))
            mp3_directory = os.path.join(script_directory,"downloads")
            os.makedirs(mp3_directory, exist_ok=True)

            progress_text = "Operation in progress. Please wait."
            p=0
            bar = st.progress(p,text=progress_text)
            n = len(tracks)
            for track in tracks:
                    name = track['track']['name']     
                    artists = ', '.join(artist['name'] for artist in track['track']['artists'])  
                    keyword=f"{name},{artists}"  
                    url = link.get_video_url(keyword)
                    video = YouTube(url)           
                    try:
                        stream = video.streams.filter(only_audio=True).first()
                        title = re.sub(r'[^\w\-_\. ]', '_', video.title)
                        stream.download(output_path=mp3_directory,filename=f"{title}.mp3")
                        file_path_playlist = rf"{mp3_directory}\{title}.mp3"
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
            zip_directory = os.path.join(script_directory,"mp3")
            shutil.make_archive(zip_directory,'zip',mp3_directory)
            with open('mp3.zip', 'rb') as f:
                zip_file=f.read()

            
            col1, col2, col3 = st.columns([2.5,2,1.5])
            with col2:
                flag = st.download_button(label='Download Zip', data=zip_file, file_name='songs.zip',type="secondary")  # Defaults to 'application/octet-stream'
                if flag:
                    st.write('Thanks for downloading!')

else:
    st.warning("Enter a Valid Link")



#SIDEBAR IMPLEMENTATION
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


