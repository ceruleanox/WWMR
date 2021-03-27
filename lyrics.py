import configparser
import requests
import re 
from spellCheck import bannedWords
from bs4 import BeautifulSoup

def getAccessToken():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['Client_Access_Token']['token']

token = getAccessToken()

def searchMusicArtist(name):    
    api_url = "https://api.genius.com/search?q={}".format(name)
    headers = {"authorization": token}
    r = requests.get(api_url, headers=headers)
    return r.json()

def getArtistID(name):
    r = searchMusicArtist(name)
    id = r["response"]["hits"][0]["result"]["primary_artist"]["id"]
    return id

def getTopTenSongs(name):
    id = getArtistID(name)
    api_url = "https://api.genius.com/artists/{}/songs".format(id)
    headers = {"authorization": token}
    params = {
        "sort": "popularity",
        "per_page": 3
    }
    r = requests.get(api_url, headers=headers, params=params)
    return r.json()

def getLyricsArray(name):
    r = getTopTenSongs(name)
    songs = r["response"]["songs"]
    lyrics_array = []
    for song in songs:
        lyrics_array.append(song["url"])
    return lyrics_array

def scrapeLyricText(name):
    links = getLyricsArray(name)
    song_lyrics = []
    for link in links:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')

        lyrics_div = soup.find(class_="lyrics")
        anchor_tags = lyrics_div.find_all('a')
        current_lyrics = []
        for anchor in anchor_tags:
            if len(anchor.text) > 0 and anchor.text[0] != "[":
                # loop through key value pairs to replace banned words with something less explicit 
                for key, value in bannedWords.items():
                    text = anchor.text.replace(key.lower(),value)
                    print(key,value)
   
                # text = anchor.text.replace("fuck"," f*ck ")
                #text = anchor.text.replace("shit"," sh*t ")
                current_lyrics.append(text)
        song_lyrics.append(current_lyrics)
    return song_lyrics

# print(scrapeLyricText("fall out boy"))
# print(getLyricsArray("Adam Levine"))
# print(getTopTenSongs("bts"))
# print(getArtistID("adele"))
# print(searchMusicArtist("drake"))