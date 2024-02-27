import streamlit as st

import auth
import spotify
import youtube
import downloading_mp3
import downloading_mp4


playlist_link = st.text_input("Enter your playlist link")
subButton = st.button("Submit")
if subButton:
    spotify.getLink(playlist_link)
    auth.run()
    spotify.run()
    youtube.run()
    # downloading_mp4.run()
    downloading_mp3.run()