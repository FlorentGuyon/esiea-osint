#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# DUMPS AND SERIALIZATION
import json

# PARALLELIZATION
import threading

# EMAIL SCANNING
from modules.h8mail.api import callh8mail as h8mail

#_____FILE_____________________CLASS___
from .Hash 	 			import Hash
from .CustomEncoder 	import CustomEncoder


class Email:

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

		if self.address != None:
			threading.Thread(name = "Email", target = self.scanLeaks).start()


	def __repr__(self):

		return json.dumps(self.__dict__, indent=4, separators=(',', ': '), cls=CustomEncoder)