import yt_dlp
import string
import os
from mutagen.easyid3 import EasyID3
from mutagen import id3

class Album():
    def __init__(self, artist, title, year, songs):
        self.artist = artist
        self.title = title
        self.folder = to_filename(title)
        self.year = year
        self.songs = songs

    def __str__(self):
        return f"{self.artist} - {self.title}, ({self.year})"

class Song():
    def __init__(self, title, url, index):
        self.title = title
        self.filename = to_filename(title)
        self.url = url
        self.index = index

    def __str__(self):
        return f"{self.index}. {self.title}: {self.url}"

def to_filename(title):
    output = ""
    for char in title.lower().replace(" ", "-"):
        if char in string.ascii_letters + string.digits + "-":
            output += char
            continue
        if char in "åä":
            output += "a"
            continue
        if char == "ö":
            ourpur += "o"
    return output

def download_audio(url, output_path):
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def gather_album_info():
    artist_title = input("Title of artist: ")
    album_title = input("Title of album: ")
    album_year = input("Release year: ")
    songs = []
    index = 1
    print("Enter song names and urls:")
    while 1:
        song = Song(input(f"{index:>4}│ Name: "), input("    └ URL: "), index)
        if song.title == "":
            break
        songs.append(song)
        index += 1
    return Album(artist_title, album_title, album_year, songs)

if __name__ == "__main__":
    album = gather_album_info()

    os.mkdir(album.folder) 
    for song in album.songs:
        path = os.path.join(album.folder, song.filename)
        download_audio(song.url, path)
        path += ".mp3"
        song_file = EasyID3(path)
        song_file["artist"] = album.artist
        song_file["album"] = album.title
        song_file["date"] = album.year
        song_file["tracknumber"] = f"{song.index:02}"
        song_file["title"] = song.title
        song_file.save()

    print(f"{album} downloaded.")
