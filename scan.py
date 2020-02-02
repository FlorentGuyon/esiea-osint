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
#response = input("Have you already start the setup.py program (in sudo mode) ? [Y/n] : ")

# If the setup script is not running
#if response not in ["", "y", "Y"]:
	# Quit
#	exit()
# If the setup script is already running
#else:
	# Clear the shell and go on
#	clear()

from modules.littlebrother.core.searchInstagram import extractInstagram
from modules.littlebrother.core.leaked import leaked
from modules.littlebrother.core.searchNumber import searchNumberAPI
from modules.h8mail.api import callh8mail as h8mail
from modules.spiderfoot.api import launchScan
from download import download

## CONSTANTS --------------------------------------------------------------------------------------

resultsPath = None

## Classes --------------------------------------------------------------------------------------

class CustomEncoder(json.JSONEncoder):

	def default(self, complexObject):

		if isinstance(complexObject, datetime.datetime):
			return complexObject.replace(microsecond=0).isoformat()

		return {complexObject.__class__.__name__: complexObject.__dict__}


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


	def __repr__(self):

		return json.dumps(self.__dict__, indent=4, separators=(',', ': '), cls=CustomEncoder)


class Photo:

	url = None
	name = None
	date = None
	location = None
	protocol = None
	path = None
	fullPath = None
	contents = []
	isDownloaded = None
	width = None
	height = None


	def __init__(self, **kwargs):

		self.url = None
		self.name = None
		self.date = None
		self.location = None
		self.path = None
		self.fullPath = None
		self.contents = []
		self.isDownloaded = False
		self.width = None
		self.height = None
		self.protocol = None

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
				if value != None:
					if value is not list:
						value = [value]
					self.contents = value
			elif key == "width":
				self.width = value
			elif key == "height":
				self.height = value
			elif key == "protocol":
				self.protocol = value

		if (self.protocol == None) and (self.url != None):
			protocol = self.url.split("?")[0].split(".").pop().lower()
			if len(protocol) <= 4:
				self.protocol = protocol

		if (self.path != None) and (self.name != None) and (self.protocol != None):
			self.fullPath = os.sep.join([self.path, "{}.{}".format(self.name, self.protocol)])

		if self.date == None:
			self.date = datetime.datetime.now()

		if self.url != None:
			threading.Thread(name="Photo", target=self.download).start()


	def download(self):

		if self.fullPath != None:
			if not isFile(self.fullPath):

				if doesThisURLExist(self.url):
					try:
						download(url = self.url, path = self.fullPath, verbose=False, progressbar=False)
					except:
						pass

					if isFile(self.fullPath):
						self.isDownloaded = True
			else:
				self.isDownloaded = True


	def __repr__(self):

		return json.dumps(self.__dict__, indent=4, separators=(',', ': '), cls=CustomEncoder)


class Website:

	serviceName = None
	serviceCategory = None
	url = None
	qrcode = None
	username = None
	images = []
	imagesPath = None

	def __init__(self, serviceName, serviceCategory = None, url = None, username = None, defaultExtraction = True):

		self.serviceName = serviceName
		self.serviceCategory = serviceCategory
		self.url = url
		self.username = username
		self.qrcode = None
		self.images = []
		self.imagesPath = os.sep.join([resultsPath, serviceName])

		if username != None:
			self.imagesPath = os.sep.join([self.imagesPath, username])

		currentTries = 0
		maxTries = 3

		if url != None:

			qrSideSize = 75
			self.qrcode = Photo(name="qrcode", path=self.imagesPath, width=qrSideSize, height=qrSideSize, protocol="png")

			while (not self.qrcode.isDownloaded) and (currentTries < maxTries):

				if not os.path.exists(self.qrcode.path):
					os.makedirs(self.qrcode.path)

				chart = pygooglechart.QRChart(qrSideSize, qrSideSize)
				chart.add_data(self.url)
				chart.set_ec('H', 0)

				try:
					chart.download(self.qrcode.fullPath)
				except:
					time.sleep(1)

				currentTries += 1

				if isFile(self.qrcode.fullPath):
					self.qrcode.isDownloaded = True


			if defaultExtraction:
				threading.Thread(name="Website", target=self.extractData).start()


	def extractData(self):

		page = requests.get(self.url).content.decode('utf-8')

		# Parse the content as lxml
		soup = bs(page, 'lxml')

		images = soup.select("img")

		for index, image in enumerate(images):
			if image.has_attr("src"):
				
				imageUrl = image["src"].split("?")[0]

				if imageUrl[:4] != "http":
					imageUrl = self.url + imageUrl
				
				imageType = imageUrl.split(".").pop()

				if len(imageType) > 4:
					imageType = None

				imageName = "{}_{}".format(self.username, index)
				imageContents = image["alt"] if (image.has_attr("alt")) and (image["alt"] != "") else None
				
				self.images.append(Photo(url=imageUrl, name=imageName, path=self.imagesPath, contents=imageContents, protocol=imageType))


	def __repr__(self):

		return json.dumps(self.__dict__, indent=4, separators=(',', ': '), cls=CustomEncoder)


