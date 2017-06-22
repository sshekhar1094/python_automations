#!usr/bin/python

# Command line tool, takes in a music file name and plays the first result


import os
from file_finder import find_file


sara = '\n****\tSara: '														#name

#speaks out the text
def speak(text):														
	print(sara + text + '\n')
												

#task is to play music, plays the relevant music file
def music(res):															
	res = res[res.index(' ')+1:]											#remove word play 
	print(sara + 'Searching for ' + res + '\n')

	path = '/media/shashank/Entertainment/MUSIC'							#folder containig all music files
	file = res.split(' ')													#tokenize
	file = find_file(file, path)											#actual name of file looking for
	if(file == None):
		speak('Sorry, ' + res + ' not found')
	else:
		speak('Playing ' + file)
		command = 'mpg321 --quiet "' + file + '"' 
		os.system(command)


#function to process the user response
def process(response):													
	if(response.startswith('play')):										#user wants to play music
		music(response)


#function to listen to user
def listen():															
	response = input('****\tCommand: ')	
	process(response)


#my main function
def main():
	speak('Hello Shashank. Anything I can do for you My Lord')
	listen()


if __name__ == "__main__": main()
