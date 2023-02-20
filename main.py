from bs4 import BeautifulSoup
import requests
import spotipy



CLIENT_ID = "SPORTIFY CLIENT ID FROM SPORIFY DEVELOPER PORTAL"
CLIENT_SECRET = "SPORTIFY SERCRET ID FROM SPORIFY DEVELOPER PORTAL"


oauth_object = spotipy.SpotifyOAuth(client_id=CLIENT_ID,
                                    client_secret=CLIENT_SECRET,
                                    redirect_uri="http://example.com",
                                    show_dialog=True,
                                    cache_path="token.txt",
                                    scope="playlist-modify-private"
                                    )

sp = spotipy.Spotify(auth_manager=oauth_object)

user_id = sp.current_user()["id"]

# user input for top 100 year
year = input("Which year would you like to create a top 100 ? \nYYYY-MM-DD\n")
# gets url for that year
URL = f"https://www.billboard.com/charts/hot-100/{year}"

# gets data
response = requests.get(URL)
top_html = response.text

user_id = sp.current_user()["id"]
# parses the site.
soup = BeautifulSoup(top_html, "html.parser")
# to find the song name with css/html selector using beautifulsoup
songs_list = soup.select("li ul li h3")

# adds song to list and removes all newlines since the H3 element is full of them
song_names = [song.get_text(strip=True) for song in songs_list]

# creates playlist with the enterd date in the year
my_playlist = sp.user_playlist_create(user=f"{user_id}", name=f"{year}: Top Tracks", public=False,
                                      description="OPTIONAL")
# song uri/tracks list
song_uri = []
# loops and gets all URIs, if it dosent find song. pass
for i in song_names:
    try:
        track = sp.search(q=' track:' + i, type='track')
        track_uri = (track["tracks"]["items"][0]["uri"])
    except IndexError:
        pass
    finally:
        song_uri.append(track_uri)



 # creates playlist from song_uri list. 
sp.playlist_add_items(playlist_id=my_playlist["id"],items=song_uri)