class Instagram(Website):

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


	def __init__(self, username = None, url = None):

		if (username != None) & (url == None):
			url = "https://www.instagram.com/" + username

		Website.__init__(self, serviceName = "Instagram", serviceCategory = "social", url = url, username = username, defaultExtraction = False)

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

		threading.Thread(name="Website", target=self.extractData).start()

	def extractData(self):

		data = extractInstagram(self.url)

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

		if data["phone"] != None:
			self.phone = Phone(data["phone"])

		photosPath = os.sep.join([resultsPath, "Instagram", self.username, "posts"])

		if not os.path.exists(photosPath):
			os.makedirs(photosPath)

		if data["profilPhoto"] != None:

			path = os.sep.join([photosPath, ".."])
			self.avatar = Photo(url=data["profilPhoto"], path=path, name=self.username, protocol="jpg")

		for photo in data["photos"]:

			photo["view"] = photo["view"].replace("Image may contain: ", "").replace(" and ", ", ")
			
			url = photo["media"]
			date = photo["date"]
			location = photo["loc"]
			name = photo["name"]
			contents = photo["view"] if photo["view"] != "" else None

			self.photos.append(Photo(url=url, date=date, location=location, path=photosPath, name=name, contents=contents, protocol="jpg"))		


	def __repr__(self):

		return json.dumps(self.__dict__, indent=4, separators=(',', ': '), cls=CustomEncoder)


class Twitter(Website):

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

		url = "https://www.twitter.com/" + username

		Website.__init__(self, serviceName = "Twitter", serviceCategory = "social", url = url, username = username, defaultExtraction = False)

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

		threading.Thread(name="Website", target=self.extractData).start()


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
		
		twitterResultsPath = os.sep.join([resultsPath, "Twitter", self.username])
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


			imageWidth = 600
			imageHeight = 150

			self.tweetsChart = Photo(name="tweets", protocol="png", path=twitterResultsPath, width=imageWidth, height=imageHeight)

			maxValue = max(tweets_count)
			
			chart = pygooglechart.SimpleLineChart(imageWidth, imageHeight, "Tweets", y_range=(0, maxValue))
			chart.set_colours(['3F51B5'])
			chart.add_data(tweets_count)
			chart.set_axis_labels(pygooglechart.Axis.BOTTOM, datetime)

			try:
				chart.download(self.tweetsChart.fullPath)
			except:
				pass

			if isFile(self.tweetsChart.fullPath):
				self.tweetsChart.isDownloaded = True


			imageWidth = 600
			imageHeight = 150

			self.repliesChart = Photo(name="replies", protocol="png", path=twitterResultsPath, width=imageWidth, height=imageHeight)

			maxValue = max(replies_count)
			
			chart = pygooglechart.SimpleLineChart(imageWidth, imageHeight, "Replies", y_range=(0, maxValue))
			chart.set_colours(['2196F3'])
			chart.add_data(replies_count)
			chart.set_axis_labels(pygooglechart.Axis.BOTTOM, datetime)

			try:
				chart.download(self.repliesChart.fullPath)
			except:
				pass

			if isFile(self.repliesChart.fullPath):
				self.repliesChart.isDownloaded = True


			imageWidth = 600
			imageHeight = 150

			self.retweetsChart = Photo(name="retweets", protocol="png", path=twitterResultsPath, width=imageWidth, height=imageHeight)

			maxValue = max(retweets_count)
			
			chart = pygooglechart.SimpleLineChart(imageWidth, imageHeight, "Retweets", y_range=(0, maxValue))
			chart.set_colours(['00BCD4'])
			chart.add_data(retweets_count)
			chart.set_axis_labels(pygooglechart.Axis.BOTTOM, datetime)

			try:
				chart.download(self.retweetsChart.fullPath)
			except:
				pass

			if isFile(self.retweetsChart.fullPath):
				self.retweetsChart.isDownloaded = True


			imageWidth = 600
			imageHeight = 150

			self.likesChart = Photo(name="likes", protocol="png", path=twitterResultsPath, width=imageWidth, height=imageHeight)

			maxValue = max(likes_count)
			
			chart = pygooglechart.SimpleLineChart(imageWidth, imageHeight, "Likes", y_range=(0, maxValue))
			chart.set_colours(['009688'])
			chart.add_data(likes_count)
			chart.set_axis_labels(pygooglechart.Axis.BOTTOM, datetime)
			
			try:
				chart.download(self.likesChart.fullPath)
			except:
				pass

			if isFile(self.likesChart.fullPath):
				self.likesChart.isDownloaded = True


			imageWidth = 600
			imageHeight = 200

			self.hoursChart = Photo(name="hours", protocol="png", path=twitterResultsPath, width=imageWidth, height=imageHeight)
		
			maxValue = max(hours)
			
			chart = pygooglechart.GroupedVerticalBarChart(imageWidth, imageHeight, "Posting hours", y_range=(0, maxValue))
			chart.set_bar_width(15)
			chart.set_colours(['F57C00'])
			chart.add_data(hours)
			chart.set_axis_labels(pygooglechart.Axis.BOTTOM, ["00h", "01h", "02h", "03h", "04h", "05h", "06h", "07h", "08h", "09h", "10h", "11h", "12h", "13h", "14h", "15h", "16h", "17h", "18h", "19h", "20h", "21h", "22h", "23h"])

			try:
				chart.download(self.hoursChart.fullPath)
			except:
				pass

			if isFile(self.hoursChart.fullPath):
				self.hoursChart.isDownloaded = True


			if filteredWords != "":

				imageWidth = 600
				imageHeight = 900

				self.wordcloud = Photo(name="wordcloud", protocol="png", path=twitterResultsPath, width=imageWidth, height=imageHeight)

				try:
					result = subprocess.run(["wordcloud_cli", "--text", wordsPath, "--imagefile", self.wordcloud.fullPath, "--contour_color", "white", "--width", str(imageWidth), "--height", str(imageHeight), "--background", "white"])
				except:
					pass

				if isFile(self.wordcloud.fullPath):
					self.wordcloud.isDownloaded = True


	def __repr__(self):

		return json.dumps(self.__dict__, indent=4, separators=(',', ': '), cls=CustomEncoder)


