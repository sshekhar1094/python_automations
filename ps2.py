#!/usr/bin/python
# This file creates an excel sheet of all the companies from the psd website
# 
# We have a psd website which lists the companies for internships. Name, stipend, disciplines, project details, facilities, all on different pages. Through selenium we automate the browser to scrape the psd website and creates an excel sheet containing all these in a single file with different columns. Thus easier to compare between the companies and make choices.
#
# External modules to install: bs4, selenium, pyvirtualdisplay, openpyxl -> $ sudo pip install openpyxl
# Note: pyvirtualdisplay might not work properly on windows, remove its components when executing on windows
# http://ideone.com/PWD6SI

import os
import openpyxl
from bs4 import BeautifulSoup
from selenium import webdriver
from pyvirtualdisplay import Display


def getBrowser():
	print("Loading webpage")
	chromedriver = "/home/shashank/python_learn/driver/chromedriver"
	os.environ["webdriver.chrome.driver"] = chromedriver
	browser = webdriver.Chrome(chromedriver)
	browser.set_page_load_timeout(100)				#timeout for loading page = 100s, else code exits with exception
	return browser


def Login(browser):
	print("Logging in")
	username = 'username'
	password = 'password'
	userbox = browser.find_element_by_name('TxtEmail')
	psswdbox = browser.find_element_by_name('txtPass')
	userbox.send_keys(username)
	psswdbox.send_keys(password)
	browser.find_element_by_name('Button1').click()		#login button
	browser.get('http://psd.bits-pilani.ac.in/Student/ViewProblemBankps2.aspx')		#move to problem bank page


def getProjects(browser, url):
	url = 'http://psd.bits-pilani.ac.in/Student/' + url
	while True:
		try: 
			browser.get(url)
			break
		except Exception as e:
			print(str(e), 'url=', url)

	soup = BeautifulSoup(browser.page_source, 'html.parser')
	projects = soup.find_all('div', {'id':'Project'})
	content = ''
	#Getting projects
	for project in projects[:-1]:
		header = project.find('h3').text
		rows = project.find_all('tr')
		title = 'Title: ' + str(rows[0].find_all('td')[1].string) + '\n'
		description = str(rows[1].find_all('td')[1].string) + '\n'
		skills = 'Skills: ' + str(rows[2].find_all('td')[1].string) + '\n'
		content = content + header + title + description + skills + '\n'

	#Getting facilities
	facilities = ''
	table = soup.find_all('table')[-5]
	rows = table.find_all('tr')
	for row in rows:
		facilities = facilities + row.text + '\n'

	return content, facilities


def FillExcel(sheet, dict, i):
	i = str(i+1)
	sheet['A' + i] = dict['location']
	sheet['B' + i] = dict['name']
	sheet['C' + i] = dict['industry']
	sheet['D' + i] = int(dict['stipendug'])
	sheet['E' + i] = int(dict['stipendpg'])
	sheet['F' + i] = int(dict['projects'])
	sheet['G' + i] = dict['disciplines']
	sheet['H' + i].alignment = sheet['H' + i].alignment.copy(wrapText=True)		#Enabling multiple lines text
	sheet['H' + i] = dict['projectDesc']
	sheet['I' + i].alignment = sheet['I' + i].alignment.copy(wrapText=True)
	sheet['I' + i] = dict['facilities']


def scrapeData(browser):
	print("Now extracting data and filling Excel")
	soup = BeautifulSoup(browser.page_source, 'html.parser')
	#soup = BeautifulSoup(open('spoj.html'), 'html.parser')

	wb = openpyxl.Workbook()		#excel object
	sheet = wb.get_sheet_by_name('Sheet')
	sheet['A1'] = 'Location'
	sheet['B1'] = 'Station Name'
	sheet['C1'] = 'Domain'
	sheet['D1'] = 'Stipend(UG)'
	sheet['E1'] = 'Stipend(PG)'
	sheet['F1'] = 'No of projects'
	sheet['G1'] = 'Disciplines'
	sheet['H1'] = 'Projects'
	sheet['I1'] = 'Facilities'

	table = soup.find('table')			#table containing the company data
	rows = table.find_all('tr')			#rows
	total = len(rows)					#no of rows

	for i in range(1, total):			#iterate from 1 to no of rows
		cells = rows[i].find_all('td')
		dict = {'projectDesc':'', 'facilities':''}						#empty dictionary
		dict['location'] = cells[1].string
		dict['name'] = cells[2].string 
		print("Extracting %d of %d: %s" % (i, total, dict['name']))
		dict['industry'] = cells[3].string 
		dict['stipendug'] = cells[4].string 
		dict['stipendpg'] = cells[5].string 
		dict['projects'] = cells[7].string 
		dict['disciplines'] = cells[8].string 
		try:
			projectDesc, facilities = getProjects(browser, cells[9].find('a')['href'])
		except Exception as e:
			print('Failed to load projects %s' % (dict['name']))
			projectDesc = 'Could not load'
			facilities = 'Could not load'
		dict['projectDesc'] = projectDesc
		dict['facilities'] = facilities
		FillExcel(sheet, dict, i)

	wb.save('ps.xlsx')
	print("Done")


def Logout(browser):
	return


def main(url):
	# display = Display(visible=0, size=(800, 600))	#does not show browser
	# display.start()					

	browser = getBrowser()
	browser.get(url)

	Login(browser)
	scrapeData(browser)
	Logout(browser)

	browser.quit()
	# display.stop()



if __name__ == "__main__": main("http://psd.bits-pilani.ac.in/Login.aspx")
