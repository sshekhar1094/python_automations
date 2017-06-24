#!/usr/bin/python3.5

# A program to download all of the accepted solutions on spoj and save them to a directory
# External Modules to install: getpass, bs4, selenium, pyvirtualdisplay
# $ sudo pip install getpass, bs4, selenium, pyvirtualdisplay

import os
import time
import getpass
from bs4 import BeautifulSoup
from selenium import webdriver
from pyvirtualdisplay import Display

start_time = time.time()
directory = '/home/shashank/spoj/'


def getBrowser():
    print("Loading webpage")
    chromedriver = "/home/shashank/Dropbox/python_learn/driver/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    browser = webdriver.Chrome(chromedriver)
    browser.set_page_load_timeout(100)				#timeout for loading page = 100s, else code exits with exception
    return browser


# function to login into spoj
def Login(browser, username, password):
    url = 'http://www.spoj.com/login'
    browser.get(url)

    userbox = browser.find_element_by_xpath('//*[@id="inputUsername"]')
    psswdbox = browser.find_element_by_xpath('//*[@id="inputPassword"]')
    userbox.send_keys(username)
    psswdbox.send_keys(password)

    browser.find_element_by_xpath('//*[@id="content"]/div/div/form/div[4]/button').click()


# function to make a list of all accepted solutions links
def list_solved(browser):
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    table = soup.find('table', {'class' : 'table-condensed'})   #table contains all the accepted solutions
    links = table.find_all('a')

    url = 'http://www.spoj.com'
    links = [url + link.get('href') for link in links]
    return links


# opens those links, clicks on edit button, then saves the code onto a file
def get_content(links, browser):
    i = 1
    count = len(links)
    for link in links:
        print('Saving %d of %d : %s' % (i, count, link), ' | Elapsed time = ', time.time()-start_time)
        i = i+1

        browser.get(link)
        browser.find_element_by_xpath('//*[@title="Edit source code"]').click()  # clicks the edit button
        #browser.find_element_by_xpath('//*[@id="statusres_17240665"]/span/a[2]').click()    # clicks ideone button

        # now take the code out
        content = browser.find_element_by_name('file').get_attribute('value')
        # get the name of the file, link = http://www.spoj.com/status/ABCPATH,austin619/
        name = link.split('/')[4].split(',')[0]

        # now write to file
        file = open(directory+name+'.cpp', 'w')
        file.write(content)
        file.close()


def main():
    username = input("Enter your spoj username: ")
    password = getpass.getpass("[Spoj] password for " + username + ": ")

    display = Display(visible=0, size=(800, 600))	#does not show browser
    display.start()
    browser = getBrowser()

    Login(browser, username, password)

    # Now open the profile page
    browser.get('http://www.spoj.com/myaccount/')

    # profile page has a list of all accepted solutions, make a list of their links
    links = list_solved(browser)
    get_content(links, browser)

    display.stop()



if __name__ == "__main__": main()