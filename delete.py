import os
import shutil
script_directory = os.path.dirname(os.path.abspath(__file__))
zip_to_delete =  os.path.join(script_directory,"mp3_playlist.zip")
directory_to_delete =  os.path.join(script_directory,"downloads")

try:
    os.remove(zip_to_delete)
except:
    print(f"The specified file does not exist.")

shutil.rmtree(directory_to_delete)