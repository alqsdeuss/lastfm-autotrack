import pylast
import time
import requests
import sys

class culori:
    gren = "\033[92m"
    red = "\033[91m"
    galben = "\033[93m"
    blue = "\033[94m"
    reset = "\033[0m"

lastfmapikey = 'ur apikey'
lastfmapisecret = 'ur secret'
lastfmuser = 'ur last.fm username'
lastfmpassword = pylast.md5('ur last.fm password')

network = pylast.LastFMNetwork(api_key=lastfmapikey, api_secret=lastfmapisecret,
                               username=lastfmuser, password_hash=lastfmpassword)

def scrobble_track(artist, track, album, timestamp):
    try:
        network.scrobble(artist=artist, title=track, album=album, timestamp=timestamp)
        print(f"{culori.gren}> by: {artist} - {track}{culori.reset}")
    except pylast.WSError as e:
        print(f"{culori.red}> error: {e}{culori.reset}")

def get_popular_tracks():
    url = 'https://api.deezer.com/chart'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        tracks = data['tracks']['data']
        popular_tracks = []
        for track in tracks:
            artist_name = track['artist']['name']
            track_title = track['title']
            album_title = track['album']['title']
            popular_tracks.append({
                'artist': artist_name,
                'track': track_title,
                'album': album_title
            })
        return popular_tracks
    else:
        print(f"{culori.galben}> deezer 404{culori.reset}")
        return []

sec = 2
tracks = 0

try:
    while True:
        mata = get_popular_tracks()
        if not mata:
            print(f"{culori.galben}> try again{culori.reset}")
            time.sleep(1)
            continue

        for mata in mata:
            artist = mata["artist"]
            track = mata["track"]
            album = mata["album"]
            current_time = int(time.time())
            
            scrobble_track(artist, track, album, current_time)
            tracks += 1
            time.sleep(sec)

except (KeyboardInterrupt, SystemExit):
    print(f"{culori.blue}> oke u have now: {tracks} tracks{culori.reset}")
    sys.exit(0)
