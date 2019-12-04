#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### IMPORTS -----------------------------------------------------------------------------------------------------------------------------------------

import sys, os.path, json, getopt

# Check the current version of Python
if sys.version_info[0] < 3:
    print("Please, use Python 3.")
    # Quit the program
    exit()

from libs.functions import *

# Check if the requirements are up to date and if the spiderfoot server is on
response = input("Have you already start the setup.py program ? [Y/n] : ")

# If the setup script is not running
if response == "n":
	# Quit
	exit()
# If the setup script is already running
else:
	# Clear the shell and go on
	clear()

# Manage arguments
from modules.littlebrother.core.searchInstagram import extractInstagram
from modules.h8mail.api import callh8mail as h8mail
from modules.spiderfoot.api import launchScan

## CONSTANTS --------------------------------------------------------------------------------------

# Load the modules configuration file
modules = loadModules()

## Classes --------------------------------------------------------------------------------------

class Photo:

	url = None
	date = None
	location = None
	path = None
	contents = []

	def __init__(self, url, date, location, path, contents):

		self.url = url
		self.date = date
		self.location = location
		self.path = path
		self.contents = contents

	def export(self, indentation = 0):

		lines = [
			("\t" * indentation) + "Photo {",
			("\t" * indentation) + "\tUrl:\t\t{}".format(self.url if self.url != None else "Unknow"),
			("\t" * indentation) + "\tDate:\t\t{}".format(self.date if self.date != None else "Unknow"),
			("\t" * indentation) + "\tLocation:\t{}".format(self.location if self.location != None else "Unknow"),
			("\t" * indentation) + "\tPath:\t\t{}".format(self.path if self.path != None else "Unknow"),
			("\t" * indentation) + "\tContents:\t{}".format(", ".join(self.contents) if self.contents != None else "Unknow"),
			("\t" * indentation) + "}"
		]

		return "\n".join(lines)

class Account:

	serviceName = None
	serviceCategory = None
	profileLink = None

	def __init__(self, serviceName = None, serviceCategory = None, profileLink = None):

		self.serviceName = serviceName
		self.serviceCategory = serviceCategory
		self.profileLink = profileLink

	def export(self, indentation = 0):

		lines = [
			("\t" * indentation) + "Account {",
			("\t" * indentation) + "\tName:\t\t" + (self.serviceName if self.serviceName != None else "Unknow"),
			("\t" * indentation) + "\tCategory:\t" + (self.serviceCategory if self.serviceCategory != None else "Unknow"),
			("\t" * indentation) + "\tLink:\t\t" + (self.profileLink if self.profileLink != None else "Unknow"),
			("\t" * indentation) + "}"
		]

		return "\n".join(lines)

class InstagramAccount(Account):

	name = None
	username = None
	userId = None
	avatarPath = None
	isPrivate = None
	followersCount = None
	friendsCount = None
	postsCount = None
	description = None
	email = None
	address = None
	phone = None
	photos = []

	def __init__(self, profileLink):

		data = extractInstagram(profileLink, os.path.abspath(os.sep.join(("modules", "littlebrother", "results"))))

		self.name = data["name"]
		self.username = data["username"]
		self.userId = data["id"]
		self.avatarPath = data["profilPhoto"]
		self.isPrivate = data["private"]
		self.followersCount = data["followers"]
		self.friendsCount = data["friends"]
		self.postsCount = data["medias"]
		self.description = data["biography"]
		self.email = data["email"]
		self.address = data["adresse"]
		self.phone = data["phone"]

		for photo in data["photos"]:

			photo["view"] = photo["view"].replace("Image may contain: ", "").replace(" and ", ", ")
			
			url = photo["media"]
			date = photo["date"]
			location = photo["loc"]
			path = photo["path"]
			contents = photo["view"].split(", ")		

			self.photos.append(Photo(url = url, date = date, location = location, path = path, contents = contents))

		Account.__init__(self, serviceName = "Instagram", serviceCategory = "social", profileLink = profileLink)

	def export(self, indentation = 0):

		lines = [
			("\t" * indentation) + "InstagramAccount {",
			("\t" * indentation) + "\tName:\t\t{}".format(self.serviceName if self.serviceName != None else "Unknow"),
			("\t" * indentation) + "\tCategory:\t{}".format(self.serviceCategory if self.serviceCategory != None else "Unknow"),
			("\t" * indentation) + "\tLink:\t\t{}".format(self.profileLink if self.profileLink != None else "Unknow"),
			("\t" * indentation) + "\tUsername:\t{}".format(self.username if self.username != None else "Unknow"),
			("\t" * indentation) + "\tUser ID:\t{}".format(self.userId if self.userId != None else "Unknow"),
			("\t" * indentation) + "\tAvatar path:\t{}".format(self.avatarPath if self.avatarPath != None else "Unknow"),
			("\t" * indentation) + "\tisPrivate:\t{}".format(self.isPrivate if self.isPrivate != None else "Unknow"),
			("\t" * indentation) + "\tFollowers:\t{}".format(self.followersCount if self.followersCount != None else "Unknow"),
			("\t" * indentation) + "\tFriends:\t{}".format(self.friendsCount if self.friendsCount != None else "Unknow"),
			("\t" * indentation) + "\tPosts:\t\t{}".format(self.postsCount if self.postsCount != None else "Unknow"),
			("\t" * indentation) + "\tDescription:\t{}".format(self.description if self.description != None else "Unknow"),
			("\t" * indentation) + "\tEmail:\t\t{}".format(self.email if self.email != None else "Unknow"),
			("\t" * indentation) + "\tAddress:\t{}".format(self.address if self.address != None else "Unknow"),
			("\t" * indentation) + "\tPhone:\t\t{}".format(self.phone if self.phone != None else "Unknow"),
			("\t" * indentation) + "\tPhotos : ["
		]

		lines += [photo.export(indentation +2) for photo in self.photos]

		lines += [
			("\t" * indentation) + "\t]",
			("\t" * indentation) + "}",
		]

		return "\n".join(lines)

	def __repr__(self):
		return self.export()

