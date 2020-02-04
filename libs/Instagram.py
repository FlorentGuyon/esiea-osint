#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PARALLELIZATION
import threading

# DUMPS AND SERIALIZATION
import json

# OS CALLS
import os

# INSTAGRAM SCANNING
from modules.littlebrother.core.searchInstagram import extractInstagram

#_____FILE_____________________CLASS___
from .Website 	 		import Website
from .Phone	 			import Phone
from .Email	 			import Email
from .Photo  			import Photo
from .CustomEncoder 	import CustomEncoder

#_____FILE_________________FUNCTIONS_____
from libs.config 	import getResultsPath


class Instagram(Website):

	def __init__(self, username = None, url = None):

		if (username != None) & (url == None):
			url = "https://www.instagram.com/" + username

		Website.__init__(self, name = "Instagram", category = "social", url = url, username = username, defaultExtraction = False)

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

		threading.Thread(name="Website", target=self.extractData).start()

	def extractData(self):

		data = extractInstagram(self.url)

		if data["username"] == None:
			return

		self.name = data["name"]
		self.username = data["username"]
		self.userId = data["id"]
		self.isPrivate = data["private"]
		self.followersCount = int(data["followers"])
		self.friendsCount = int(data["friends"])
		self.postsCount = int(data["medias"])
		self.description = data["biography"]
		self.address = data["adresse"]

		if data["email"] != None:
			self.email = Email(address = data["email"])

		if data["phone"] != None:
			self.phone = Phone(data["phone"])

		self.imagesPath = os.sep.join([getResultsPath(), "Instagram", self.username, "posts"])

		if not os.path.exists(self.imagesPath):
			os.makedirs(self.imagesPath)

		if data["profilPhoto"] != None:

			path = os.sep.join([self.imagesPath, ".."])
			self.avatar = Photo(url=data["profilPhoto"], path=path, name=self.username, protocol="jpg")

		for photo in data["photos"]:

			photo["view"] = photo["view"].replace("Image may contain: ", "").replace(" and ", ", ")
			
			url = photo["media"]
			date = photo["date"]
			location = photo["loc"]
			name = photo["name"]
			contents = photo["view"] if photo["view"] != "" else None

			self.images.append(Photo(url=url, date=date, location=location, path=self.imagesPath, name=name, contents=contents, protocol="jpg"))		


	def __repr__(self):

		return json.dumps(self.__dict__, indent=4, separators=(',', ': '), cls=CustomEncoder)