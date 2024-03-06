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
# Read the content of the .env file
with open('.env', 'r') as f:
    lines = f.readlines()
# Update the ACCESS_TOKEN line or add it if not present
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
# Write the updated content back to the .env file
with open('.env', 'w') as f:
    f.writelines(updated_lines)