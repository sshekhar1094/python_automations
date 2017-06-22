#!/usr/bin/python

# Python script to move mouse by one pixel every 5 minutes
# External module to install: pyautogui,  -----> $ sudo pip3 install pyautogui


import pyautogui as mouse 				#module for controlling mouse
import time
import sys


WAIT_TIME = 300							#default waiting time before each mouse movement = 300 seconds


def exceptionHandler(exception_type, exception, traceback):
	print("  %s\n" % (exception_type.__name__))


def main():
	print("Executing \nEnter 'CTRL + C' anytime to exit the program\n")
	sys.excepthook = exceptionHandler	#custom exception handler
	while True :
		mouse.moveRel(1, 1)				#move mouse by 1pixel right and down
		time.sleep(WAIT_TIME)			#wait


if __name__ == "__main__": main()
