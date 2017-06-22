import requests
import os
import time
from bs4 import *

def main():
	time.sleep(15)		#execute after 15s into startup
	data = requests.get('http://www.merriam-webster.com/word-of-the-day')
	soup = BeautifulSoup(data.text, "html.parser")	

	word = soup.find('div', {'class':'word-and-pronunciation'}).h1.string
	attr = soup.find('span', {'class':'main-attr'}).string
	pronunciation = soup.find('span', {'class':'word-syllables'}).string

	container = soup.find('div', {'class':'wod-definition-container'})
	lines = container.find_all('p')
	definition = lines[0].text
	def2 = lines[1].text
	example = lines[-2].text	

	if(def2 == example): def2 = ''
	example = example.replace(';', ',').split('—')[0]
	example = example.replace('"', '')
	example = example.replace("'", "")
	example = example[:300]					#example should be max 300 chars else notify-send overflows

	print(definition, def2, example, sep='\n')

	command = 'notify-send "' + word + '" "$(echo "' + attr + '    |    ' + pronunciation + ' \n' + definition + ' \n'+def2+' \n. \n' + example +'")"'
	
	print(command)
	os.system(command)
	osname = os.name

	var = 1
	while var==1:
		if(osname == "nt"):
			print(word)
			print(attr + '    |    ' + pronunciation)
			print(example)
		else:
			i = 0
			while i<3:
				os.system(command)
				i = i+1
		time.sleep(300)

main()
