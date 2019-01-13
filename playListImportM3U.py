#Josh Van Buren
#Test Script for the gmusicapi

#Imports
from gmusicapi import Mobileclient
import tkFileDialog
import tkSimpleDialog
import os.path
import eyed3

#Get the file name
path = tkFileDialog.askopenfilename()

#Create the array for the file names, artists, tracks
paths = []
artists = []
tracks = []

#Loop through the file
for line in file(path):
	#If the line is not a comment
	if not line.startswith('#'):
		#Strip the line
		line = line.strip()
		
		#Add the path to the list
		paths.append(line)

#Get the encoding of the file
raw = file(path).read(min(32, os.path.getsize(path)))

#Check to see if it's utf 8
if(raw.startswith(codecs.BOM_UTF8)):
	#Fix the first path
	paths[0] = (paths[0])[3:]

#Loop through the paths
for filePath in paths:
	#If the file exists, get the info
	if os.path.isfile(filePath):
		print filePath
		#Open the file
		mp3File = eyed3.load(filePath)
		
		#Get the info
		artists.append(mp3File.tag.artist)
		tracks.append(mp3File.tag.title)
		

#Enter the playlist name
pListName = tkSimpleDialog.askstring('Playlist Name', 'What is the name of the playlist?')

#Create the mobile client
api = Mobileclient()

#Login
api.login('Emailhere', 'pwdhere', Mobileclient.FROM_MAC_ADDRESS)
# => True

#Get all of the songs in the library
library = api.get_all_songs()

#Create the list
pListTracks = []

#Create the playlist
playlist_id = api.create_playlist(pListName)

#Loop through the playlist files
for i in range(len(tracks)):
	#If the artist is in the list
	for iTrack in library:
		#Check the track
		if (iTrack['title'] == tracks[i]) and (iTrack['artist'] == artists[i]):
			#Add the track to the list
			pListTracks.append(iTrack['id'])
			#print iTrack['id']


#Add the songs to the playlist
api.add_songs_to_playlist(playlist_id, pListTracks)