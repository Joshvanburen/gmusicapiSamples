#Josh Van Buren
#Test Script for the gmusicapi

#Imports
from gmusicapi import Mobileclient
import os
import eyed3
from mutagen.mp3 import MP3

#Root music directory to search through
rootDir = "C:\\Users\\Joshv\\Josh\\Josh's Music"

#Directory to write the playlist file to
writeDir = "C:\\Users\\Joshv\\Desktop"

#Create the mobile client
api = Mobileclient()

#api.perform_oauth('C:\\Users\\Joshv\\Josh\\Programming\\Python\\googleMusic\\gMusicDeviceID.txt')
api.oauth_login('b83fce595c6fd82bcfcfdd8e2e542d79f3c176bb0974c4bb34da2df10d95cec1')

#Retrieve all playlists
playlists = api.get_all_playlists(False, False)

#Retrive the contents of all playlists
playlistContents = api.get_all_user_playlist_contents()

#Get the entire song library
library = api.get_all_songs(False, False)

#loop through all of the playlists
for playlist in playlists:	
	#Output the name of the playlist
	print("Playlist Name: " + playlist['name'])
	
	#Path to write to
	m3uFilePath = writeDir + "\\" + playlist['name'] + ".m3u"
	
	#Open the file
	m3uFile = open(m3uFilePath, 'w')
	
	#Write the first line
	m3uFile.write('#PLaylist\n')
	
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
						#Loop through the directory structure
						for currDir, subDirectories, files in os.walk(rootDir):
							#Loop through the files
							for file in files:
								#If the file is a mp3
								if(file.endswith('.mp3')):
									#Load the mp3
									mp3File = MP3(os.path.join(currDir, file))
									
									#If the tag data matches
									if((song['artist'] == mp3File['TPE1']) and (song['title'] == mp3File['TIT2'])):
										#Print the playlist, artist and title info
										print(playlist['name'] + ": " + song['artist'] + " - " + song['title'] + " Path: " + os.path.join(currDir, file))
										
										#Write to the file
										m3uFile.write(os.path.join(currDir, file) + '\n')
										
	#Close the file
	m3uFile.close()