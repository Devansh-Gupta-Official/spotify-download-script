def run():
    from pytube import YouTube
    import os
    import csv

    script_directory = os.path.dirname(os.path.abspath(__file__))
    mp3_directory = os.path.join(script_directory,"downloads_mp3")
    os.makedirs(mp3_directory, exist_ok=True)

    song_number = 1

    with open('url.csv','r',newline='') as file:
        reader = csv.reader(file)
        next(reader)     #row
        for row in reader:
            url = row[0]    #saving url in a variable
            video = YouTube(url)           #gets the video on the youtube url
            try:
                stream = video.streams.filter(only_audio=True).first()
                stream.download(output_path=mp3_directory,filename=f"{video.title}.mp3")
                print(f"Download of Song {song_number} is completed successfully")
            except:
                print("An error has occurred")
                print(url)
            song_number+=1

