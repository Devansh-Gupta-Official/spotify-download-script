# Spotify to MP3 Converter

Convert your Spotify playlists or albums into MP3 files easily with this Streamlit app.

## Features
- Convert Spotify playlists or albums into MP3 files.
- Listen to samples of each song before downloading.
- Download MP3 files in a zip archive.
- Simple and intuitive user interface.
- Background image customization.

## Technologies Used
- Python
- Streamlit
- Pytube
- Spotipy
- Requests
- Dotenv
- Google API Client
- Pandas
- Simplejson
- Streamlit-feedback
- Trubrics

## Getting Started
To get a local copy up and running follow these simple steps:

1. Clone the repository:

   ```
   git clone https://github.com/Devansh-Gupta-Official/spotify-download-script.git
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
Create a .env file in the root directory of the project and add the following variables:
```
ACCESS_TOKEN=<your_access_token>
YOUTUBE_API_KEY=<your_youtube_api_key>
```

4. Run the app:

   ```
   streamlit run app.py
   ```

5. Access the app in your web browser at http://localhost:8501.

## Usage
- Choose the type of link you want to convert: Playlist or Album.
- Enter the Spotify link in the respective input field.
- Click the 'Submit' button to start the conversion process.
- Listen to a sample of each song before downloading.
- If satisfied, proceed to download the MP3 files in a zip archive.

## Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

- Fork the project.
- Create your feature branch (git checkout -b feature/AmazingFeature).
- Commit your changes (git commit -m 'Add some AmazingFeature').
- Push to the branch (git push origin feature/AmazingFeature).
- Open a pull request.

