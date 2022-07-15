
# Python script to organise music library into playlists based on bpm using spotify api
# suports FLAC files

import os
from pathlib import Path
from numpy import median, diff
import sys
import requests
from mutagen.flac import FLAC
import librosa
import soundfile
import vamp

# Spotify API Details

# Playlist Categories

car_tunes = open("Car Tunes.m3u", "w") # 60 - 80 bpm Note: Reduces the chance of accident
high_intensity = open("High Intensity.m3u", "w") # > 140 bpm
jogging = open("Jogging.m3u", "w") # 120 - 140 bpm
pathlist = Path(os.getcwd()).glob('**/*.flac')
length_to_cut = len(os.getcwd())

def main():
    for path in pathlist:
        path_str = str(path)
        path_str_t = path_str[len(os.getcwd()) + 1:]
        print("Processing " + path_str_t)
        data, rate = soundfile.read(path)
        data, fake_rate = librosa.load(path)
        bpm = vamp.collect(data, rate, "vamp-example-plugins:fixedtempo")
        bpm = bpm['list']
        bpm = bpm[0]['values'][0]
        print(bpm)
        if (bpm > 140):
            high_intensity.write(path_str_t + "\n")
            print("high intensity")
        if (bpm > 60 and bpm < 80):
            car_tunes.write(path_str_t + "\n")
            print("car tunes")
        if (bpm > 120 and bpm < 140):
            jogging.write(path_str_t + "\n")
            print("jogging")

if __name__ == '__main__':
    main()
    high_intensity.close()
    car_tunes.close()
    jogging.close()


