#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PARALLELIZATION
import threading

# DUMPS AND SERIALIZATION
import json

# PHONE SCANNING
from modules.littlebrother.core.searchNumber import searchNumberAPI


#_____FILE_____________________CLASS__
from .CustomEncoder 	import CustomEncoder


class Phone:

	def __init__(self, number):

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