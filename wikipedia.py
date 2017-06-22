#!usr/bin/python

# Python script to take in query and read out summary of corresponding wikipedia article
# Uses google search intead of wiki search as google gives the most relevant article
# External modules: requests, bs4, gtts

import os
import sys
import requests
from bs4 import *															#web scraping
from gtts import gTTS as speech												#text to speech

def main():
	if(len(sys.argv) == 1):													#checking if cmd argument given
		query =  input("Enter search item:")
		query =  query.replace(' ', '+')
	else:
		query = '+'.join(sys.argv[1:])										#walmart labs = walmart+labs

	link    =  'https://www.google.co.in/search?q=wikipedia+' + query		#google search
	data    =  requests.get(link)
	soup    =  BeautifulSoup(data.text, "html.parser")
	link    =  'https://www.google.co.in' + soup.find('div', {'class':'g'}).h3.a.get('href')	#link of 1st item
	
	data    =  requests.get(link)											#wikipedia page
	soup    =  BeautifulSoup(data.text, "html.parser")
	summary =  soup.find('div', {'id':'mw-content-text'}).p.text 			#get the 1st para

	print(summary)
	tts = speech(summary, lang='en')										#save summary as mp3
	tts.save('wiki.mp3')
	os.system('mpg321 wiki.mp3')
	os.remove('wiki.mp3')

if __name__ == "__main__": main()
