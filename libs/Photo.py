#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# OS CALLS
import os

# PARALLELIZATION
import threading

# DUMPS AND SERIALIZATION
import json

# WEB DONWLOADING
from download import download

# UTILS
from libs.functions import doesThisURLExist, isFile


#_____FILE_____________________CLASS__
from .CustomEncoder 	import CustomEncoder


class Photo:

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
				self.protocol = value.lower()

		if (self.protocol == None) and (self.url != None):
			self.protocol = self.url.split("?")[0].split(".").pop().lower()

		if (self.protocol != None) and (self.protocol not in ["png", "jpg", "jpeg", "gif", "svg", "ico"]):
			self.protocol = None

		if (self.path != None) and (self.name != None) and (self.protocol != None):
			self.fullPath = os.sep.join([self.path, "{}.{}".format(self.name, self.protocol)])

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