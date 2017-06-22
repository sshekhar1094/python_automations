#!usr/bin/python
# https://automatetheboringstuff.com/ has links to each of its chapters in html format.
# This file opens all those links and saves teh webpage as pdf
# can be used as a sample to downlaod any web page

import requests
import pdfkit								# module that converts web pages to pdf
from bs4 import *

def main():
	url = 'https://automatetheboringstuff.com/'

	data = requests.get(url)
	soup = BeautifulSoup(data.text, "html.parser")
	container = soup.find_all('ul')[1]		# [1] contains links to all chapters
	links = container.find_all('a')			# links to chapters
	
	for link in links:

		name = link.string + '.pdf'			# filename for pdf
		name = name.replace(' ', '_')		# replace all spaces in name with _
		name = '/home/shashank/Downloads/pdfkit/' + name 	#folder to save in
		path = url + link.get('href')		# actual link to the web page

		pdfkit.from_url(path, name)


if __name__ == "__main__": main()
