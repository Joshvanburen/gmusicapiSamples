#Josh Van Buren
#Compares the local playlist to the one in google music

#Imports
from gmusicapi import Mobileclient
import tkinter.filedialog
import tkinter.simpledialog
import os.path
import eyed3
import codecs

#Suppress mp3 tag warnings
eyed3.log.setLevel("ERROR")

#Get the file name
path = tkinter.filedialog.askopenfilename()

#Create the mobile client
api = Mobileclient(False,True,True)

#Login
#api.perform_oauth('C:\\Users\\Joshv\\Josh\\Programming\\Python\\googleMusic\\gMusicDeviceID.txt')
api.oauth_login('b83fce595c6fd82bcfcfdd8e2e542d79f3c176bb0974c4bb34da2df10d95cec1')

#Retrieve all playlists
playlists = api.get_all_playlists(False, False)

#Retrive the contents of all playlists
playlistContents = api.get_all_user_playlist_contents()

#Get the entire song library
library = api.get_all_songs(False, False)

#Create the array for the file names, artists, tracks in the local playlist
paths = []
lArtists = []
lTracks = []

#Create arrays for the artists and tracks in the gmusic playlist
gArtists = []
gTracks = []

#Get the playlist file name
playlistFileName = os.path.basename(path)
playlistName = os.path.splitext(playlistFileName)[0]

#Print the playlist file name
print("-----------------------------------------")
print(playlistName)
print("-----------------------------------------")

#Loop through the file
for line in open(path):
	#If the line is not a comment
	if not line.startswith('#'):
		#Strip the line
		line = line.strip()

		#Add the path to the list
		paths.append(line)

#Get the encoding of the file
raw = open(path).read(min(32, os.path.getsize(path)))

#Check to see if it's utf 8
if(raw.startswith('\xef\xbb\xbf')):
	#Fix the first path
	paths[0] = (paths[0])[3:]

#Loop through the paths
for filePath in paths:
	#If the file exists, get the info
	if os.path.exists(filePath):
		#Open the file
		mp3File = eyed3.load(filePath)
		
		#Get the info
		lArtists.append(mp3File.tag.artist)
		lTracks.append(mp3File.tag.title)

#Look for the correct playlist
for playlist in playlists:
	if playlist['name'] == playlistName:
		#Log match found
		print("-----------------------------------------")
		print("Playlist name match found")
		print("-----------------------------------------")
		
		#Loop through the playlist contents looking for entries corresponding to the current playlist
		for entry in playlistContents:
			#Look for a id match
			if(playlist['id'] == entry['id']):
				#Loop through the tracks in each playlist
				for track in entry['tracks']:
					#Look for the name of each song
					for song in library:
						#If the id's match
						if(song['id'] == track['trackId']):
							#Add to the arrays for the gmusic artists and tracks
							gArtists.append(song['artist'])
							gTracks.append(song['title'])
		#Compare the lengths of the arrays for the initial check
		if(len(lArtists) == len(gArtists)):
			print("-----------------------------------------")
			print("Playlist lengths are equal, compare playlists...")
			print("-----------------------------------------")
			
			#Current mismatch count
			mismatchCount = 0
			
			#Loop through the playlists and compare
			for x in range(0, len(lArtists) - 1):
				#If a mismatch is found
				if((lArtists[x] != gArtists[x]) or (lTracks[x] != gTracks[x])):
					#Log the mismatch
					print("Mismatch found:")
					print("Local Artist: ", lArtists[x], "Local Track: ", lTracks[x])
					print("gMusic Artist: ", gArtists[x], "gMusic Title: ", gTracks[x])
					
					#Increment the count
					mismatchCount = mismatchCount + 1
					
			#Print the total number of mismatches
			print("Total Number of Mismatches: ", mismatchCount)
		#Else, lengths are not equal
		else:
			print("-----------------------------------------")
			print("Playlist lengths are not equal")
			print("Local Playlist Length: ", len(lArtists), "gMusic Playlist Length: ", len(gArtists))
			print("Exiting....")
			print("-----------------------------------------")