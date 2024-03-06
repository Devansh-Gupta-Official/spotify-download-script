#LOGIC TO SELF CLASSIFY WHAT TYPE OF LINK THE USER HAS PROVIDED

playlist_link = 'https://open.spotify.com/album/78bpIziExqiI9qztvNFlQu?si=KD20tppwS-udpQqtY38-hA'

def identify_link(link):
    if "spotify" in link and "playlist" in link:
        return "spotify_playlist"
    elif "spotify" in link and "album" in link:
        return "spotify_album"
    else:
        return "This is not a valid link"