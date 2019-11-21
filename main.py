#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Commands calling
from subprocess import call

# JSON File reading
from json import loads

# Checking if a file exist
import os.path

# System info
import sys

### CONFIG ------------------------------------------------------------------------------------------------------------------------------------------

# Python 2
python2 = "D:\\Python2\\python"

# Python 3
python3 = "D:\\Python\\python"

# Modules configuration
modulesConfigurationPath = ".\\modules.json"

# Modules data
modules = None

# Download requirements during next execution
doDownloadRequirements = True

### FUNCTIONS ---------------------------------------------------------------------------------------------------------------------------------------

## EXIT SCRIPT AFTER A FATAL ERROR
def fatalError(msg):
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

## CHECK IF A FILE EXIST
def isFile(path):
	# Return True if the path is valid
	return os.path.isfile(path)

## LOAD MODULES DATA
def loadModules():
	# If the path is valid
	if isFile(modulesConfigurationPath):
		# Open the file
		with open(modulesConfigurationPath) as file:
			# extract the data		
			string = file.read()
			# Load the data as object
			json = loads(string)
			# Print a success message
			success("Modules configuration file loaded.")
			# Return the data object
			return json
	# If the file does not exist
	else:
		# Print an error message
		error("No modules configuration file at " + modulesConfigurationPath)
		# Return the error code
		return -1

## DOWNLOAD REQUIREMENTS
def downloadRequirements(pythonVersion, requirementsPath):
	# If the file exist
	if isFile(requirementsPath):
		# Print a downloading message
		print("\n[DOWNLOADING REQUIREMENTS]\n")
		# Download the requirements
		call(str(pythonVersion) + " -m pip install -r " + requirementsPath)
	# If the file does not exist
	else :
		# Print an error message
		error("No requirements file at " + requirementsPath)
		# Return an error code
		return -1
	# Return a success code
	return 0


## START A MODULE WITH ITS ARGUMENTS
def startModule(pythonVersion, moduleKey, extraArgs = None):
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

	# If the downloading of requirements is active
	if doDownloadRequirements:
		# If the module has requirements
		try:
			# Get the requirements file
			requirementsPath = module["requirements"]	
			# If the downloading succeed
			if downloadRequirements(pythonVersion, requirementsPath) == 0:
				# Print a success message
				success("requirements downloaded.")
			# If the downloading failed
			else:
				# Quit the function with an error code
				return -1		
		# If the module does not have requirements
		except:
			# Print a warning message
			warning("No requirements path defined for module \"" + moduleKey + "\" in " + modulesConfigurationPath)

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
		# For each argument, insert it to the list
		[command.append(str(arg["value"])) for arg in moduleArgs]
	# If the module does not have arguments
	except:
		# Print a warning message
		warning("No args defined for module \"" + moduleKey + "\" in " + modulesConfigurationPath)

	# If the function has extra arguments
	if extraArgs != None:
		# Add the extra arguments to the list
		[command.append(arg) for arg in extraArgs]

	# Print the final command
	print("\n" + " ".join(command))

	# Save the result of the execution of the command
	result = call(command)

	# Print the end of the module
	print("\n[End module | " + moduleName + "]")

	# Return the result of the execution
	return result

### MAIN --------------------------------------------------------------------------------------------------------------------------------------------

# Print the current version of Python
print("Main script executed with Python " + str(sys.version_info[0]) + "." + str(sys.version_info[1]))

# Load the modules configuration file
modules = loadModules()

# If the loading failed
if modules == -1:
	# Quit the script with an error message
	fatalError("The script cannot work without a modules configuration file.")

## PHOTON -----------------------------------------------------------------------------------------

# Get the return code of the module execution
returncode = startModule(python3, "photon")

# Set the final variable 
result = None

# If the execution succed
if returncode == 0 :
	# Open the result file
	with open(modules["photon"]["args"][3]["value"] + "\\exported.json") as file:
		# Extract the text		
		string = file.read()
		# Load the data as an object
		json = loads(string)
		# Save the interesting part of the object
		result = json['custom']
		# Print an empty line
		print("")
		# For each category of data (email, phone...)
		for key in result:
			# If there is at least one result
			if len(result[key]) > 0 :
				# Print the count of result
				print(" " + str(len(result[key])) + " " + key + " found:")
				# For each result
				for value in result[key]:
					# Print the result on a new line
					print("  - " + value)
			# If there is no result
			else :
				# Print a specific message
				print(" No " + key + " found.")
# If the execution failed
else:
	# Print a warning message
	warning("The \"photon\" module exits with an error.")

## H8MAIL -----------------------------------------------------------------------------------------

# If the execution of the "photon" module succed
if result != None:
	# If there is emails in the result
	try:
		# Save the list of email
		emails = ",".join(result["email"])		
	# If there is no emails
	except:
		# Print an error message
		error("The \"email\" dictionary is corrupted.")

	# If the email list saved is not empty
	if emails != "":
		# Start the h8mail module with the email list
		startModule(python3, "h8mail", ["--target", emails])
	# If the email list is empty
	else:
		# Print a warning message
		warning("No email to scan with the module \"h8mail\".")

## ------------------------------------------------------------------------------------------------