#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# SYS CALLS
import sys

# OS CALLS
import os

# JSON DUMPS AND SERIALIZATION
import json

# MULTITHREADING
import subprocess

# OS DETECTION
import platform

# TIME MANIUPLATIN
import time

# WEB REQUESTS
import requests


#____PACKAGE_______________________________________OBJEECT_________________RENAME_
from selenium 								import webdriver 			as wd
from selenium.webdriver.firefox.options 	import Options
from selenium.webdriver.common.by 			import By
from selenium.webdriver.common.keys 		import Keys
from webdriver_manager.firefox 				import GeckoDriverManager
from bs4 									import BeautifulSoup 		as bs



resultsPath = None
resultsName = None


def getResultsPath():
	return resultsPath


def setResultsPath(value):
	global resultsPath
	resultsPath = value


def getResultsName():
	return resultsName


def setResultsName(value):
	global resultsName
	resultsName = value


def checkPythonVersion():

	# Check the current version of Python
	if sys.version_info[0] < 3:
	    print("Please, use at least Python 3.6")
	    # Quit the program
	    exit()
	else if (sys.version_info[0] == 3) and (sys.version_info[1] < 6):
		print("Please, use at least Python 3.6")
		# Quit the program
		exit()


# Clear the shell
def clear():
	# If the current os is a windows
	if platform.system() == "Windows":
		# Use specific command
		os.system("cls")
	# Else if the current os is not a windows
	else:
		# Use generic command
		os.system("clear")


## RETURN TRUE IF THE FILE EXISTS
def isFile(path):
	return os.path.isfile(path)


def doesThisURLExist(url):

	try:
		doesThisURLExist = (requests.get(url, timeout=20).status_code == 200)
	except:
		doesThisURLExist = False

	return doesThisURLExist


def fromUsernameToWebsites(username):
	
	options = Options()
	options.headless = True

	browser = wd.Firefox(options=options, executable_path = GeckoDriverManager().install())

	browser.minimize_window()

	# Go to the URL
	browser.get("https://namechk.com/")

	browser.find_element_by_id("q").send_keys(username)
	browser.find_element(By.CSS_SELECTOR , '#app-form button.search-btn.btn.btn-block').send_keys(Keys.ENTER)

	time.sleep(10)

	# Load the page content
	HTML = browser.page_source

	browser.quit()

	# Parse the content as lxml
	parsedHTML = bs(HTML, 'lxml')

	existingWebsites = parsedHTML.select("section.app-body .box.unavailable")

	websites = []
	# This websites return a 200 stauts code even when the username is invalid
	blackListedWebsites = ["Imgur", "ProductHunt", "Tripit", "Kik", "Hackernews", "Younow", "Mixcloud", "Ask FM", "PayPal", "Wikipedia"]
	
	for account in existingWebsites:
		
		website = account.text
		link = None

		if website in blackListedWebsites:
			continue

		if account.select_one("a") != None:
			link = account.select_one("a")["href"]

		else:
			website = username + website
			link = "https://www." + website

		websites.append({"name": website, "link": link})

	return websites