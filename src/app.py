import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
#import seaborn as sns (having problems importing seaborn: E0401:import-error, so I'll use matplotlib)
import matplotlib.pyplot as plt

# load the .env file variables
load_dotenv()

client_credentials_manager = SpotifyClientCredentials(
    client_id = os.environ.get("CLIENT_ID"),
    client_secret = os.environ.get("CLIENT_SECRET")
    )

sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

result = sp.artist_top_tracks('spotify:artist:3TOqt5oJwL9BE2NG9MEwDa')

if result:

    data_list = []
    for track in result['tracks'][:10]:
        print('track    : ' + track['name'])
        minutes = track['duration_ms'] // 60000
        seconds = track['duration_ms'] % 60000 // 1000
        print(f'audio    :  {minutes}:{seconds:02d}') 
        print('popularity: ' + str(track['popularity']))
        print()
        
        data_list.append({
            'Name' : track['name'],
            'Duration_ms' : (track['duration_ms']/(1000*60)%60),
            'Popularity' : track['popularity']
        })

df = pd.DataFrame(data_list, columns = ["Name", "Duration_ms", "Popularity"])

df = df.sort_values("Popularity", ascending = False)
print(df.head(3))

plt.figure(figsize = (10, 6))
plt.scatter(df['Popularity'], df['Duration_ms'], color = 'blue')

plt.xlabel("Popularity")
plt.ylabel('Duration_ms')

plt.grid(True, linestyle = '--')

plt.show()

print("As shown in the scatter plot, there's no relation between the duration of the song and the popularity of it.")