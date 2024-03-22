import pyrebase

firebaseConfig = {
  'apiKey': "AIzaSyBse46d2yfIDwAg5laKRULC4Ko6IouMLRQ",
  'authDomain': "spotify-downloader-4cd67.firebaseapp.com",
  'projectId': "spotify-downloader-4cd67",
  'databaseURL':'https://console.firebase.google.com/u/0/project/spotify-downloader-4cd67/database/spotify-downloader-4cd67-default-rtdb/data/~2F',
  'storageBucket': "spotify-downloader-4cd67.appspot.com",
  'messagingSenderId': "533782551079",
  'appId': "1:533782551079:web:043931fb5a4b7875c94c02",
  'measurementId': "G-N0JFE9DR4W"
};

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

db=firebase.database()
storage = firebase.storage()

firebase_upload = storage.put('')

