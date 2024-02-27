import csv
import os
from pytube import YouTube

#creating a folder where these videos should download
script_directory = os.path.dirname(os.path.abspath(__file__))
download_directory = os.path.join(script_directory,"downloads")
os.makedirs(download_directory, exist_ok=True)

video_number = 0

# opening track.csv
with open('url.csv','r',newline='') as file:
    reader = csv.reader(file)
    next(reader)     #row
    for row in reader:
        url = row[0]    #saving url in a variable
        video = YouTube(url)           #gets the video on the youtube url
        try:
            video.streams.first().download(output_path=download_directory)
            print(f"Download of Video {video_number} is completed successfully")
        except:
            print("An error has occurred")
            print(url)
        video_number+=1
        
# video = YouTube('https://www.youtube.com/watch?v=v6Gxin8VKZc')
# video.streams.first().download()
