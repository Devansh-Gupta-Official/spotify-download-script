#LOGIC TO SELF CLASSIFY WHAT TYPE OF LINK THE USER HAS PROVIDED

playlist_link = 'https://open.spotify.com/album/78bpIziExqiI9qztvNFlQu?si=KD20tppwS-udpQqtY38-hA'

def identify_link(link):
    if "spotify" in link and "playlist" in link:
        return "This is a Spotify playlist link."
    elif "spotify" in link and "album" in link:
        return "This is a Spotify album link."
    elif "apple" in link and "playlist" in link:
        return "This is a Apple Music playlist link."
    elif "apple" in link and "album" in link:
        return "This is a Apple Music album link."
    else:
        return "This is not a valid link"


result = identify_link(playlist_link)
print(result)