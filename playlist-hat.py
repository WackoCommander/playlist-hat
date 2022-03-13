
# Python script to organise music library into playlists based on bpm using spotify api
# suports FLAC files

import os
from pathlib import Path
from numpy import median, diff
import sys
import requests
from mutagen.flac import FLAC

# SPOTIFY API DETAILS
CLIENT_ID = CLIENT_ID
CLIENT_SECRET = CLIENT_SECRET
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
slow_jamz = open("Slow Jamz.m3u", "w")
warm_up = open("Warm Up.m3u", "w")
steady_state = open("Steady State.m3u", "w")
build = open("Build.m3u", "w")
plus_ultra = open("Plus Ultra.m3u", "w")
peace = open("Peace.m3u", "w")
touch_the_sky = open("Touch the Sky.m3u", "w")
computer = open("Computer.m3u", "w")
lost = open("lost.m3u", "w")
pathlist = Path(os.getcwd()).glob('**/*.flac')
length_to_cut = len(os.getcwd())

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
            if (bpm > 59.9 and bpm < 90.1):
                slow_jamz.write(path_in_str_trimmed + "\n")
                print(str(bpm) + "Added to slow jamz")
            if (bpm > 99.9 and bpm < 140.1):
                print(str(bpm) + "Added to warm_up")
                warm_up.write(path_in_str_trimmed + "\n")
            if (bpm > 119.9 and bpm < 140.1):
                steady_state.write(path_in_str_trimmed + "\n")
                print(str(bpm) + "Added to steady_state")
            if (bpm > 129.9 and bpm < 150.1):
                build.write(path_in_str_trimmed + "\n")
                print(str(bpm) + "Added to build")
            if (bpm > 140):
                plus_ultra.write(path_in_str_trimmed + "\n")
                print(str(bpm) + "Added to plus_ultra")
            if (bpm < 59.9):
                lost.write(path_in_str_trimmed + "\n")
                print(str(bpm) + "added to lost")



    #if (get_processed(path)):
    #    print("Already processed, going to next song")
    #    continue
    #else:
    #    print("Processing now...")
        
        

slow_jamz.close()
warm_up.close()
steady_state.close()
build.close()
plus_ultra.close()
peace.close()
touch_the_sky.close()
computer.close()
lost.close()