class Hash:

	value = None
	protocol = None
	clear = None

	def crackHash(self):

		results = leaked().hash(self.value)

		if results != None:
			(self.clear, self.protocol) = results

	def __init__(self, value, protocol = None, clear = None):

		self.value = value
		self.protocol = protocol
		self.clear = clear

		if self.value != None:
			threading.Thread(name="Hash", target=self.crackHash).start()


	def __repr__(self):

		return json.dumps(self.__dict__, indent=4, separators=(',', ': '), cls=CustomEncoder)


class Wikipedia(Website):

	images = []
	text = None


	def __init__(self, username):

		self.images = []
		self.text = None

		url = "https://fr.wikipedia.org/wiki/{}".format(username)

		Website.__init__(self, serviceName = "Wikipedia", serviceCategory = "culture", url = url, username = username, defaultExtraction = False)

		page = requests.get(url).content.decode('utf-8')

		# Parse the content as lxml
		soup = bs(page, 'lxml')

		# Remove all the unwanted texts (example: Edit button)
		tagsToRemove = soup.select(".mw-editsection, .toc, .reference, .need_ref_tag, .mw-cite-backlink, .bandeau-niveau-detail, .bandeau-portail, small, sup, style, .API.nowrap, a.external.text")

		# For all the found tags
		for tag in tagsToRemove:
			# Delete it
			tag.decompose()

		# Select only the interesting part
		paragraphs = soup.select("p")

		if len(paragraphs) != 0:

			self.text = ""

			for paragraph in paragraphs:

				# If it is a comment, ignore it
				if type(paragraph).__name__ == "Comment":
					continue

				# If it is a string
				if type(paragraph).__name__ == "NavigableString":
					# Remove an invisible char and print it
					self.text += paragraph.replace("‎", "")

				# Else if it is an object
				else:
					# Remove an invisible char and print the object text
					self.text += paragraph.text.replace("‎", "")


		imagePath = os.sep.join([resultsPath, self.serviceName, self.username])

		if not os.path.exists(imagePath):
			os.makedirs(imagePath)

		images = soup.select("img")
		filteredImages = list(filter(lambda image: image["src"].find(username) != -1, images))
		
		for index, image in enumerate(filteredImages):
			
			imageType = image["src"].split(".").pop()
			imageName = "{}_{}.{}".format(self.username, index, imageType)
			imageURL = "https:{}".format(image["src"])
			
			imageContents = None
			imageWidth = None
			imageHeight = None
			
			if image["alt"] != "":
				imageContents = image["alt"]

			if image["width"] != None:
				imageWidth = int(image["width"])

			if image["height"] != None:
				imageHeight = int(image["height"])
			
			self.images.append(Photo(name = imageName, url = imageURL, path = imagePath, contents = imageContents, width = imageWidth, height = imageHeight))


	def __repr__(self):

		return json.dumps(self.__dict__, indent=4, separators=(',', ': '), cls=CustomEncoder)


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


	def __init__(self, address):

		self.address = address
		self.leaks = []

		threading.Thread(name = "Email", target = self.scanLeaks).start()


	def __repr__(self):

		return json.dumps(self.__dict__, indent=4, separators=(',', ': '), cls=CustomEncoder)


