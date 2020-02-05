#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PARALLELIZATION
import threading

# WEB REQUESTS
import requests

# DUMPS AND SERIALIZATION
import json

# OS CALLS
import os

# TIME MANIPULATION
import time

# HTML PARSING
from bs4 import BeautifulSoup as bs

# CHARTS CREATION
import pygooglechart

# WEB DONWLOADING
from download import download


#_____FILE_____________________CLASS___
from .Photo	 			import Photo
from .CustomEncoder 	import CustomEncoder


#_____FILE_________________FUNCTIONS_____________
from .utils		 	import isFile, getResultsPath


class Website:

	def __init__(self, name, category = None, url = None, username = None, defaultExtraction = True):

		self.name = name
		self.category = category
		self.url = url
		self.username = username
		self.qrcode = None
		self.images = []
		self.imagesPath = os.sep.join([getResultsPath(), self.name])

		if self.username != None:
			self.imagesPath = os.sep.join([self.imagesPath, self.username])

		if not os.path.exists(self.imagesPath):
			os.makedirs(self.imagesPath)

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


	def getPage(self):

		page = requests.get(self.url).content.decode('utf-8')
		return bs(page, 'lxml')


	def extractData(self):

		page = self.getPage()
		self.extractImages(page)


	def extractImages(self, page):

		images = page.select("img")

		for index, image in enumerate(images):
			if image.has_attr("src"):
						
				imageUrl = image["src"].split("?")[0]

				if imageUrl[:4] != "http":
					imageUrl = self.url + imageUrl
				
				imageProtocol = imageUrl.split(".").pop()
				imageName = "{}_{}".format(self.username, index)
				
				imageContents = None
				imageWidth = None
				imageHeight = None

				if (image.has_attr("alt")) and (image["alt"] != ""):
					imageContents = image["alt"] 			

				if image.has_attr("width"):
					imageWidth = image["width"]

				if image.has_attr("height"):
					imageHeight = image["height"]
				
				self.images.append(Photo(url=imageUrl, name=imageName, path=self.imagesPath, contents=imageContents, protocol=imageProtocol, width=imageWidth, height=imageHeight))


	def __repr__(self):

		return json.dumps(self.__dict__, indent=4, separators=(',', ': '), cls=CustomEncoder)