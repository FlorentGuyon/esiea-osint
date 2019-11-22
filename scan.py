#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### IMPORTS -----------------------------------------------------------------------------------------------------------------------------------------

# Manage arguments
from getopt import getopt

# Read system info
import sys

# Manipulate system paths
import os.path

# Import specific functions for this script
from libs.functions import loadModules, fatalError, startModule, warning

## PHOTON -----------------------------------------------------------------------------------------

# Load JSON string as object
from json import loads

## CONSTANTS --------------------------------------------------------------------------------------

# Normalised value of the target type URL
targetType_URL = "url"

# Normalised value of the target type Name
targetType_NAME = "name"

### MAIN --------------------------------------------------------------------------------------------------------------------------------------------

# Display an help message
def displayHelp():
	# Lines of the message
	lines = [
		"",
		"  ╔════════════════════╗",
		"  ║ DO YOU NEED HELP ? ║",
		"  ╠════════════════════╩═════════════════════════════════════════════════════════════════════╗",
		"  ║ Enter your argument as follows:                                                          ║",
		"  ║                                                                                          ║",
		"  ║   ■ python scan.py -h or --help                                                          ║",
		"  ║   ■ python scan.py -n \"<firstname> <lastname>\" or --name=\"<firstname> <lastname>\"        ║",
		"  ║   ■ python scan.py -u <url> or --url=<url>                                               ║",
		"  ║                                                                                          ║",
		"  ╚══════════════════════════════════════════════════════════════════════════════════════════╝"
	]
	# Print the final message
	print("\n".join(lines))

# First function called
def main(argv):

	# Test if the arguments are valid
	try:
		# Extract the arguments following this options
		opts, args = getopt(argv, "hn:u:", ["help", "name=", "url="])
	# If the arguments are invalid
	except:
		# Display an help message
		displayHelp()
		# Exit the script
		fatalError("\"" + " ".join(argv) + "\" are not valid arguments.")

	# Type of the target: name, url...
	targetType = None
	# Value of the scan target
	targetValue = None

	# If the arguments are missing
	if len(opts) == 0:
		# Display an help message
		displayHelp()
		# Exit the script
		fatalError("The arguments are missing.")

	# For all arguments
	for opt, arg in opts:
		# If the argument is about help
		if opt in ("-h", "--help"):
			displayHelp()
			quit()
		# Else if the argument is about a name
		elif opt in ("-n", "--name"):
			targetType = targetType_NAME
			targetValue = arg
		# Elif the argument is about an url
		elif opt in ("-u", "--url"):
			targetType = targetType_URL
			targetValue = arg

	# Print the current version of Python
	print("Main script executed with Python " + str(sys.version_info[0]) + "." + str(sys.version_info[1]))
	# Print of the scan details
	print("Research from the " + str(targetType) + " " + str(targetValue))
	# Load the modules configuration file
	modules = loadModules()
	# Set the final variable 
	result = None

	## PHOTON -----------------------------------------------------------------------------------------

	# If the target type is an URL
	if targetType == targetType_URL:
		# Get the return code of the module execution
		returncode = startModule(modules, "photon", ["--url", targetValue])
		# If the execution succed
		if returncode == 0 :
			# Set the path to the result file
			filePath = os.sep.join([targetValue, "exported.json"])
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

	# Else if the target type is a name
	elif targetType == targetType_NAME:
		# Format the name for the spiderfoot module 
		name = "\"" + targetValue + "\""
		# Start the spiderfoot module
		startModule(modules, "spiderfoot", name)

## ------------------------------------------------------------------------------------------------

if __name__ == "__main__":
	# Call the main function with all the arguments except the path to this file
	main(sys.argv[1:])

## ------------------------------------------------------------------------------------------------