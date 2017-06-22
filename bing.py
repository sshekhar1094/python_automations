#!/usr/bin/python
# Downloads the Bing wallpaper of the day and sets it as the ubuntu desktop background

import urllib.request
import urllib.parse
import json
import os
import time
import sys

def main(url):
	time.sleep(15)											#wait for 15sec after startup
	filename = str(time.strftime("%d-%m-%Y")) + '.jpg'
	path = '/home/shashank/Pictures/Wallpapers/' + filename	#folder for saving wallpaper

	#execute only if running for first time after 12pm
#	if int(time.strftime("%H")) < 12 : 
		#print("Time less than 12")
#		sys.exit()

	if os.path.exists(path):
		#print("Wallpaper up to date")
		sys.exit()
 
	#extract url for json
	headers = {}		#empty dictionary
	headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
	request = urllib.request.Request(url, headers=headers)
	response = urllib.request.urlopen(request)

	#load json
	obj = json.loads(response.read().decode())				#saving to json
	#print(json.dumps(obj, indent=2))						#prints json in pretty format
	url = (obj['images'][0]['urlbase'])
	url = 'http://www.bing.com' + url + '_1920x1080.jpg'	#image url

	#Now save the image to a file
	f = open(path, 'wb')
	f.write(urllib.request.urlopen(url).read())
	f.close()

	#Now set as wallpaper
	command = 'gsettings set org.gnome.desktop.background picture-uri file://' + path
	os.system(command)

main('http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US')
