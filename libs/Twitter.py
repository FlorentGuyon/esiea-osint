#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# OS CALLS
import os

# PARALLELIZATION
import threading

# TWITTER SCANNING
import twint

# SUBSTRING RESEARCH
import re

# STRING OCCURENCE COUNTING
import collections

# DUMPS AND SERIALIZATION
import json

# CHARTS CREATION
import pygooglechart

#_____FILE_____________________CLASS___
from .Website 	 		import Website
from .Photo			 	import Photo
from .CustomEncoder 	import CustomEncoder

#_____FILE_____________________FUNCTIONS_____________
from .utils 			import isFile, getResultsPath


class Twitter(Website):

	def __init__(self, username):

		url = "https://www.twitter.com/" + username

		Website.__init__(self, name = "Twitter", category = "social", url = url, username = username, defaultExtraction = False)

		twintPath = os.sep.join([getResultsPath(), self.name, self.username])

		if not os.path.exists(twintPath):
			os.makedirs(twintPath)

		self.userId = None
		self.isPrivate = None
		self.tweetsPath = os.sep.join([twintPath, "tweets.json"])
		self.tweetsChart = None
		self.repliesChart = None
		self.retweetsChart = None
		self.likesChart = None
		self.hoursChart = None
		self.wordcloud = None

		threading.Thread(name="Website", target=self.extractData).start()


	def extractData(self):

		c = twint.Config()
		c.Username = self.username
		c.Store_json = True
		c.Output = self.tweetsPath
		c.Resume = os.sep.join([getResultsPath(), self.name, self.username, "resume.txt"])
		c.Hide_output = True

		try:
			twint.run.Search(c)
		except:
			return

		self.extractText()
		self.createCharts()	


	def extractText(self):

		if isFile(self.tweetsPath):
			self.isPrivate = False
			with open(self.tweetsPath, "r", encoding="utf-8") as tweets:
				for tweet in tweets:
					tweet = json.loads(tweet)
					self.userid = tweet["user_id"]
					break
		else:
			self.isPrivate = True


	def createCharts(self):

		datetime, tweets_count, replies_count, retweets_count, likes_count = [], [], [], [], []
		
		words = ""
		data = {}
		hours = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

		if isFile(self.tweetsPath):

			with open(self.tweetsPath, "r", encoding="utf-8") as tweets:
				
				for tweet in tweets:
					tweet = json.loads(tweet)
					hour = int(tweet["time"].split(":")[0])
					hours[hour] += 1

					year, month, day = tweet["date"].split("-")
					key = "-".join([year, month])

					if key not in data:
						data[key] = {"datetime": key, "tweets_count": 0, "replies_count": 0, "retweets_count": 0, "likes_count": 0}

					data[key]["tweets_count"] += 1
					data[key]["replies_count"] += tweet["replies_count"]
					data[key]["retweets_count"] += tweet["retweets_count"]
					data[key]["likes_count"] += tweet["likes_count"]

					match = re.findall(r"[#\-êçûéèààa-zA-Z]{6,}", tweet["tweet"])

					if match != None:
						words += " " + " ".join(match)

			occurences = dict(collections.Counter(words.split(" ")))
			filteredWords = " ".join([key for key, value in occurences.items() if value > 7])
			wordsPath = os.sep.join([self.imagesPath, "words.txt"])

			with open(wordsPath, 'w'): pass
			with open(wordsPath, "w", encoding="utf-8") as file:
				file.write(filteredWords)

			for key in data:
				year, month = key.split("-")

				if year not in datetime:
					datetime.insert(0, year)
			
				tweets_count.insert(0, data[key]["tweets_count"])
				replies_count.insert(0, data[key]["replies_count"])
				retweets_count.insert(0, data[key]["retweets_count"])
				likes_count.insert(0, data[key]["likes_count"])


			imageWidth = 600
			imageHeight = 150

			self.tweetsChart = Photo(name="tweets", protocol="png", path=self.imagesPath, width=imageWidth, height=imageHeight)

			maxValue = max(tweets_count)
			
			chart = pygooglechart.SimpleLineChart(imageWidth, imageHeight, "Tweets", y_range=(0, maxValue))
			chart.set_colours(['3F51B5'])
			chart.add_data(tweets_count)
			chart.set_axis_labels(pygooglechart.Axis.BOTTOM, datetime)

			try:
				chart.download(self.tweetsChart.fullPath)
			except:
				pass

			if isFile(self.tweetsChart.fullPath):
				self.tweetsChart.isDownloaded = True


			imageWidth = 600
			imageHeight = 150

			self.repliesChart = Photo(name="replies", protocol="png", path=self.imagesPath, width=imageWidth, height=imageHeight)

			maxValue = max(replies_count)
			
			chart = pygooglechart.SimpleLineChart(imageWidth, imageHeight, "Replies", y_range=(0, maxValue))
			chart.set_colours(['2196F3'])
			chart.add_data(replies_count)
			chart.set_axis_labels(pygooglechart.Axis.BOTTOM, datetime)

			try:
				chart.download(self.repliesChart.fullPath)
			except:
				pass

			if isFile(self.repliesChart.fullPath):
				self.repliesChart.isDownloaded = True


			imageWidth = 600
			imageHeight = 150

			self.retweetsChart = Photo(name="retweets", protocol="png", path=self.imagesPath, width=imageWidth, height=imageHeight)

			maxValue = max(retweets_count)
			
			chart = pygooglechart.SimpleLineChart(imageWidth, imageHeight, "Retweets", y_range=(0, maxValue))
			chart.set_colours(['00BCD4'])
			chart.add_data(retweets_count)
			chart.set_axis_labels(pygooglechart.Axis.BOTTOM, datetime)

			try:
				chart.download(self.retweetsChart.fullPath)
			except:
				pass

			if isFile(self.retweetsChart.fullPath):
				self.retweetsChart.isDownloaded = True


			imageWidth = 600
			imageHeight = 150

			self.likesChart = Photo(name="likes", protocol="png", path=self.imagesPath, width=imageWidth, height=imageHeight)

			maxValue = max(likes_count)
			
			chart = pygooglechart.SimpleLineChart(imageWidth, imageHeight, "Likes", y_range=(0, maxValue))
			chart.set_colours(['009688'])
			chart.add_data(likes_count)
			chart.set_axis_labels(pygooglechart.Axis.BOTTOM, datetime)
			
			try:
				chart.download(self.likesChart.fullPath)
			except:
				pass

			if isFile(self.likesChart.fullPath):
				self.likesChart.isDownloaded = True


			imageWidth = 600
			imageHeight = 200

			self.hoursChart = Photo(name="hours", protocol="png", path=self.imagesPath, width=imageWidth, height=imageHeight)
		
			maxValue = max(hours)
			
			chart = pygooglechart.GroupedVerticalBarChart(imageWidth, imageHeight, "Posting hours", y_range=(0, maxValue))
			chart.set_bar_width(15)
			chart.set_colours(['F57C00'])
			chart.add_data(hours)
			chart.set_axis_labels(pygooglechart.Axis.BOTTOM, ["00h", "01h", "02h", "03h", "04h", "05h", "06h", "07h", "08h", "09h", "10h", "11h", "12h", "13h", "14h", "15h", "16h", "17h", "18h", "19h", "20h", "21h", "22h", "23h"])

			try:
				chart.download(self.hoursChart.fullPath)
			except:
				pass

			if isFile(self.hoursChart.fullPath):
				self.hoursChart.isDownloaded = True


			if filteredWords != "":

				imageWidth = 600
				imageHeight = 900

				self.wordcloud = Photo(name="wordcloud", protocol="png", path=self.imagesPath, width=imageWidth, height=imageHeight)

				try:
					result = subprocess.run(["wordcloud_cli", "--text", wordsPath, "--imagefile", self.wordcloud.fullPath, "--contour_color", "white", "--width", str(imageWidth), "--height", str(imageHeight), "--background", "white"])
				except:
					pass

				if isFile(self.wordcloud.fullPath):
					self.wordcloud.isDownloaded = True


	def __repr__(self):

		return json.dumps(self.__dict__, indent=4, separators=(',', ': '), cls=CustomEncoder)