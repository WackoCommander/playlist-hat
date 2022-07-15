
# Python script to organise music library into playlists based on bpm using spotify api
# suports FLAC files

import os
from pathlib import Path
from numpy import median, diff
import sys
import requests
from mutagen.flac import FLAC

# Spotify API Details
CLIENT_ID = os.environ.get('SPOTIFY_CLIENT')
CLIENT_SECRET = os.environ.get('SPOTIFY_SECRET')
BASE_URL = "https://api.spotify.com/v1/"
API_KEY = ""
AUTH_URL = "https://accounts.spotify.com/api/token"
auth_response = requests.post (AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})
auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']
headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}

# Playlist Categories
lost = open("lost.m3u", "w")

car_tunes = open("Car Tunes.m3u", "w") # 60 - 80 bpm Note: Reduces the chance of accident
high_intensity = open("High Intensity.m3u", "w") # > 140 bpm
jogging = open("Jogging.m3u", "w") # 120 - 140 bpm

pathlist = Path(os.getcwd()).glob('**/*.flac')
length_to_cut = len(os.getcwd())

def main():
    for path in pathlist:
        path_in_str = str(path)
        path_in_str_trimmed = path_in_str[length_to_cut+1:]
        title = get_title(path_in_str)
        artist = get_artist(path_in_str)
        details = requests.get(BASE_URL + "search?q=" + title + "&type=track&limit=30", headers=headers)
        details = details.json()
        confirm = 0
        count = -1
        lost_cause = 0
        print("Processing " + title + " by " + artist)
        try:
            if (details["tracks"]["items"][0]["artists"][0]["name"] == artist):
                count = count + 1
            else:
                while (confirm != 'y'):
                    count = count + 1
                    #confirm = input("Confirm correct track " + details["tracks"]["items"][count]["name"] + " by " + str(details["tracks"]["items"][count]["artists"][0]["name"])+ "\n")
                    try:
                       if (details["tracks"]["items"][count]["artists"][0]["name"] == artist):
                            confirm = 'y'
                    except:
                        lost_cause = 1
                        lost.write(path_in_str_trimmed + "\n")
                        print("Added to lost")
                        confirm = 'y'
        except:
            lost_cause = 1
            lost.write(path_in_str_trimmed + "\n")
            print("Added to lost")

        if lost_cause == 0:
            try:
                artist_details = requests.get(BASE_URL + "artists/" + details["tracks"]["items"][count]["artists"][0]["id"],headers=headers)
                artists_details = artist_details.json()
                track_url = details["tracks"]["items"][count]["id"]
                song_details = requests.get(BASE_URL + "audio-features/" + track_url, headers=headers)
                song_details = song_details.json()
                bpm = song_details["tempo"]
                processed = 0
            except:
                lost_cause = 1
                lost.write(path_in_str_trimmed + "\n")
                print("Added to lost")
            if (lost_cause == 0):
                if (bpm > 59.9 and bpm < 80.1):
                    car_tunes.write(path_in_str_trimmed + "\n")
                if (bpm > 140):
                    high_intensity.write(path_in_str_trimmed + "\n")
                if (bpm > 119.9 and bpm < 140):
                    jogging.write(path_in_str_trimmed + "\n")

def get_title(path):
    audio = FLAC(path)
    return str(audio["TITLE"])[2:][:-2]

def get_artist(path):
    audio = FLAC(path)
    return str(audio["ARTIST"])[2:][:-2]

def get_processed(path):
    audio = FLAC(path)
    return int(audio["PROCESSED"])

def set_processed(path):
    audio = FLAC(path)

if __name__ == '__main__':
    main()
    high_intensity.close()
    car_tunes.close()
    lost.close()
    jogging.close()


