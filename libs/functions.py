#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### IMPORTS -----------------------------------------------------------------------------------------------------------------------------------------

import os, json, subprocess, platform, time, requests

from selenium import webdriver as wd
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup as bs

### CONFIG ------------------------------------------------------------------------------------------------------------------------------------------

# Modules configuration
modulesConfigurationPath = os.sep.join([os.path.dirname(os.path.abspath(__file__)), "..", "modules.json"])

### FUNCTIONS ---------------------------------------------------------------------------------------------------------------------------------------

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

## EXIT SCRIPT AFTER A FATAL ERROR
def fatalError(msg = None):
	# If there is a message to display
	if msg != None:
		# Print the message
		print(msg)
	# Quit the main script
	exit()

## PRINT ERROR EVENT
def error(msg):
	# Print the message
	print("\n------------------------------------------------------------------------\n[ERROR] " + msg + "\n------------------------------------------------------------------------")

## PRINT WARNING MESSAGES
def warning(msg):
	# Print the message
	print("\n[WARNING] " + msg)

## PRINT SUCCESS EVENT
def success(msg):
	# Print the message
	print("\n[SUCCESS] " + msg)

## RETURN TRUE IF THE FILE EXISTS
def isFile(path):
	return os.path.isfile(path)

## LOAD MODULES DATA
def loadModules():
	# If the path is valid
	if isFile(modulesConfigurationPath):
		# Return the json Object
		return extractJson(modulesConfigurationPath)

	# If the file does not exist
	else:
		# Print an error message
		error("No modules configuration file at " + modulesConfigurationPath)
		# Print a fatal error message
		fatalError("The script cannot work without a modules configuration file.")


## START A MODULE WITH ITS ARGUMENTS
def startModule(modules, moduleKey, extraArgs = None):
	# Is the moduleKey in the config file
	try:
		# If yes, load the data
		module = modules[moduleKey]
	# If no
	except:
		# Print an error message
		error("No module named \"" + moduleKey + "\" in " + modulesConfigurationPath)
		# Quit the function with an error code
		return -1

	# If the module has a name
	try:
		# Load the name
		moduleName = module["name"]
		# Print the loaded name
		print("\n[Start module | " + moduleName + "]")
	# If the module does not have name
	except:
		# Print a warning message
		warning("No name defined for module \"" + moduleKey + "\" in " + modulesConfigurationPath)

	# If the module has a description
	try:
		# Load the description
		moduleDescription = module["description"]
		# Print the loaded description
		print("\"" + moduleDescription + "\"")
	# If the module does not have a description
	except:
		# Print a warning message
		warning("No description defined for module \"" + moduleKey + "\" in " + modulesConfigurationPath)
	
	# Set the list of arguments
	command = []

	# If the module has arguments
	try: 
		# Load the argument list
		moduleArgs = module["args"]
		# For each argument
		for arg in moduleArgs:
			# Get the value of the argument
			arg = arg["value"]
			# If the current argument is a list
			if type(arg) is list:
				# Join the elements of the list with the correct system separator
				arg = os.sep.join(arg)
			# Turn the argument to a string
			arg = str(arg)
			# Insert the argument to the command list
			command.append(arg)
	# If the module does not have arguments
	except:
		# Print a warning message
		warning("No args defined for module \"" + moduleKey + "\" in " + modulesConfigurationPath)

	# If the function has extra arguments
	if extraArgs != None:
		# If there are several arguments
		if type(extraArgs) is list:
			# For each of the arguments
			for arg in extraArgs:
				# If the current argument is a list
				if type(arg) is list:
					# Join the elements of the list with the correct system separator
					arg = os.sep.join(arg)
				# Turn the argument to a string
				arg = str(arg)
				# Insert the argument to the command list
				command.append(arg)
		# If there is only one argument
		else:
			# Add the argyument to the command list
			command.append(extraArgs)

	# Print the final command
	#print("\n" + " ".join(command))

	# Save the result of the execution of the command
	result = subprocess.call(command)

	# Print the end of the module
	print("\n[End module | " + moduleName + "]")

	# Return the result of the execution
	return result

# Display an error message for wrong attribute types
def wrongAttrType(self, attr, rightType, wrongVal):
	print('"{}" attribute of "{}" class must be "{}", not "{}"'.format(
		attr, 
		self.__class__.__name__, 
		rightType.__name__, 
		wrongVal.__class__.__name__))
	exit()

# Extract data and parse them as JSON
def extractJson(filePath):
	# Open the result file
	with open(filePath, "r") as file:
		# Extract the text		
		string = file.read()
		# Load the data as an object
		jsonObject = json.loads(string)
		# Return the result
		return jsonObject


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