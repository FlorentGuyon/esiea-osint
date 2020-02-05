#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PARALLELIZATION
import threading

# DUMPS AND SERIALIZATION
import json

# UTILS
from libs.functions import *

# NAME SCANNING
from modules.spiderfoot.api import launchScan


#_____FILE_____________________CLASS_
from .Phone 			import Phone
from .Email				import Email
from .Website 			import Website
from .Instagram			import Instagram
from .Twitter 			import Twitter
from .Wikipedia			import Wikipedia
from .CustomEncoder 	import CustomEncoder


#_____FILE_____________________FUNCTIONS_____________________
from libs.config 		import getResultsPath, getResultsName
from libs.fpdf.api 		import create_pdf


class Person:

	def __init__(self, **kwargs):

		self.firstname = None
		self.lastname = None
		self.middlenames = []
		self.usernames = []
		self.websites = []
		self.emails = []
		self.phones = []

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
				self.addPhones(value)

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

	def addPhones(self, phones):

		if type(phones) is str:
			phones = [phones]

		for number in phones:
			if number not in [savedPhone.number for savedPhone in self.phones]:
				self.phones.append(Phone(number))


	def addEmails(self, emails):

		if type(emails) is str:
			emails = [emails]

		[self.emails.append(Email(address)) for address in emails if address not in self.emails]


	def addUsernames(self, usernames):
		
		if type(usernames) is str:
			usernames = [usernames]

		usernames = [username for username in usernames if username not in self.usernames]

		self.usernames += usernames

		for username in usernames:
			threading.Thread(name="Username", target=self.scanUsernames, args=[username]).start()


	def addWebsite(self, website):

		if website.__class__.__name__ not in ("Website", "Instagram", "Twitter", "Wikipedia"):
			wrongAttrType(self, "website", Website, website)

		elif website.__class__.__name__ == "Website":
			self.websites.append(website)

		else:
			self.websites.insert(0, website)


	# Scan the name with spiderfoot: NOT USED
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
				name = result["data"][0]
				# Get the name of the service
				category = result["data"][1]
				# Get the path to the profile
				url = result["data"][2]

				if url[-1] == "/":
					url = url[0:-1]

				username = url.split("/").pop()

				if (url not in [website.url for website in self.websites]) and (doesThisURLExist(url)):
					# If it is an Instagram account
					if name == "Instagram":
						# Create the Instagram account
						self.addWebsite(Instagram(username = username, url = url))
					# If it is another account
					else:
						# Create the new account
						self.addWebsite(Website(username = username, name = name, category = category, url = url))
			
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
				self.addWebsite(Website(name = kwargs["website"]["name"], url = kwargs["website"]["link"], username = kwargs["website"]["username"]))


	def scanUsernames(self, *args):

		username = args[0]
		websites = fromUsernameToWebsites(username)

		for website in websites:
			website["username"] = username
			if website["link"] not in [website.url for website in self.websites]:
				threading.Thread(name="URL", target=self.verifyWebsite, kwargs={"website": website}).start()


	def __repr__(self):

		return json.dumps(self.__dict__, indent=4, separators=(',', ': '), cls=CustomEncoder)


	def jsonExport(self):

		exportFile = os.sep.join([getResultsPath(), "results.json"])

		with open(exportFile, "w", encoding="utf-8") as file:
			file.write(str(self))


	def pdfExport(self):

		create_pdf(self, getResultsPath(), getResultsName())