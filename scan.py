#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### IMPORTS -----------------------------------------------------------------------------------------------------------------------------------------

import sys, os.path, json, getopt, threading, time, datetime, asyncio, twint, collections, pygooglechart, re, requests

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
if response not in ["", "y", "Y"]:
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
	country = None
	location = None

	def __init__(self, number = number):

		self.number = number
		self.deviceType = None
		self.country = None
		self.location = None

		threading.Thread(name = "Phone", target = self.findDetails).start()


	def findDetails(self):

		results = searchNumberAPI(self.number)

		self.deviceType = results["deviceType"]
		self.country = results["country"]
		self.location = results["location"]


	def export(self, indentation = 0):

		lines = [
			("\t" * indentation) + "PhoneNumber {",
			("\t" * indentation) + "\tNumber:\t\t" + (self.number if self.number != None else "Unknow"),
			("\t" * indentation) + "\tDevice Type:\t" + (self.deviceType if self.deviceType != None else "Unknow"),			
			("\t" * indentation) + "\tCountry:\t" + (self.country if self.country != None else "Unknow"),
			("\t" * indentation) + "\tLocation:\t" + (self.location if self.location != None else "Unknow"),
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


	def __init__(self, **kwargs):

		self.url = None
		self.name = None
		self.date = None
		self.location = None
		self.path = None
		self.contents = []

		for key, value in kwargs.items():
			if key == "url":
				self.url = value
			elif key == "name":
				self.name = value
			elif key == "date":
				self.date = value
			elif key == "location":
				self.location = value
			elif key == "path":
				self.path = value
			elif key == "contents":
				self.contents = value

		if self.date == None:
			self.date = datetime.datetime.now()

		if self.url != None:
			threading.Thread(name="Photo", target=self.download).start()


	def download(self):

		download(url = self.url, path = os.sep.join([self.path, self.name]), verbose=False, progressbar=False)


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
	qrcode = None
	username = None

	def __init__(self, serviceName, serviceCategory = None, profileLink = None, username = None):

		self.serviceName = serviceName
		self.serviceCategory = serviceCategory
		self.profileLink = profileLink
		self.username = username
		self.qrcode = None

		if profileLink != None:
			while self.qrcode == None:

				qrPath = os.sep.join([resultsPath, serviceName])  

				if username != None:
					qrPath = os.sep.join([qrPath, username])
				else:
					print(serviceName)
					break

				self.qrcode = Photo(name="qrcode.png", path=qrPath)

				if not os.path.exists(self.qrcode.path):
					os.makedirs(self.qrcode.path)

				chart = pygooglechart.QRChart(75, 75)
				chart.add_data(self.profileLink)
				chart.set_ec('H', 0)

				try:
					chart.download(os.sep.join([self.qrcode.path, self.qrcode.name]))
				except:
					time.sleep(1)
					self.qrcode = None



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


	def __init__(self, username = None, profileLink = None):

		if (username != None) & (profileLink == None):
			profileLink = "https://www.instagram.com/" + username

		Account.__init__(self, serviceName = "Instagram", serviceCategory = "social", profileLink = profileLink, username = username)

		self.name = None
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

		if data["username"] == None:
			return

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

		print(self.description)

		if data["phone"] != None:
			self.phone = Phone(data["phone"])

		photosPath = os.sep.join([resultsPath, "Instagram", self.username, "posts"])

		if not os.path.exists(photosPath):
			os.makedirs(photosPath)

		if data["profilPhoto"] != None:

			path = os.sep.join([photosPath, ".."])
			name = "{}.jpg".format(self.username)
			self.avatar = Photo(url=data["profilPhoto"], path=path, name=name)

		for photo in data["photos"]:

			photo["view"] = photo["view"].replace("Image may contain: ", "").replace(" and ", ", ")
			
			url = photo["media"]
			date = photo["date"]
			location = photo["loc"]
			name = photo["name"]
			contents = photo["view"].split(", ")

			self.photos.append(Photo(url=url, date=date, location=location, path=photosPath, name=name, contents=contents))


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


class TwitterAccount(Account):

	userId = None
	isPrivate = None
	tweetsPath = None
	tweetsChart = None
	repliesChart = None
	retweetsChart = None
	likesChart = None
	hoursChart = None
	wordcloud = None


	def __init__(self, username):

		profileLink = "https://www.twitter.com/" + username

		Account.__init__(self, serviceName = "Twitter", serviceCategory = "social", profileLink = profileLink, username = username)

		twintPath = os.sep.join([resultsPath, "twitter", self.username])

		if not os.path.exists(twintPath):
			os.makedirs(twintPath)

		self.userId = None
		self.isPrivate = None
		self.tweetsPath = os.sep.join([twintPath, "tweets.json"])
		self.tweetsChart = None
		self.repliesChart = None
		self.retweetsChart = None
		self.likesChart = None
		self.hoursChart = None
		self.wordcloud = None

		threading.Thread(name="Account", target=self.extractData).start()


	def extractData(self):

		asyncio.set_event_loop(asyncio.new_event_loop())

		c = twint.Config()
		c.Username = self.username
		c.Store_json = True
		c.Output = self.tweetsPath
		c.Resume = os.sep.join([resultsPath, "twitter", self.username, "resume.txt"])
		c.Hide_output = True

		twint.run.Search(c)

		if isFile(self.tweetsPath):
			self.isPrivate = False
			with open(self.tweetsPath, "r", encoding="utf-8") as tweets:
				for tweet in tweets:
					tweet = json.loads(tweet)
					self.userid = tweet["user_id"]
					break
		else:
			self.isPrivate = True

		self.createCharts()


	def createCharts(self):

		datetime, tweets_count, replies_count, retweets_count, likes_count = [], [], [], [], []
		
		twitterResultsPath = os.sep.join([resultsPath, "twitter", self.username])
		words = ""
		data = {}
		hours = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

		if isFile(self.tweetsPath):

			with open(self.tweetsPath, "r", encoding="utf-8") as tweets:
				
				for tweet in tweets:
					tweet = json.loads(tweet)
					hour = int(tweet["time"].split(":")[0])
					hours[hour] += 1

					year, month, day = tweet["date"].split("-")
					key = "-".join([year, month])

					if key not in data:
						data[key] = {"datetime": key, "tweets_count": 0, "replies_count": 0, "retweets_count": 0, "likes_count": 0}

					data[key]["tweets_count"] += 1
					data[key]["replies_count"] += tweet["replies_count"]
					data[key]["retweets_count"] += tweet["retweets_count"]
					data[key]["likes_count"] += tweet["likes_count"]

					match = re.findall(r"[#\-êçûéèààa-zA-Z]{6,}", tweet["tweet"])

					if match != None:
						words += " " + " ".join(match)

			occurences = dict(collections.Counter(words.split(" ")))
			filteredWords = " ".join([key for key, value in occurences.items() if value > 7])
			wordsPath = os.sep.join([resultsPath, "twitter", self.username, "words.txt"])

			with open(wordsPath, 'w'): pass
			with open(wordsPath, "w", encoding="utf-8") as file:
				file.write(filteredWords)

			for key in data:
				year, month = key.split("-")

				if year not in datetime:
					datetime.insert(0, year)
			
				tweets_count.insert(0, data[key]["tweets_count"])
				replies_count.insert(0, data[key]["replies_count"])
				retweets_count.insert(0, data[key]["retweets_count"])
				likes_count.insert(0, data[key]["likes_count"])

			try:
				self.tweetsChart = Photo(name="tweets.png", path=twitterResultsPath)

				maxValue = max(tweets_count)
				chartPath = os.sep.join([self.tweetsChart.path, self.tweetsChart.name])

				chart = pygooglechart.SimpleLineChart(600, 150, "Tweets", y_range=(0, maxValue))
				chart.set_colours(['3F51B5'])
				chart.add_data(tweets_count)
				chart.set_axis_labels(pygooglechart.Axis.BOTTOM, datetime)
				chart.download(chartPath)

			except:
				self.tweetsChart = None

			try:
				self.repliesChart = Photo(name="replies.png", path=twitterResultsPath)

				maxValue = max(replies_count)
				chartPath = os.sep.join([self.repliesChart.path, self.repliesChart.name])

				chart = pygooglechart.SimpleLineChart(600, 150, "Replies", y_range=(0, maxValue))
				chart.set_colours(['2196F3'])
				chart.add_data(replies_count)
				chart.set_axis_labels(pygooglechart.Axis.BOTTOM, datetime)
				chart.download(chartPath)

			except:
				self.repliesChart = None

			try:
				self.retweetsChart = Photo(name="retweets.png", path=twitterResultsPath)

				maxValue = max(retweets_count)
				chartPath = os.sep.join([self.retweetsChart.path, self.retweetsChart.name])

				chart = pygooglechart.SimpleLineChart(600, 150, "Retweets", y_range=(0, maxValue))
				chart.set_colours(['00BCD4'])
				chart.add_data(retweets_count)
				chart.set_axis_labels(pygooglechart.Axis.BOTTOM, datetime)
				chart.download(chartPath)

			except:
				self.retweetsChart = None

			try:
				self.likesChart = Photo(name="likes.png", path=twitterResultsPath)

				maxValue = max(likes_count)
				chartPath = os.sep.join([self.likesChart.path, self.likesChart.name])

				chart = pygooglechart.SimpleLineChart(600, 150, "Likes", y_range=(0, maxValue))
				chart.set_colours(['009688'])
				chart.add_data(likes_count)
				chart.set_axis_labels(pygooglechart.Axis.BOTTOM, datetime)
				chart.download(chartPath)
			
			except:
				self.likesChart = None

			try:
				self.hoursChart = Photo(name="hours.png", path=twitterResultsPath)

				maxValue = max(hours)
				chartPath = os.sep.join([self.hoursChart.path, self.hoursChart.name])

				chart = pygooglechart.GroupedVerticalBarChart(600, 200, "Posting hours", y_range=(0, maxValue))
				chart.set_bar_width(15)
				chart.set_colours(['F57C00'])
				chart.add_data(hours)
				chart.set_axis_labels(pygooglechart.Axis.BOTTOM, ["00h", "01h", "02h", "03h", "04h", "05h", "06h", "07h", "08h", "09h", "10h", "11h", "12h", "13h", "14h", "15h", "16h", "17h", "18h", "19h", "20h", "21h", "22h", "23h"])
				chart.download(chartPath)

			except:
				self.hoursChart = None

			if filteredWords != "":
				self.wordcloud = Photo(name="wordcloud.png", path=twitterResultsPath)
				chartPath = os.sep.join([self.wordcloud.path, self.wordcloud.name])

				result = subprocess.run(["wordcloud_cli", "--text", wordsPath, "--imagefile", chartPath, "--contour_color", "white", "--width", "600", "--height", "900", "--background", "white"])


	def __repr__(self):
		return str(self.__dict__)


	def __str__(self):
		return str(self.__dict__)


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

	def addPhoneNumbers(self, newPhoneNumbers):

		if type(newPhoneNumbers) is str:
			newPhoneNumbers = [newPhoneNumbers]

		for newNumber in newPhoneNumbers:
			if newNumber not in [phone.number for phone in self.phoneNumbers]:
				self.phoneNumbers.append(Phone(newNumber))


	def addEmails(self, emails):

		if type(emails) is str:
			emails = [emails]

		[self.emails.append(Email(address)) for address in emails if address not in self.emails]

	def addUsernames(self, usernames):
		
		if type(usernames) is str:
			usernames = [usernames]

		for username in usernames:
			if username not in self.usernames:
				self.usernames.append(username) 
				threading.Thread(name="Username", target=self.scanUsername, kwargs={"username": username}).start()


	def addAccount(self, account):

		if account.__class__.__name__ not in ("Account", "InstagramAccount", "TwitterAccount"):
			wrongAttrType(self, "account", Account, account)

		elif account.__class__.__name__ == "Account":
			self.accounts.append(account)

		else:
			self.accounts.insert(0, account)



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

				if profileLink[-1] == "/":
					profileLink = profileLink[0:-1]

				username = profileLink.split("/").pop()

				if (profileLink not in [account.profileLink for account in self.accounts]) and (doesThisURLExist(profileLink)):
					# If it is an Instagram account
					if serviceName == "Instagram":
						# Create the Instagram account
						self.addAccount(InstagramAccount(username = username, profileLink = profileLink))
					# If it is another account
					else:
						# Create the new account
						self.addAccount(Account(username = username, serviceName = serviceName, serviceCategory = serviceCategory, profileLink = profileLink))
			
			# Else if the result is a username
			elif result["event_type"] == "USERNAME":
				# Add the new username
				self.addUsernames(result["data"])


	def verifyAccount(self, **kwargs):

		if doesThisURLExist(kwargs["account"]["link"]):
			if kwargs["account"]["name"] == "Instagram":
				self.addAccount(InstagramAccount(username = kwargs["account"]["username"]))
			elif kwargs["account"]["name"] == "Twitter":
				self.addAccount(TwitterAccount(username = kwargs["account"]["username"]))
			else:
				self.addAccount(Account(serviceName = kwargs["account"]["name"], profileLink = kwargs["account"]["link"], username = kwargs["account"]["username"]))


	def scanUsername(self, **kwargs):

		accounts = fromUsernameToAccounts(kwargs["username"])

		for account in accounts:
			account["username"] = kwargs["username"]
			if account["link"] not in [account.profileLink for account in self.accounts]:
				threading.Thread(name="URL", target=self.verifyAccount, kwargs={"account": account}).start()


	def __init__(self, **kwargs):

		self.firstname = None
		self.lastname = None
		self.middlenames = []
		self.usernames = []
		self.accounts = []
		self.emails = []
		self.phoneNumbers = []

		for key, value in kwargs.items():

			if key == "firstname":
				self.firstname = value

			elif key == "middlename":
				self.middlenames = value

			elif key == "lastname":
				self.lastname = value

			elif key == "username":
				self.addUsernames(value)

			elif key == "email":
				self.addEmails(value)

			elif key == "phone":
				self.addPhoneNumbers(value)

		if self.firstname != None and self.lastname != None:

			compactFirstname = self.firstname.lower().replace(" ", "")
			compactLastname = self.lastname.lower().replace(" ", "")

			self.addUsernames([
				"{}{}".format(compactFirstname, compactLastname),
				"{}{}".format(compactLastname, compactFirstname),
			])
			# Spiderfoot is very slow and the results are almost all wrong
			#threading.Thread(name="Person", target=self.scanName).start()


	# Represent the attribute
	def __repr__(self):
		# Return the formated string
		return self.export()


### MAIN --------------------------------------------------------------------------------------------------------------------------------------------

stop = False
threadTypes = ["Person", "Email", "Hash", "Phone", "Account", "Photo", "Username", "URL"]

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

			#clear()
			print("\n".join(lines))
			time.sleep(0.1)

# Display an help message
def displayHelp():
	# Lines of the message
	lines = [
		"",
		"  ╔════════════════════╗",
		"  ║ DO YOU NEED HELP ? ║",
		"  ╠════════════════════╩═══════════════════════════════════════════════════════════════════════╗",
		"  ║ Enter your arguments as follows:                                                           ║",
		"  ║                                                                                            ║",
		"  ║   ■ -h                                  or --help                                          ║",
		'  ║   ■ -f "<firstname>"                    or --firstname="<firstname>"                       ║',
		'  ║   ■ -l "<lastname>"                     or --lastname="<lastname>"                         ║',
		'  ║   ■ -m "<middlename1>,<middlename2>..." or --middlename="<middlename1>,<middlename2>..."   ║',
		'  ║   ■ -u "<username1>,<username2>..."     or --username="<username1>,<username2>..."         ║',
		'  ║   ■ -e "<email1>,<email2>..."           or --email="<email1>,<email2>..."                  ║',
		'  ║   ■ -p "<phone1>,<phone2>..."           or --phone="<phone1>,<phone2>..."                  ║',
		"  ║                                                                                            ║",
		"  ╚════════════════════════════════════════════════════════════════════════════════════════════╝"
	]
	# Print the final message
	print("\n".join(lines))

# First function called
def main(argv):

	# Test if the arguments are valid
	try:
		# Extract the arguments following this options
		opts, args = getopt.getopt(argv, "hf:l:e:m:p:u:", ["help", "firstname=", "lastname=", "email=", "middlename=", "phone=", "username="])
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

	data = {}

	# For all arguments
	for opt, arg in opts:
		
		# If the argument is about help
		if opt in ("-h", "--help"):
			displayHelp()
			quit()

		else:
			
			opt = opt.replace("-", "")

			key = None

			if len(opt) == 1:
				if opt == "f": key = "firstname"
				elif opt == "l": key = "lastname"
				elif opt == "m": key = "middlename"
				elif opt == "u": key = "username"
				elif opt == "e": key = "email"
				elif opt == "p": key = "phone"

			else:
				key = opt

			if (key not in ["firstname", "lastname", "middlename"]) & (arg.count(" ") > 0):
				print("Error: Unauthorized spaces, please use commas as separator for {} list.".format(key))
				quit()


			if key in ["firstname", "lastname"]:
				data[key] = arg.strip()

			else:
				arg = arg.split(",")
				for value in arg:
					if value != "":
						if key not in data.keys():
							data[key] = []
						data[key].append(value.strip())
					else:
						print("Warning: {} list is empty.".format(key)) 


	identity = ""

	if "firstname" in data.keys():
		identity += data["firstname"]

	if "middlename" in data.keys(): 
		if identity != "":
			identity += " "
		identity += " ".join(data["middlename"])

	if "lastname" in data.keys():
		if identity != "":
			identity += " "
		identity += data["lastname"]

	for nameSource in ["username", "email", "phone", "twitter", "instagram"]:
		if identity == "":
			if nameSource in data.keys(): 
				identity += data[nameSource][0]
				break

	if identity == "":
		identity += datetime.datetime.now().strftime("%d %B %Y %Hh%M %Ss")

	global resultsPath
	resultsPath = os.sep.join([os.path.dirname(os.path.abspath(__file__)), "results", identity])
	display = threading.Thread(target = displayStats)
	display.start()

	from modules.photon.photon import main as photon

	target = Person(**data)

	while len([thread for thread in threading.enumerate() if thread.name in threadTypes]) > 0:
		[thread.join() for thread in threading.enumerate() if thread.name in threadTypes]

	time.sleep(0.2)

	global stop
	stop = True

	display.join()

	print(target)
	create_pdf(target, resultsPath, identity)


if __name__ == "__main__":

	# Call the main function with all the arguments except the path to this file
	main(sys.argv[1:])

## ------------------------------------------------------------------------------------------------
#python "ESIEA\5A\PST5 - OSINT\POC\scan.py" -t "KerriganNuNue"