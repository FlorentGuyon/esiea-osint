#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# USER INTERFACE WIDGET MANIPULATION
from tkinter import *

# FONT MANIPULATION
from tkinter.font import Font

# JPEG/JPG, PNG IMAGE TYPE MANIPULATION
from PIL import ImageTk, Image

# OS CALLS
import os

# TIME MANIUPULATION
import time

# PARALLELIZATION
import threading


#____FILE__________________CLASS_
from libs.Person 	import Person


#____FILE__________________FUNCTIONS__________________________________
from setup			import getModules, getRequirements, installPackage
from libs.utils		import *


class UserInterface(Tk):

	def __init__(self):

		title = "OSINT Scanner"

		Tk.__init__(self, title)

		self.title(title)
		self.geometry("1280x720")
		self.update()

		self.fonts = {
			"tiny": {
				"normal": Font(family="Helvetica", size=8),
				"italic": Font(family="Helvetica", size=8, slant="italic")
			},
			"normal": {
				"normal": Font(family="Helvetica", size=12),
				"italic": Font(family="Helvetica", size=12, slant="italic")
			},
			"large": {
				"normal": Font(family="Helvetica", size=16),
				"italic": Font(family="Helvetica", size=16, slant="italic")
			},
			"extrem": {
				"normal": Font(family="Helvetica", size=20),
				"italic": Font(family="Helvetica", size=20, slant="italic")
			}
		}

		self.initialData = {
			"Firstname": None,
			"Middlenames" : [],
			"Lastname": None,
			"Usernames" : [],
			"Emails" : [],
			"Phones" : []
		}
		self.initialDataIndex = 0

		self.addBackground(self, "mainBackground.png")
		

	def start(self):

		self.defaultWindow()
		self.mainloop()


	def clearWindow(self):

		for widget in self.winfo_children()[1:]:
			widget.destroy()


	def getImage(self, imageName):

		imagePath = os.sep.join([os.path.dirname(os.path.abspath(__file__)), "ressources", imageName])
		image = ImageTk.PhotoImage(Image.open(imagePath))

		return image


	def addBackground(self, parent, imageName):

		backgroundImage = self.getImage(imageName)
		
		canvas = Canvas(self, width=parent.winfo_width(), height=parent.winfo_height())
		canvas.create_image(parent.winfo_width(), parent.winfo_height(), image=backgroundImage)
		canvas.keepAlive = backgroundImage
		canvas.pack(fill=BOTH, expand=1)


	def createButton(self, parent, command, text=None, textvariable=None, image=None, background="#192024", bordermode=INSIDE, relx=0, rely=0, relwidth=1.0, relheight=1.0, fontSize="normal", fontStyle="normal"):

		if text != None:
			button = Button(parent, text=text, relief=FLAT, activeforeground="white", fg="white", activebackground=background, bg=background, bd=0, justify=CENTER, command=command, font=self.fonts[fontSize][fontStyle])
		elif textvariable != None:
			button = Button(parent, textvariable=textvariable, relief=FLAT, activeforeground="white", fg="white", activebackground=background, bg=background, bd=0, justify=CENTER, command=command, font=self.fonts[fontSize][fontStyle])
		elif image != None:
			imageObject = self.getImage(image)
			button = Button(parent, relief=FLAT, image=imageObject, activebackground=background, bg=background, bd=0, command=command)
			button.keepAlive = imageObject
		button.pack()
		button.place(bordermode=bordermode, relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)

		return button


	def createEntry(self, parent, textvariable, background="#192024", bordermode=INSIDE, relx=0, rely=0, relwidth=1.0, relheight=1.0, fontSize="normal", fontStyle="normal"):

		entry = Entry(parent, textvariable=textvariable, relief=FLAT, fg="white", bg=background, bd=0, justify=CENTER, font=self.fonts[fontSize][fontStyle])
		entry.pack()
		entry.place(bordermode=bordermode, relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)

		return entry


	def createLabel(self, parent, text=None, textvariable=None, background="#192024", bordermode=INSIDE, relx=0, rely=0, relwidth=1.0, relheight=1.0, fontSize="normal", fontStyle="normal"):

		if text != None:
			label = Label(parent, text=text, relief=FLAT, fg="white", bg=background, bd=0, justify=CENTER, font=self.fonts[fontSize][fontStyle])
		elif textvariable != None:
			label = Label(parent, textvariable=textvariable, relief=FLAT, fg="white", bg=background, bd=0, justify=CENTER, font=self.fonts[fontSize][fontStyle])
		label.pack()
		label.place(bordermode=bordermode, relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)

		return label


	def createFrame(self, relwidth, relheight, parent=None, background="#192024", relx=None, rely=None):

		if parent == None:
			parent = self

		width = self.winfo_width() * relwidth
		height = self.winfo_height() * relheight

		if relx == None:
			relx = 0.5 - (relwidth / 2)
	
		if rely == None:
			rely = 0.5 - (relheight / 2)

		frame = Frame(parent, bg=background, bd=0, relief=FLAT)
		frame.pack()
		frame.place(bordermode=INSIDE, relx=relx, rely=rely, width=width, height=height)

		return frame


	def defaultWindow(self):

		frame = self.createFrame(0.2, 0.4)

		self.setupStatus = StringVar()
		self.setupStatus.set("Install requirements")

		self.createButton(parent=frame, text="START", command=self.getInitialData, relheight=0.8, fontSize="large")
		self.createButton(parent=frame, textvariable=self.setupStatus, command=self.setupWindow, rely=0.8, relheight=0.2, fontSize="tiny", fontStyle="italic")		


	def setupWindow(self):

		modulesList = getModules()

		# If there at least one module
		if len(modulesList) > 0:
			packages = []
			# For each module in the list
			for module in modulesList:
				packages += getRequirements(module)
			
			packageCount = len(packages)

			if packageCount > 0:					
				self.setupStatus.set("Install requirements (0%)")
				self.update()

				# For each package in the list
				for packageIndex, package in enumerate(packages):
					installPackage(package)
					progress = int((packageIndex +1) * 100 / packageCount)
					self.setupStatus.set("Install requirements ({}%)".format(progress))
					self.update()


	def getInitialData(self):

		self.clearWindow()

		frame = self.createFrame(0.2, 0.4)

		self.askInitialData(frame, list(self.initialData.keys())[self.initialDataIndex])


	def decreaseInitialDataIndex(self):

		if self.initialDataIndex > 0:
			self.initialDataIndex -= 1
		self.getInitialData()


	def increaseInitialDataIndex(self):

		if (self.initialDataIndex +1) < len(self.initialData):
			self.initialDataIndex += 1
		self.getInitialData()


	def addInitialData(self):

		title = list(self.initialData.keys())[self.initialDataIndex]

		if len(self.initialData[title]) < 3:
			self.initialData[title].append(StringVar())
			self.getInitialData()
		

	def askInitialData(self, parent, title):

		self.createLabel(parent, text=title, relheight=0.5)

		if type(self.initialData[title]) == list:
			if len(self.initialData[title]) == 0:
				self.initialData[title].append(StringVar())
			
			for index, textVariable in enumerate(self.initialData[title]):
				self.createEntry(parent, textvariable=textVariable, background="#171d21", relwidth=0.75, relheight=0.1, relx=0.125, rely=0.4 + (index * 0.125))
			
			if len(self.initialData[title]) < 3:
				self.createButton(parent, image="plus.png", command=self.addInitialData, relwidth=0.2, relheight=0.1, relx=0.7, rely=0.275)

		else:
			if self.initialData[title] == None:
				newTextVarialble = StringVar()
				self.initialData[title] = newTextVarialble
			else:
				newTextVarialble = self.initialData[title]
			self.createEntry(parent, textvariable=newTextVarialble, background="#171d21", relwidth=0.75, relheight=0.1, relx=0.125, rely=0.5)

		
		if self.initialDataIndex > 0:
			self.createButton(parent, image="left.png", command=self.decreaseInitialDataIndex, relwidth=0.2, relheight=0.1, rely=0.85)
		
		if (self.initialDataIndex +1) < len(self.initialData):
			self.createButton(parent, image="right.png", command=self.increaseInitialDataIndex, relwidth=0.2, relheight=0.1, rely=0.85, relx=0.8)
		else:
			self.createButton(parent, image="ok.png", command=self.scanWindow, relwidth=0.2, relheight=0.1, rely=0.85, relx=0.8)


	def scanWindow(self):

		self.clearWindow()
		
		frame = self.createFrame(0.2, 0.4)

		self.createButton(parent=frame, text="Scan now", command=self.startScan, relheight=0.8, fontSize="large")
		self.createLabel(parent=frame, text="When complete, check the results folder", rely=0.8, relheight=0.2, fontSize="tiny", fontStyle="italic")		


	def startScan(self):

		self.formatedInitialData = {}

		for key, value in self.initialData.items():

			if (type(value).__name__ == "StringVar") and (value.get() != ""):
				self.formatedInitialData[key.lower()] = value.get()

			elif type(value) == list:
				formatedValue = [stringvar.get() for stringvar in value if stringvar.get() != ""]
				
				if len(formatedValue) != 0:
					self.formatedInitialData[key.lower()] = formatedValue

		self.initialData = {
			"Firstname": None,
			"Middlenames" : [],
			"Lastname": None,
			"Usernames" : [],
			"Emails" : [],
			"Phones" : []
		}
		
		self.initialDataIndex = 0

		setResultsValues(self.formatedInitialData)

		target = Person(**self.formatedInitialData)

		waitEndOfScans()

		# EXPORT THE RESULTS AS A PDF FILE
		target.pdfExport()

		# EXPORT THE RESULTS AS A JSON FILE
		target.jsonExport()

		self.clearWindow()
		
		frame = self.createFrame(0.2, 0.4)

		self.createButton(parent=frame, text="New scan", command=self.getInitialData, relheight=0.8, fontSize="large")
		self.createButton(parent=frame, text="QUIT", command=self.quit, rely=0.8, relheight=0.2, fontSize="tiny", fontStyle="italic")		