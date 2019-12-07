#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### IMPORTS -----------------------------------------------------------------------------------------------------------------------------------------

import sys, os.path, json, getopt, threading, time

# Check the current version of Python
if sys.version_info[0] < 3:
    print("Please, use Python 3.")
    # Quit the program
    exit()

from libs.functions import *
from libs.fpdf.api import create_pdf

# Check if the requirements are up to date and if the spiderfoot server is on
response = input("Have you already start the setup.py program (in sudo mode) ? [Y/n] : ")

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
from modules.littlebrother.core.leaked import leaked
from modules.littlebrother.core.searchNumber import searchNumberAPI
from modules.h8mail.api import callh8mail as h8mail
from modules.spiderfoot.api import launchScan
from download import download

## CONSTANTS --------------------------------------------------------------------------------------

resultsPath = None

## Classes --------------------------------------------------------------------------------------

class Phone:

	number = None
	deviceType = None
	city = None
	location = None
	provider = None

	def __init__(self, number = number):

		self.number = number
		self.deviceType = None
		self.city = None
		self.location = None
		self.provider = None

		threading.Thread(name = "Phone", target = self.findDetails).start()


	def findDetails(self):

		results = searchNumberAPI(self.number)

		self.deviceType = results["deviceType"]
		self.city = results["city"]
		self.location = results["location"]
		self.provider = results["provider"]


	def export(self, indentation = 0):

		lines = [
			("\t" * indentation) + "PhoneNumber {",
			("\t" * indentation) + "\tNumber:\t\t" + (self.number if self.number != None else "Unknow"),
			("\t" * indentation) + "\tDevice Type:\t" + (self.deviceType if self.deviceType != None else "Unknow"),			
			("\t" * indentation) + "\tCity:\t\t" + (self.city if self.city != None else "Unknow"),
			("\t" * indentation) + "\tLocation:\t" + (self.location if self.location != None else "Unknow"),
			("\t" * indentation) + "\tprovider:\t" + (self.provider if self.provider != None else "Unknow"),
			("\t" * indentation) + "}",
		]

		return "\n".join(lines)


	def __repr__(self):

		return self.export()


