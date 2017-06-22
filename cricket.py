#Script to get cricket scores and display it every 10 secs, asks user the url to 

import requests
import os
import re
import time
import pyperclip				#to access clipboard
from bs4 import *
from selenium import webdriver
from pyvirtualdisplay import Display

if(os.name != "nt"): display = Display(visible=0, size=(800, 600))

def setVirtualDisplay():
	#Dont physically open the browser
	if(os.name == "nt"): return
	display.start()

def StopDisplay():
	if(os.name == "nt"): return
	display.stop()

def getBrowser():
	if(os.name == "nt"):
		browser = webdriver.Firefox()
	else:
		chromedriver = "/home/shashank/python_learn/driver/chromedriver"
		os.environ["webdriver.chrome.driver"] = chromedriver
		browser = webdriver.Chrome(chromedriver)
	browser.set_page_load_timeout(200)
	return browser

def getScore(url):
	try:
		browser = getBrowser()
		print("Now extracting")
		var = 1

		while var==1:
			try:
				browser.get(url)
			except Exception as e:
				print("Timed out, loading again")
				browser.quit()
				browser = getBrowser()
				continue


			try:
				html = browser.page_source
				soup = BeautifulSoup(html, "html.parser")

				page = soup.html
				title = soup.title.string
				score = title.partition(",")[0] + ')'
				required = soup.find('div', {'class':'innings-requirement'}).string.lstrip()

				batsmen = soup.find('table', {'class':'batsmen'})
				bats1 = batsmen.find('tr', {'class':'row1'})
				bats2 = batsmen.find('tr', {'class':'row2'})
				divs = bats1.find_all('td')
				bname1 = divs[0].a.string
				run1 = divs[1].string
				ball1 = divs[2].string
				divs = bats2.find_all('td')
				bname2 = divs[0].a.string
				run2 = divs[1].string
				ball2 = divs[2].string

				bowlers = soup.find('table', {'class':'bowlers'})
				bow1 = bowlers.find('tr', {'class':'row1'})
				bow2 = bowlers.find('tr', {'class':'row2'})
				divs = bow1.find_all('td')
				wname1 = divs[0].a.string
				overs1 = divs[1].string 
				brun1 = divs[3].string 
				wick1 = divs[4].string 
				divs = bow2.find_all('td')
				wname2 = divs[0].a.string
				overs2 = divs[1].string 
				brun2 = divs[3].string 
				wick2 = divs[4].string 

			except Exception as e:
				print(str(e))
				browser.quit()
				browser = getBrowser()
				continue

			if(os.name == "nt"):	#windows
				print(score)
				print(bname1 + ": " + run1 + "(" + ball1 + ")"
					+ "   |   " + bname2 + ": " + run2 + "(" + ball2 + ")")
				print(wname1 + ": " + brun1 + "/" + wick1 + "(" + overs1 + ")"
					+ "   |   " + wname2 + ": " + brun2 + "/" + wick2 + "(" + overs2 + ")")
				print(required)

				command = 'C:\\notify\\notify-send ' + '"' + score + '"' + ' "' + bname1 + ": " + run1 + "(" + ball1 + ")" + "   |   " + bname2 + ": " + run2 + "(" + ball2 + ")" + "   |   " + wname1 + ": " + brun1 + "/" + wick1 + "(" + overs1 + ")" + "   |   " + wname2 + ": " + brun2 + "/" + wick2 + "(" + overs2 + ")" + '"'
				#print(command)
				os.system(command)
			else:					#linux
				#instead send a notification
				command = 'notify-send ' + '"' + score + '" ' + '"$(echo "' + bname1 + ": " + run1 + "(" + ball1 + ")" + "   |   "  + bname2 + ": " + run2 + "(" + ball2 + ")" + '\n' + wname1 + ": " + wick1 + "/" + brun1 + "(" + overs1 + ")" + "   |   " + wname2 + ": " + wick2 + "/" + brun2 + "(" + overs2 + ")" + '\n' + required + '")"'
				os.system(command)

			time.sleep(60)	#update again after 60sec

		browser.quit()

	except Exception as e:
		print(str(e))


def main():
	#url = input('Enter url for match: ')
	url = pyperclip.paste()				#copies from clipboard

	print("URL from clipboard is: " + url)
	response = input("Enter y to continue with url, else n to change: ")
	if response=='n' or response=='N':
		url = input('Enter url for match: ')

	setVirtualDisplay()
	getScore(str(url))
	StopDisplay()
	#getScore("http://www.espncricinfo.com/india-v-new-zealand-2016-17/engine/match/1030215.html")

main()