class Person:

	firstname = None
	middlenames = []
	lastname = None
	usernames = []
	emails = []
	website = []
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


	def addWebsite(self, website):

		if website.__class__.__name__ not in ("Website", "Instagram", "Twitter", "Wikipedia"):
			wrongAttrType(self, "website", Website, website)

		elif website.__class__.__name__ == "Website":
			self.websites.append(website)

		else:
			self.websites.insert(0, website)


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
				result["data"] = result["data"].replace("\n", "e ").replace(")", "").split(" ")
				# Delete the useless 'category' keywork
				del(result["data"][1])
				# Get the name of the service
				serviceName = result["data"][0]
				# Get the name of the service
				serviceCategory = result["data"][1]
				# Get the path to the profile
				url = result["data"][2]

				if url[-1] == "/":
					url = url[0:-1]

				username = url.split("/").pop()

				if (url not in [website.url for website in self.websites]) and (doesThisURLExist(url)):
					# If it is an Instagram account
					if serviceName == "Instagram":
						# Create the Instagram account
						self.addWebsite(Instagram(username = username, url = url))
					# If it is another account
					else:
						# Create the new account
						self.addWebsite(Website(username = username, serviceName = serviceName, serviceCategory = serviceCategory, url = url))
			
			# Else if the result is a username
			elif result["event_type"] == "USERNAME":
				# Add the new username
				self.addUsernames(result["data"])


	def verifyWebsite(self, **kwargs):

		if doesThisURLExist(kwargs["website"]["link"]):
			if kwargs["website"]["name"] == "Instagram":
				self.addWebsite(Instagram(username = kwargs["website"]["username"]))
			elif kwargs["website"]["name"] == "Twitter":
				self.addWebsite(Twitter(username = kwargs["website"]["username"]))
			elif kwargs["website"]["name"] == "Wikipedia":
				self.addWebsite(Wikipedia(username = kwargs["website"]["username"]))
			else:
				self.addWebsite(Website(serviceName = kwargs["website"]["name"], url = kwargs["website"]["link"], username = kwargs["website"]["username"]))


	def scanUsername(self, **kwargs):

		websites = fromUsernameToWebsites(kwargs["username"])

		for website in websites:
			website["username"] = kwargs["username"]
			if website["link"] not in [website.url for website in self.websites]:
				threading.Thread(name="URL", target=self.verifyWebsite, kwargs={"website": website}).start()


	def __init__(self, **kwargs):

		self.firstname = None
		self.lastname = None
		self.middlenames = []
		self.usernames = []
		self.websites = []
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

			wikipediaFirstname = self.firstname.title().replace(" ", "-")
			wikipediaLastname = self.lastname.title().replace(" ", "-")
			wikipediaUsername = "{}_{}".format(wikipediaFirstname, wikipediaLastname)

			website = {
				"link" : "https://fr.wikipedia.org/wiki/{}".format(wikipediaUsername),
				"name" : "Wikipedia",
				"username" : wikipediaUsername
			}

			threading.Thread(name="URL", target=self.verifyWebsite, kwargs={"website": website}).start()

			compactFirstname = self.firstname.lower().replace(" ", "")
			compactLastname = self.lastname.lower().replace(" ", "")

			self.addUsernames([
				"{}{}".format(compactFirstname, compactLastname),
				"{}{}".format(compactLastname, compactFirstname),
			])

			# Spiderfoot is very slow and the results are almost all wrong
			#threading.Thread(name="Person", target=self.scanName).start()

	def __repr__(self):

		return json.dumps(self.__dict__, indent=4, cls=CustomEncoder)


	def export(self):

		exportFile = os.sep.join([resultsPath, "results.json"])

		with open(exportFile, "w", encoding="utf-8") as file:
			file.write(str(self))


### MAIN --------------------------------------------------------------------------------------------------------------------------------------------

stop = False
threadTypes = ["Person", "Email", "Hash", "Phone", "Website", "Photo", "Username", "URL"]

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
		identity += data["firstname"].title()

	if "middlename" in data.keys(): 
		if identity != "":
			identity += " "
		identity += " ".join(data["middlename"].title())

	if "lastname" in data.keys():
		if identity != "":
			identity += " "
		identity += data["lastname"].title()

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

	target.export()
	create_pdf(target, resultsPath, identity)


if __name__ == "__main__":

	# Call the main function with all the arguments except the path to this file
	main(sys.argv[1:])

## ------------------------------------------------------------------------------------------------