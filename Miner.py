import os
import sys
import json 
import spotipy
import webbrowser
import spotipy.util as util
import csv
import pymongo
from json.decoder import JSONDecodeError

#Constantes
token = "BQCq7atPuPvBEeOsE_KspEtU88aObsC__PRVvI_E1oydwp6myds9Npw4kdFlJ9sQSvUeJi3bQZzxZmdZ-ofttz1UyEjPPoLzu0BCO1OzY9gIrqo4bK02NypoBJi0V7UijFscqgDX-c9BowMaR3mslO_wTdD6nEtBD75zWa1ARZ1nJQyVZniWFhExMGsd_1jBaMVTmmZh5O-AbxvjQ68"
dbPath = 'mongodb://localhost:27017/' #Direccion de la conexion
dbName = 'canciones' # Nombre de la BD
colName = 'lista_canciones' #Nombre de la coleccion
songFileName = 'Top_Songs_1940_2018.csv'
#------------------------------------------------------------------
def startSpotify(token):
    return spotipy.Spotify(auth = token)

def getSongInfo(session,name,year):
    song = session.search(name,limit = 1, offset = 0, type = 'track') # Make API Request to Search endpoint
    resp = json.dumps(song, sort_keys = True, indent = 4) # Parses request as json
    song = json.loads(resp) # Loads JSON

    song_id = song['tracks']['items'][0]['id']
    song_name = song['tracks']['items'][0]['name']
    song_artist = song['tracks']['items'][0]['album']['artists'][0]['name']
    #song_release_date = song['tracks']['items'][0]['album']['release_date']

    song_features = session.audio_features(song_id) # Make request for song features
    feat_json = json.dumps(song_features, sort_keys = True, indent = 4)
    features = json.loads(feat_json)
    song_valence = features[0]['valence']
    song_energy =   features[0]['energy']

    return { "id": song_id , "name": song_name , "artist": song_artist , "year": year , "valence": song_valence , "energy": song_energy}
  

Spotify = startSpotify(token)

myclient = pymongo.MongoClient(dbPath)
mydb = myclient[dbName]
mycol = mydb[colName]
x = 0
with open(songFileName) as Songs:
    reader = csv.reader(Songs)
    for i in reader:
        try:
            songInfo = getSongInfo(Spotify, i[1] + " - " + i[2] , i[0])
            print(songInfo)
            mycol.insert_one(songInfo)
            print("Insercion exitosa")
        except:
            x+=1
            print("Insercion no exitosa")
print("Numero de inserciones no exitosas")
        
Songs.close()





