#!usr/bin/python

# This script given the path and file name searches for the file recursively and return the first file containing any of the tokens of the search

import os

def find_file(file, path):												
	'''file parameter should be a list of tokens'''
	directories = []

	#first check for all files in the directory
	for f in os.scandir(path):	
		if(f.is_file()):
			for name in file:
				#ignoring 3 letter names as might be too common
				if(len(name)>3 and name.lower() in f.name.lower()): return path + '/' + f.name
		elif(f.is_dir()):
			directories.append(f.name)

	#if not found then check in subdirectories
	for directory in directories:
		found = find_file(file, path + '/' + directory)
		if(found != None): return found

	return None					#return null if file not found



if __name__ == "__main__": main()
