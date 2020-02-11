#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# OS CALLS
import os

# SYSTEM CALLS
import sys

# MULTITHREADING
import subprocess

# MATHEMATICAL CEIL
import math

# OS DETECTION
import platform


def checkPythonVersion():

	# Check the current version of Python
	if sys.version_info[0] < 3:
	    print("Please, use at least Python 3.6")
	    # Quit the program
	    exit()
	elif (sys.version_info[0] == 3) and (sys.version_info[1] < 6):
		print("Please, use at least Python 3.6")
		# Quit the program
		exit()
	else:
		# If the current os is a windows
		if platform.system() == "Windows":
			# Use specific command
			os.system("cls")
		# Else if the current os is not a windows
		else:
			# Use generic command
			os.system("clear")


def getModulesPath():

	# Absolut path to the modules directory
	return os.sep.join([os.path.dirname(os.path.abspath(__file__)), "modules"])


def getModules():

	# Absolut path to the modules directory
	modulesPath = getModulesPath()
	# List of modules
	modulesList = os.listdir(modulesPath)
	# Set the index of the pip module
	defaultIndex = modulesList.index("default")
	# Place pip in first place to upgrade its tools
	modulesList[0], modulesList[defaultIndex] = modulesList[defaultIndex], modulesList[0]

	return modulesList


def getRequirements(module):

	# Set an empty package list
	packages = []
	# Absolut path to the modules directory
	modulesPath = getModulesPath()
	# Set the path to the requirements file
	filePath = os.sep.join((modulesPath, module, "requirements.txt"))
	# If a requirements file exist
	if os.path.exists(filePath):
		# Open the requirements file
		with open(filePath, "r") as file:
			# Set the list of packages
			packages = file.read().split("\n")
			# Remove the empty names
			packages = [package for package in packages if package != ""]

	return packages


def installPackage(package):

	# Set the command
	command = "{} -m pip install --upgrade {}".format(sys.executable, package)
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
		# return them
		return error

	else:
		return None


def startSetup():

	checkPythonVersion()
	modulesList = getModules()

	# If there at least one module
	if len(modulesList) > 0:
		# Print the banner
		print(" Download/Update requirements:\n")
		# Lenght of the longest module name for esthetical printing purpose
		longestModuleName = max(modulesList, key=len)

		# For each module in the list
		for module in modulesList:
			packages = getRequirements(module)
			# Set the count of package for printing purpose
			packagesCount = len(packages)
			# Set a current package index for printing purpose
			currentPackageIndex = 0

			if packagesCount > 0:
				# Print the current module name
				sys.stdout.write("\t■ {}".format(module) + " " * (len(longestModuleName) - len(module)) + "\t\t   0%\t[          ]")
				sys.stdout.flush()			

				# For each package in the list
				for package in packages:
					error = installPackage(package)
					
					# If there is an error
					if error != None:
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
				print("No requirements found for the {} module".format(module))

	# If no modules fond
	else:
		print("No modules found at {}.".format(modulesPath))


if __name__ == "__main__":

	startSetup()