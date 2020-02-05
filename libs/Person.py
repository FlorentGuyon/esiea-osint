#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PARALLELIZATION
import threading

# DUMPS AND SERIALIZATION
import json


#_____FILE_____________________CLASS_
from .Phone 			import Phone
from .Email				import Email
from .Website 			import Website
from .Instagram			import Instagram
from .Twitter 			import Twitter
from .Wikipedia			import Wikipedia
from .CustomEncoder 	import CustomEncoder


#_____FILE_____________________FUNCTIONS___________________________RENAME_
from .utils		 		import *
from modules.fpdf.api	import create_pdf 						as pdf


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

		pdf(self, getResultsPath(), getResultsName())