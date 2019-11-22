#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### IMPORTS -----------------------------------------------------------------------------------------------------------------------------------------

# Read system info
import sys

# Manipulate system paths
import os.path

# Import specific functions for this script
from libs.functions import loadModules, fatalError, startModule, warning

## PHOTON -----------------------------------------------------------------------------------------

# Load JSON string as object
from json import loads

### MAIN --------------------------------------------------------------------------------------------------------------------------------------------

# Print the current version of Python
print("Main script executed with Python " + str(sys.version_info[0]) + "." + str(sys.version_info[1]))

# Load the modules configuration file
modules = loadModules()

## PHOTON -----------------------------------------------------------------------------------------

# Set the final variable 
result = None#{"email": ["guyon@et.esiea.fr", "innocenti@et.esiea.fr"]}#None

# Get the return code of the module execution
returncode = startModule(modules, "photon")

# If the execution succed
if returncode == 0 :
	# Set the path to the result file
	filePath = os.sep.join([modules["photon"]["args"][3]["value"], "exported.json"])
	# Open the result file
	with open(filePath, "r") as file:
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

## H8MAIL && SPIDERFOOT -----------------------------------------------------------------------------------------

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
		startModule(modules, "h8mail", ["--target", emails])
		# Start the spiderfoot module with the email list
		startModule(modules, "spiderfoot", emails)
	# If the email list is empty
	else:
		# Print a warning message
		warning("No email to scan with the module \"h8mail\".")
		# Print a warning message
		warning("No email to scan with the module \"spiderfoot\".")

## ------------------------------------------------------------------------------------------------