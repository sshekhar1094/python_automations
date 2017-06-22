# Displays teh current weather conditions

import requests
from bs4 import *
import os

data = requests.get("http://www.accuweather.com/en/in/hyderabad/202190/weather-forecast/202190")
#data = requests.get("https://www.google.co.in/search?q=hyderabad%20weather&rct=j")
soup = BeautifulSoup(data.text, "html.parser")

#For accuweather
data1 = soup.find('span', {'class':'large-temp'})
data2 = soup.find('span', {'class':'cond'})

#For Google
# data1 = soup.find('span', {'class':'wob_t'})
# data2 = soup.find('span', {'class':'vk_gy vk_sh'})

#Temperature
temp = data1.string
condition = data2.string

if(os.name == "nt"):
	command = 'C:\\notify\\notify-send ' + '"Temperature: ' + temp + '" ' + '"Condition: ' + condition + '"' 
else:
	command = 'notify-send "Hello Shashank" "$(echo "Current Temperature = ' + temp + '.\nCondition = ' + condition + '.")"'
os.system(command)