class Photo:

	url = None
	name = None
	date = None
	location = None
	path = None
	contents = []


	def __init__(self, url, path, name, date=None, location=None, contents=None):

		self.url = url
		self.name = name
		self.date = date
		self.location = location
		self.path = path
		self.contents = contents

		if self.url != None:
			threading.Thread(name="Photo", target=self.download).start()


	def download(self):

		download(self.url, self.path, self.name)


	def export(self, indentation = 0):

		lines = [
			("\t" * indentation) + "Photo {",
			("\t" * indentation) + "\tUrl:\t\t{}".format(self.url if self.url != None else "Unknow"),
			("\t" * indentation) + "\tName:\t\t{}".format(self.name if self.name != None else "Unknow"),
			("\t" * indentation) + "\tDate:\t\t{}".format(self.date if self.date != None else "Unknow"),
			("\t" * indentation) + "\tLocation:\t{}".format(self.location if self.location != None else "Unknow"),
			("\t" * indentation) + "\tPath:\t\t{}".format(self.path if self.path != None else "Unknow"),
			("\t" * indentation) + "\tContents:\t{}".format(", ".join(self.contents) if self.contents != None else "Unknow"),
			("\t" * indentation) + "}"
		]

		return "\n".join(lines)


	def __repr__(self):

		return self.export()


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
	avatar = None
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

		Account.__init__(self, serviceName = "Instagram", serviceCategory = "social", profileLink = profileLink)

		self.name = None
		self.username = None
		self.userId = None
		self.avatar = None
		self.isPrivate = None
		self.followersCount = None
		self.friendsCount = None
		self.postsCount = None
		self.description = None
		self.email = None
		self.address = None
		self.phone = None
		self.photos = []

		threading.Thread(name="Account", target=self.extractData).start()

	def extractData(self):

		data = extractInstagram(self.profileLink)

		self.name = data["name"]
		self.username = data["username"]
		self.userId = data["id"]
		self.isPrivate = data["private"]
		self.followersCount = data["followers"]
		self.friendsCount = data["friends"]
		self.postsCount = data["medias"]
		self.description = data["biography"]
		self.email = data["email"]
		self.address = data["adresse"]

		if data["phone"] != None:
			self.phone = Phone(data["phone"])

		if data["profilPhoto"] != None:

			path = os.sep.join([resultsPath, "images", "instagram", self.username])
			name = "{}.jpg".format(self.username)
			self.avatar = Photo(url=data["profilPhoto"], path=path, name=name)

		for photo in data["photos"]:

			photo["view"] = photo["view"].replace("Image may contain: ", "").replace(" and ", ", ")
			
			url = photo["media"]
			date = photo["date"]
			location = photo["loc"]
			name = photo["name"]
			contents = photo["view"].split(", ")

			path = os.sep.join([resultsPath, "images", "instagram", self.username, "photos"])		

			self.photos.append(Photo(url=url, date=date, location=location, path=path, name=name, contents=contents))


	def export(self, indentation = 0):

		lines = [
			("\t" * indentation) + "InstagramAccount {",
			("\t" * indentation) + "\tName:\t\t{}".format(self.serviceName if self.serviceName != None else "Unknow"),
			("\t" * indentation) + "\tCategory:\t{}".format(self.serviceCategory if self.serviceCategory != None else "Unknow"),
			("\t" * indentation) + "\tLink:\t\t{}".format(self.profileLink if self.profileLink != None else "Unknow"),
			("\t" * indentation) + "\tUsername:\t{}".format(self.username if self.username != None else "Unknow"),
			("\t" * indentation) + "\tUser ID:\t{}".format(self.userId if self.userId != None else "Unknow"),
			("\t" * indentation) + "\tAvatar path:\t{}".format(str(self.avatar) if self.avatar != None else "Unknow"),
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

class Hash:

	value = None
	protocol = None
	crack = None

	def crackHash(self):

		results = leaked().hash(self.value)

		if results != None:
			(self.crack, self.protocol) = results

	def __init__(self, value, protocol = None, crack = None):

		self.value = value
		self.protocol = protocol
		self.crak = crack

		if self.value != None:
			threading.Thread(name="Hash", target=self.crackHash).start()


	def export(self, indentation = 0):

		lines = [
			("\t" * indentation) + "Hash {",
			("\t" * indentation) + "\tvalue:\t\t" + self.value,
			("\t" * indentation) + "\tprotocol:\t" + (self.protocol if self.protocol != None else "Unknow"),
			("\t" * indentation) + "\tcrack:\t\t" + (self.crack if self.crack != None else "Unknow"),
			("\t" * indentation) + "}"
		]
		
		return "\n".join(lines)

	def __repr__(self):

		return self.export()

class Email:

	address = None
	leaks = []

	def scanLeaks(self):

		results = h8mail(self.address)
		results = [result for result in results if len(result) == 2]

		leakSource = None
		leakType = None
		leakValue = None

		for result in results:

			(dataType, value) = result
			
			if value == "":
				continue
			
			elif dataType == "SCYLLA_SOURCE":
				leakSource = value
			
			elif dataType == "SCYLLA_PASSWORD" or dataType == "SCYLLA_HASH":
				
				if dataType == "SCYLLA_PASSWORD":
					leakValue = value

				else:
					leakValue = Hash(value)

				leakType = str.lower(dataType.replace("SCYLLA_", ""))
				
				self.leaks.append({
					"source": leakSource,
					"type": leakType,
					"value": leakValue
				})

			else:
				error("{} is an unknow data type of email leak.".format(dataType))


	def export(self, indentation = 0):

		lines = [
			("\t" * indentation) + "Email {",
			("\t" * indentation) + "\taddress:\t" + self.address,
			("\t" * indentation) + "\tleaks: ["
		]

		for leak in self.leaks:

			line = ("\t" * (indentation +2)) + "Source: {}, Type: {}, Value: ".format(leak["source"], leak["type"])

			if leak["type"] == "hash":
				line += "\n" + leak["value"].export(indentation +3)
			else:
				line += leak["value"]

			lines += [line]

		lines += [
			("\t" * indentation) + "\t]",
			("\t" * indentation) + "}"
		]

		return "\n".join(lines)


	def __init__(self, address):

		self.address = address
		self.leaks = []

		threading.Thread(name = "Email", target = self.scanLeaks).start()

	def __repr__(self):

		return self.export()

class Person:

	firstname = None
	middlenames = []
	lastname = None
	usernames = []
	emails = []
	accounts = []
	phoneNumbers = []

	def addPhoneNumbers(self, phoneNumbers):

		if type(phoneNumbers) is str:
			phoneNumbers = [phoneNumbers]

		[self.phoneNumbers.append(Phone(phoneNumber)) for phoneNumber in phoneNumbers]
		

	def addMiddleNames(self, middlenames):

		if type(middlenames) is str:
			middlenames = [middlenames]

		self.middlenames += middlenames


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
			"\tFirstname:\t" 	+ (self.firstname if self.firstname != None else "Unknow"),
			"\tMiddlenames:\t" 	+ (", ".join(self.middlenames) if len(self.middlenames) != 0 else "Unknow"),
			"\tLastname:\t" 	+ (self.lastname if self.lastname != None else "Unknow"),
			"\tEmails: ["
		]
		
		lines += [email.export(indentation +2) for email in self.emails]

		lines += [
			"\t]",
			"\tUsernames: "		+ (", ".join(self.usernames) if len(self.usernames) != 0 else "Unknow"),
			"\tAccounts: ["
		]

		lines += [account.export(indentation +2) for account in self.accounts]

		lines += [
			"\t]",
			"\tPhone numbers: ["
		]

		lines += [phoneNumber.export(indentation +2) for phoneNumber in self.phoneNumbers]

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


	def __init__(self, firstname = None, middlenames = None, lastname = None):

		self.firstname = firstname
		self.lastname = lastname
		self.usernames = []
		self.emails = []
		self.accounts = []
		self.phoneNumbers = []

		if middlenames != None:
			self.addMiddleNames(middlenames)


		if self.firstname != None and self.lastname != None:

			threading.Thread(name="Person", target=self.scanName).start()


	# Represent the attribute
	def __repr__(self):
		# Return the formated string
		return self.export()


