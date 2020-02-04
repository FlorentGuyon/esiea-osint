#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# OS CALLS
import os

# DUMPS AND SERIALIZATION
import json

# PARALLELIZATION
import threading

# WEB REQUESTS
import requests

# HTML PARSING
from bs4 import BeautifulSoup as bs


#_____FILE_____________________CLASS__
from .Website 			import Website
from .Photo			 	import Photo
from .CustomEncoder 	import CustomEncoder

#_____FILE_________________FUNCTIONS_____
from libs.config 	import getResultsPath


class Wikipedia(Website):

	def __init__(self, username):

		self.text = None

		url = "https://fr.wikipedia.org/wiki/{}".format(username)

		Website.__init__(self, name = "Wikipedia", category = "culture", url = url, username = username, defaultExtraction = False)

		self.extractData()
		

	def extractData(self):

		page = self.getPage()
		self.extractText(page)
		self.extractImages(page)


	def extractText(self, page):

		# Remove all the unwanted texts (example: Edit button)
		[tag.decompose() for tag in page.select(".mw-editsection, .toc, .reference, .need_ref_tag, .mw-cite-backlink, .bandeau-niveau-detail, .bandeau-portail, small, sup, style, .API.nowrap, a.external.text")]			

		# Select only the interesting part
		paragraphs = page.select("p")

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


	def extractImages(self, page):
		
		images = page.select("img")
		
		# KEEP ONLY THE IMAGES NAMED WITH THE USERNAME
		#filteredImages = list(filter(lambda image: image["src"].find(username) != -1, images))
		
		for index, image in enumerate(images):
			
			imageName = "{}_{}".format(self.username, index)
			imageURL = "https:{}".format(image["src"])

			imageContents = None
			imageWidth = None
			imageHeight = None

			if (image.has_attr("alt")) and (image["alt"] != ""):
				imageContents = image["alt"] 			

			if image.has_attr("width"):
				imageWidth = image["width"]

			if image.has_attr("height"):
				imageHeight = image["height"]
						
			self.images.append(Photo(name = imageName, url = imageURL, path = self.imagesPath, contents = imageContents, width = imageWidth, height = imageHeight))


	def __repr__(self):

		return json.dumps(self.__dict__, indent=4, separators=(',', ': '), cls=CustomEncoder)