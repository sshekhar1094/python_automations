#!usr/bin/python

	# Script to decrypt files of the encrypted folder
	# The password acts as key for deryption

import os
import getpass
from crypto import decode 											#function just to encrypt string, write your own

def main(path, password):
	decodedList = []

	for file in os.scandir(path):									#iterates through all files and directories in given path
		cyphertext = file.name 
		plaintext  = decode(password, cyphertext)					#decrypt
		decodedList.append([cyphertext, plaintext])

	for i in range(0, len(decodedList)):							#show the decryptions
		print("%d.%s" % (i+1, decodedList[i][1]))

	#now wait if the user wants to play a video file
	while(True):
		print('\n')
		no = int(input("Enter serial number of file to play:"))
		command = 'vlc ' + path + '/' + decodedList[no-1][0]
		os.system(command)


if __name__ == "__main__": 
	path = input('Enter path:')
	password = getpass.getpass()
	main(path, password)
