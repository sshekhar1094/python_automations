#!/usr/bin/python
# Get ratings from imdb

# Takes in a search query, searches for it on imdb and then returns the top 10 results. Then gives the imdb rating of the selected result
# Improvement- use the IMDB api instead of making requests

import requests
import sys
from bs4 import BeautifulSoup

def main():
	#print(type(sys.argv))
	url = 'http://www.imdb.com/find?ref_=nv_sr_fn&q='
	if(len(sys.argv) == 1):
		show = input("Enter name of show: ")
		show = show.split(' ')
	else:
		show = sys.argv[1:]

	name = show[0]
	for i in range(1, len(show)):
		name = name + '+' + show[i]

	#Showing results
	url = url + name + '&s=all'
	data = requests.get(url)
	soup = BeautifulSoup(data.text, 'html.parser')
	table = soup.find('table')
	rows = table.find_all('tr')
	print("These are the top results:\n")
	arr = []
	for i, row in enumerate(rows):
		text = row.find_all('td')[1].text
		print(i+1, ':', text)
		arr.append((text, row.find_all('a')[1]['href']))
	print('')

	#Finding rating for selection
	res = int(input("Enter your show's index: "))
	res = res - 1
	url = 'http://www.imdb.com/' + arr[res][1]
	name = arr[res][0]
	data = requests.get(url)
	soup = BeautifulSoup(data.text, 'html.parser')
	rating = soup.find('div', {'class':'imdbRating'}).find('span').string
	print(name, '--->', rating)


if __name__ == "__main__": main()
