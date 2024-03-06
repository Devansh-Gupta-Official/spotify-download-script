from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
import requests
import csv
import pandas as pd

load_dotenv()
#loading api key in this variable from .env
API_KEY=os.getenv("YOUTUBE_API_KEY")
#create a resource to access YouTube Data API
def get_video_url(name):
    youtube=build('youtube','v3',developerKey=API_KEY)
    request = youtube.search().list(part='snippet',type='video',q=name,maxResults=1)
    response=request.execute()
    id = response['items'][0]['id']['videoId']   #extracts videoid from repsonse
    videoURL=f"https://www.youtube.com/watch?v={id}"   #concatenates with a string to get link
    return videoURL
# query = 'The Nights,Avicii'
# results = get_video_id(query)
# print(results)
#extracting song name, artist name from csv
with open("track.csv", "r", newline='') as file:
    reader = csv.reader(file)
    # next(reader)   #skips the header row
    url_list=[]
    
    for read in reader:
        keyword=f"{read[0]},{read[1]}"     #song name, artist name for each row
        url = get_video_url(keyword)
        url_list.append(url)
    url_list[0] =f"URL"
    
dataframe = pd.DataFrame(url_list)
dataframe.to_csv('url.csv',index=False,header=False)