class Email:

	address = None
	leaks = []

	def scanLeaks(self):

		leaks = h8mail("example@example.com")
		leaks = [leak for leak in leaks if len(leak) == 2]

		leakSource = None
		leakType = None
		leakValue = None

		for leak in leaks:
			(dataType, value) = leak
			if value == "":
				continue
			if dataType == "SCYLLA_SOURCE":
				leakSource = value
			elif dataType == "SCYLLA_PASSWORD" or dataType == "SCYLLA_HASH":
				leakType = str.lower(dataType.replace("SCYLLA_", ""))
				leakValue = value

				self.leaks.append({
					"source": leakSource,
					"type": leakType,
					"value": leakValue
				})


	def export(self, indentation = 0):

		lines = [
			("\t" * indentation) + "Email {",
			("\t" * indentation) + "\taddress:\t" + self.address,
			("\t" * indentation) + "\tleaks: ["
		]

		lines += [("\t" * (indentation +2)) + str(leak) for leak in self.leaks] if len(self.leaks) != 0 else "Unknow"

		lines += [
			("\t" * indentation) + "\t]",
			("\t" * indentation) + "}"
		]

		return "\n".join(lines)


	def __init__(self, address):

		if type(address) is str:
			self.address = address
		else:
			wrongAttrType(self, "address", str, address)

		self.scanLeaks()

	def __repr__(self):

		return self.export()

