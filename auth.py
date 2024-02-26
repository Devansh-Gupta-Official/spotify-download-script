import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()   #Load environment variables from .env file

# Access client ID, client secret from environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

client_credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"    #f string
encoded_client_creds = base64.b64encode(client_credentials.encode())
#encoded_client_creds: Holds the result of the Base64 encoding, which is a bytes object containing the Base64-encoded representation of client_credentials.

#GETTING THE ACCESS TOKEN
auth_url = 'https://accounts.spotify.com/api/token'
#That's the authorization URL, and then we can just put our credentials in a dictionary to send with the request.

#If the user accepted your request, then your app is ready to exchange the authorization code for an access token. It can do this by sending a POST request to the /api/token endpoint.

headers={
    #Base 64 encoded string that contains the client ID and client secret key. The field must have the format: Authorization: Basic <base64 encoded client_id:client_secret>
    'Authorization':f"Basic {encoded_client_creds.decode()}"
}

form={
    #This field must contain the value "authorization_code".
    'grant_type':'client_credentials'
}

response = requests.post(auth_url,data=form,headers=headers)

#The access token is another alphanumeric string that also has some other symbols in it.
if response.status_code==200:
    access_token=response.json()['access_token']
    print("sucessful")
else:
    print("error")
    exit()

## Save the access token to the environment variable for future use
os.environ['ACCESS_TOKEN'] = access_token

with open('.env', 'a') as f:
            f.write(f'\nACCESS_TOKEN="{access_token}"')