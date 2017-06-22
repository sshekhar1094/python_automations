#!usr/bin/python

	# Script to encrypt all files and sub directories in the given directory
	# Simply give the path and password which then acts as key for encryption
	# This script does its task recursively

import os
import getpass
from crypto import encode										#function just to encrypt string, write your own

def main(path, password):
	print("\nCWD: " + path)										#Current working directory
	files = []
	directories = []

	for f in os.scandir(path):									#iterates through all files and directories in given path
		if(f.is_file()): files.append(f.name)
		else: directories.append(f.name)

	for file in files:
		cyphertext = encode(password, file)						#encrypt
		try:
			os.rename(path+'/'+file, path+'/'+cyphertext)		#change name to encrypted one
		except Exception as e:
			print(file)
			print(str(e))


	for directory in directories:
		main(path+'/'+directory, password)						#recurse on all sub-directories
		cyphertext = encode(password, directory)
		try:
			os.rename(path+'/'+directory, path+'/'+cyphertext)	#change directory name
		except Exception as e:
			print(directory)
			print(str(e))


if __name__ == "__main__": 
	path = input('Enter path:')
	password = getpass.getpass()
	main(path, password)