class Person:

	firstname = None
	middleNames = []
	lastname = None
	usernames = []
	emails = []
	accounts = []

	def addMiddleNames(self, middleNames):

		if type(middleNames) is str:
			middleNames = [middleNames]

		self.middleNames += middleNames


	def addEmails(self, emails):

		if type(emails) is str:
			emails = [emails]

		[self.emails.append(Email(address)) for address in emails]

	def addUsernames(self, usernames):

		if type(usernames) is str:
			usernames = [usernames]

		[self.usernames.append(username) for username in usernames]


	def addAccount(self, account):

		if account.__class__.__name__ not in ("Account", "InstagramAccount"):
			wrongAttrType(self, "account", Account, account)

		else:
			self.accounts.append(account)


	def export(self, indentation = 0):
		
		lines = [
			"PERSON {",
			"\tfirstname:\t" 	+ (self.firstname if self.firstname != None else "Unknow"),
			"\tmiddlenames:\t" 	+ (", ".join(self.middleNames) if len(self.middleNames) != 0 else "Unknow"),
			"\tlastname:\t" 	+ (self.lastname if self.lastname != None else "Unknow"),
			"\temails: ["
		]
		
		lines += [email.export(indentation +2) for email in self.emails]

		lines += [
			"\t]",
			"\tusernames: "		+ (", ".join(self.usernames) if len(self.usernames) != 0 else "Unknow"),
			"\taccounts: ["
		]

		lines += [account.export(indentation +2) for account in self.accounts]

		lines += [
			"\t]",
			"}"
		]

		return "\n".join(lines);

	# Scan the name with spiderfoot
	def scanName(self):
		# Set the firstname and last name as a string
		fullName = "{} {}".format(self.firstname, self.lastname)
		# Format the name
		formatedFullName = '\"{}\"'.format(fullName)
		# Start the spiderfoot module
		results = launchScan(formatedFullName)
		# Scan all the results
		for result in results:
			# If the result is an account
			if result["event_type"] == "ACCOUNT_EXTERNAL_OWNED":
				# Formate results
				result["data"] = result["data"].replace("\n", " ").replace(")", "").split(" ")
				# Delete the useless 'category' keywork
				del(result["data"][1])
				# Get the name of the service
				serviceName = result["data"][0]
				# Get the name of the service
				serviceCategory = result["data"][1]
				# Get the path to the profile
				profileLink = result["data"][2]
				# If it is an Instagram account
				if serviceName == "Instagram":
					# Create the Instagram account
					self.addAccount(InstagramAccount(profileLink = profileLink))
				# If it is another account
				else:
					# Create the new account
					self.addAccount(Account(serviceName = serviceName, serviceCategory = serviceCategory, profileLink = profileLink))
			
			# Else if the result is a username
			elif result["event_type"] == "USERNAME":
				# Add the new username
				self.addUsernames(result["data"])


	def __init__(self, firstname = None, middleNames = None, lastname = None):

		if firstname != None:
			self.firstname = firstname
		
		if middleNames != None:
			self.addMiddleNames(middleNames)
	
		if lastname != None:
			self.lastname = lastname

	# Define a new attribute
	def __setattr__(self, attr, val):
		# If the type of firstname or lastname is string
		if (attr == "firstname" or attr == "lastname") and type(val) is str:
			# Define the new attribute
			object.__setattr__(self, attr, val)
			# If both first and last name are set
			if self.firstname != None and self.lastname != None:
				# Start a scan of the name
				self.scanName()
		# If the attribute type is wrong
		else:
			# Display an error message
			wrongAttrType(self, attr, str, val)

		# If the type of middlenames or emails is not a list
		if (attr == "middleNames" or attr == "emails") and type(val) is not list:
			# Display an error message
			wrongAttrType(self, attr, list, val)

	# Represent the attribute
	def __repr__(self):
		# Return the formated string
		return self.export()

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
		opts, args = getopt.getopt(argv, "hn:", ["help", "name="])
	# If the arguments are invalid
	except:
		# Display an help message
		displayHelp()
		# Exit the script
		fatalError("\"" + " ".join(argv) + "\" are not valid arguments.")

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

			arg = arg.split(" ")

			if len(arg) < 2:
				displayHelp()

			else:
				(firstname, lastname) = arg

				target = Person(firstname = firstname, lastname = lastname)
				target.addEmails("florent.guyon@protonmail.com")

				print(target)

	## PHOTON -----------------------------------------------------------------------------------------

	# If the target type is an URL
#	if targetType == targetType_URL:
#		# Get the return code of the module execution
#		returncode = startModule(modules, "photon", ["--url", targetValue])
#		# If the execution succed
#		if returncode == 0 :
#			# Set the path to the result file
#			filePath = os.sep.join(["modules", "photon", "results", "exported.json"])
#			# Open the result file
#			with open(filePath, "r") as file:
#				# Extract the text		
#				string = file.read()
#				# Load the data as an object
#				json = loads(string)
#				# Save the interesting part of the object
#				result = json['custom']
#				# Print an empty line
#				print("")
#				# For each category of data (email, phone...)
#				for key in result:
#					# If there is at least one result
#					if len(result[key]) > 0 :
#						# Print the count of result
#						print(" " + str(len(result[key])) + " " + key + " found:")
#						# For each result
#						for value in result[key]:
#							# Print the result on a new line
#							print("  - " + value)
#					# If there is no result
#					else :
#						# Print a specific message
#						print(" No " + key + " found.")
#		# If the execution failed
#		else:
#			# Print a warning message
#			warning("The \"photon\" module exits with an error.")
#
#		## H8MAIL && SPIDERFOOT -----------------------------------------------------------------------------------------
#
#		# If the execution of the "photon" module succed
#		if result != None:
#			# If there is emails in the result
#			try:
#				# Save the list of email
#				emails = ",".join(result["email"])		
#			# If there is no emails
#			except:
#				# Print an error message
#				error("The \"email\" dictionary is corrupted.")
#
#			# If the email list saved is not empty
#			if emails != "":
#				# Start the h8mail module with the email list
#				startModule(modules, "h8mail", ["--target", emails])
##				# Start the spiderfoot module with the email list
#				startModule(modules, "spiderfoot", emails)
#			# If the email list is empty
#			else:
##				# Print a warning message
#				warning("No email to scan with the module \"h8mail\".")
#				# Print a warning message
#				warning("No email to scan with the module \"spiderfoot\".")
#
#	# Else if the target type is a name
#	elif targetType == targetType_NAME:
#		# Format the name for the spiderfoot module 
#		name = "\"" + targetValue + "\""
#		# Start the spiderfoot module
#		startModule(modules, "spiderfoot", name)
#
## ------------------------------------------------------------------------------------------------

if __name__ == "__main__":
	# Call the main function with all the arguments except the path to this file
	main(sys.argv[1:])

## ------------------------------------------------------------------------------------------------