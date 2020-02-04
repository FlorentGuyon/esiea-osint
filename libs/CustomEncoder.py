#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# DATE MANIPULATION
import datetime

# DUMPS AND SERIALIZATION
import json


class CustomEncoder(json.JSONEncoder):

	def default(self, complexObject):

		if isinstance(complexObject, datetime.datetime):
			return complexObject.replace(microsecond=0).isoformat()

		return {complexObject.__class__.__name__: complexObject.__dict__}