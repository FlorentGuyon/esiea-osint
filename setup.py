#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### IMPORTS -----------------------------------------------------------------------------------------------------------------------------------------

# Manipulate system paths
import os.path

# Read system informations
import sys

# Specific functions for this script
from libs.functions import loadModules, fatalError, isFile, warning, success

### MAIN --------------------------------------------------------------------------------------------------------------------------------------------

# Load the modules configuration file
modules = loadModules()

# Empty the requirements list
requirements = ""
# For all module in the configuration file
for index, (moduleKey, moduleData) in enumerate(modules.items()):
	# Set the requirements path of the current module
	requirementsPath = os.sep.join([os.path.abspath("."), "modules", moduleKey, "requirements.txt"])
	# If the requirements file exists
	if isFile(requirementsPath):
		# Open the file
		with open(requirementsPath, "r") as file:
			# extract the data		
			requirements += file.read() + "\n"
	# If the requirements file does not exist
	else:
		# Print a warning message
		warning("Requirements file not found at " + requirementsPath + ".")

# Set the path of the total requirements file
finalRequirementsPath = os.sep.join([os.path.abspath("."), "requirements.txt"])
# Open the file
with open(finalRequirementsPath, "w") as file:
	# Write the list of requirements
	file.write(requirements)
	# Print advices about the downloading of the requirements
	success("The list of requirements is now available at \"" + finalRequirementsPath + "\".\nMake sure to download them before running the \"main.py\" script.\nYou can download the requirements by running the following command: \"python3 -m pip install --upgrade -r " + finalRequirementsPath + "\".")