#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### IMPORTS -----------------------------------------------------------------------------------------------------------------------------------------

import os, sys, subprocess, math, platform

# Check the current version of Python
if sys.version_info[0] < 3:
    print("Please, use Python 3.")
    # Quit the program
    exit()

from libs.functions import clear

# Ask for the path to python 2
python2 = input("\n Write the alias or the path to python2: ")

clear()

# List of modules using python 2
python2Modules = ["spiderfoot"]

### MAIN --------------------------------------------------------------------------------------------------------------------------------------------

# Absolut path to the modules directory
modulesPath = os.sep.join([os.path.dirname(os.path.abspath(__file__)), "modules"])
# List of modules
modulesList = os.listdir(modulesPath)
# Set the index of the pip module
pipIndex = modulesList.index("pip")
# Place pip in first place to upgrade its tools
modulesList[0], modulesList[pipIndex] = modulesList[pipIndex], modulesList[0]

# If there at least one module
if len(modulesList) > 0:
	# Print the banner
	print(" Download of requirements:\n")
	# Lenght of the longest module name for esthetical printing purpose
	longestModuleName = max(modulesList, key=len)

	# For each module in the list
	for module in modulesList:
		# Set the path to the requirements file
		filePath = os.sep.join((modulesPath, module, "requirements.txt"))
		# If a requirements file exist
		if os.path.exists(filePath):
			# Print the current module name
			sys.stdout.write("\t■ {}".format(module) + " " * (len(longestModuleName) - len(module)) + "\t\t   0%\t[          ]")
			sys.stdout.flush()			
			# Open the requirements file
			with open(filePath, "r") as file:
				# Set the list of packages
				packages = file.read().split("\n")
				# Remove the empty names
				packages = [package for package in packages if package != ""]
				# Set the count of package for printing purpose
				packagesCount = len(packages)
				# Set a current package index for printing purpose
				currentPackageIndex = 0

				# For each package in the list
				for package in packages:
					# Set the command
					command = (sys.executable if module not in python2Modules else python2) + " -m pip install --upgrade " + package
					# Check for linux systems
					if platform.system() == "Linux":
						# Add a sudo argument
						command = "sudo -H " + command
					# Start the download
					output = subprocess.Popen(command.split(" "), stdout=open(os.devnull, "wb"), stderr=subprocess.PIPE)
					# Get the errors
					error = output.communicate()[1].decode()
					# If there is at least one error
					if error != "" and error[0:11] != "DEPRECATION":
						# Print them
						print("\n\n{}".format(error))
					# If there is no error
					else:
						# Increase the current package index for printing purpose
						currentPackageIndex += 1
						# Set the current download progress for printing purpose
						currentProgress = int(currentPackageIndex * 100 / packagesCount)
						# Print the new progress
						sys.stdout.write("\b" * 18 + " {}%\t[".format(currentProgress) + ("■" * int(currentProgress / 10)) + (" " * math.ceil((100 - currentProgress) / 10)) + "]{}".format("\n" if packagesCount == currentPackageIndex else ""))
						sys.stdout.flush()
		
		# If no requirements file found
		else:
			print("\nNo requirements found for the {} module".format(module))

# If no modules fond
else:
	print("No modules found at {}.".format(modulesPath))

# Set the path to the spiderfoot module server
spiderfootServerPath = os.sep.join([os.path.dirname(os.path.abspath(__file__)), "modules", "spiderfoot", "sf.py"])
# Start the spiderfoot module server
spiderfootServer = subprocess.Popen(python2.split(" ") + [spiderfootServerPath], stdout=open(os.devnull, "wb"), stderr=open(os.devnull, "wb"))
#fatalError("Impossible to start the spiderfoot server. Make sure that there is no other instance of sf.py running and that no other program use the port number 5001.")
input("\n Servers are on. Keep this process open until you finished all your scans. Then press 'Enter'\n")
# Close the spiderfoot module server
spiderfootServer.terminate()
# Display end message
print(" Servers are off. You can quit this process.")