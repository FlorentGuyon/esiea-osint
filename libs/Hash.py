#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PARALLELIZATION
import threading

# DUMPS AND SERIALIZATION
import json

# HASH SCANNING
from modules.littlebrother.core.leaked import leaked


#_____FILE_____________________CLASS__
from .CustomEncoder 	import CustomEncoder


class Hash:

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