### MAIN --------------------------------------------------------------------------------------------------------------------------------------------

stop = False
threadTypes = ["Person", "Email", "Hash", "Phone", "Account", "Photo"]

def displayStats():

	previousThreadCount = -1

	while stop != True:
		
		threadCount = len(threading.enumerate())
		sys.stdout.flush()
		
		if threadCount != previousThreadCount:

			previousThreadCount = threadCount

			threadClasses = [thread.name for thread in threading.enumerate()]

			lines = [
				"",
				"  Analysing...",
				"",
			]

			lines += ["    ■ {}\t  {}\t| {}".format(threadType, threadClasses.count(threadType), "■" * threadClasses.count(threadType)) for threadType in threadTypes]

			clear()
			print("\n".join(lines))
			time.sleep(0.1)

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

				global resultsPath
				resultsPath = os.sep.join([os.path.dirname(os.path.abspath(__file__)), "results", "{} {}".format(firstname, lastname)])

				display = threading.Thread(target = displayStats)
				display.start()

				target = Person(firstname = firstname, lastname = lastname)
				#target.addAccount(InstagramAccount("https://www.instagram.com/_where_to_travel_"))
				#target.addAccount(InstagramAccount("https://www.instagram.com/_grayrabbit"))
				#target.addAccount(Account(serviceName="Youtube", serviceCategory="video", profileLink="www.yt.com"))

				while len([thread for thread in threading.enumerate() if thread.name in threadTypes]) > 0:
					[thread.join() for thread in threading.enumerate() if thread.name in threadTypes]

				time.sleep(0.2)

				global stop
				stop = True

				display.join()

				#print(target)
				create_pdf(target, resultsPath)


if __name__ == "__main__":

	# Call the main function with all the arguments except the path to this file
	main(sys.argv[1:])

## ------------------------------------------------------------------------------------------------
#	--threads=1, --level=2, --keys, --regex, "{\"email\": \"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-]+\", \"phone number\": \"\\(?\\+?[0-9]{1,4}\\)?[1-9] [0-9]{2} [0-9]{2} [0-9]{2} [0-9]{2}\"}"