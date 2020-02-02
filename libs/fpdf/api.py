#coding: utf-8

from __future__ import unicode_literals

import os

from . import FPDF


pageWidth = 210
pageHeight = 297

leftMargin = 10
rightMargin = 10
topMargin = 10
bottomMargin = 10

areaWidth = pageWidth - (leftMargin + rightMargin)
areaHeight = pageHeight - (topMargin + bottomMargin)

fontFamily = "DejaVu"

filePath = os.path.dirname(os.path.abspath(__file__))

lineHeight = 5
indentationWidth = 10

fontSize = {
	
	"tiny": 10,
	"normal": 12,
	"large": 14,
	"veryLarge": 18,
	"veryVeryLarge": 24
}


def newChapter(title, subtitle):

	pdf.add_page()
	newLine(20)
	pdf.set_font(fontFamily, size=fontSize["veryVeryLarge"])
	pdf.multi_cell(0, 10, txt=title, align="C")
	pdf.set_font(fontFamily, 'B', size=fontSize["large"])
	pdf.multi_cell(0, 5, txt=subtitle, align="C")
	pdf.set_font(fontFamily, size=fontSize["normal"])


def newSection(top = None, bottom = None):

	pdf.add_page()

	if top != None:
		pdf.set_font(fontFamily, 'B', size=fontSize["large"])
		pdf.cell(23, 10, txt=top, ln=1)

	pdf.line(pdf.get_x(), pdf.get_y(), leftMargin + areaWidth, pdf.get_y())
	
	if bottom != None:
		pdf.set_font(fontFamily, 'I', size=fontSize["normal"])
		pdf.cell(23, 10, txt=bottom, ln=1)
	
	pdf.set_font(fontFamily, size=fontSize["normal"])


def newLink(link, indentation=0, align="L"):

	if indentation != 0:
		pdf.cell(indentationWidth * indentation)

	pdf.set_font(fontFamily, size=fontSize["tiny"])
	pdf.cell(0, 5, txt=link, link=link, ln=1, align=align)
	pdf.set_font(fontFamily, size=fontSize["normal"])


def newValue(indentation=0, description="{}", values=[], align="L", fontSize=fontSize["normal"]):

	if type(values) != list:
		values=[values]

	for value in values:
		if value == None:
			value = ""
		elif type(value) != str:
			value = str(value)
		description=description.replace("{}", value, 1)

	if indentation != 0:
		pdf.cell(indentationWidth * indentation)
	
	pdf.set_font(fontFamily, size=fontSize)
	pdf.multi_cell(0, 5, txt=description, align=align)


def newLine(number = 1):

	pdf.ln(lineHeight * number)


def newImage(path, size=30, protocol=None, x=None, y=None, link=None):

	if protocol == None:
		protocol = path.split(".").pop().lower()

	allowedImageTypes = ["png", "jpg", "jpeg", "gif"]

	if protocol not in allowedImageTypes:
		path = os.sep.join([filePath, "images", "invalid_image.png"])
		protocol = "png"

	if x == None:
		x = pdf.get_x()

	if y == None:
		y = pdf.get_y()	

	try:
		pdf.image(path, x, y, size, link=link, type=protocol)
	except:
		path = os.sep.join([filePath, "images", "invalid_image.png"])
		protocol = "png"
		pdf.image(path, x, y, size, link=link, type=protocol)


def newGallery(images = [], imageSize = 50, spaceBetweenImages = 75, identationBetweenDescriptions = 6, imagesByLine = 3, LineByPage = 3):

	imagesOnPage = 0
	imagesOnLine = 0
	imagesByPage = imagesByLine * LineByPage

	for image in images:

		if image.isDownloaded:

			if (image.contents != None) and (len(image.contents) != 0):
				
				identation = imagesOnLine * identationBetweenDescriptions
				
				if image.contents != None:
					imageContents = ", ".join(image.contents)
				
				newValue(indentation = identation, values=imageContents, fontSize=fontSize["tiny"])

			x = None 

			if imagesOnLine != 0:
				x = imagesOnLine * spaceBetweenImages
			
			imagePath = os.sep.join([image.path, image.name])
			
			newImage(imagePath, imageSize, protocol=image.protocol, x=x, y=pdf.get_y() + 1, link=image.url)

			imagesOnLine += 1
			imagesOnPage += 1

			if imagesOnLine == imagesByLine:
				newLine(15)	
				imagesOnLine = 0

			if imagesOnPage == imagesByPage:
				pdf.add_page()
				imagesOnPage = 0


class CustomPDF(FPDF):
 
 	#Header Definition
    def header(self):

        # Set up a logo
        newImage(os.sep.join([filePath, "images", "Logo-ESIEA.jpg"]), 33, x=170, y=5)

        # Line break
        newLine(4)

	#Footer Definition 
    def footer(self):
    	#Set position to bottom
        self.set_y(-10)
 
 		#Change font to italic
        self.set_font(fontFamily, size=fontSize["tiny"])
 
        # Add a page number
        self.cell(0, 10, str(self.page_no()) + " | " + "{nb}", align='R')


def create_pdf(person, resultsPath, identity):

	global pdf

	#Create header and footer
	pdf = CustomPDF()

	#Get total number of pages
	pdf.alias_nb_pages()

	#
	pdf.add_font(fontFamily, '', os.sep.join([filePath, "fonts", "DejaVuSansCondensed.ttf"]), uni=True)
	pdf.add_font(fontFamily, 'B', os.sep.join([filePath, "fonts", "DejaVuSansCondensed-Bold.ttf"]), uni=True)
	pdf.add_font(fontFamily, 'IB', os.sep.join([filePath, "fonts", "DejaVuSansCondensed-BoldOblique.ttf"]), uni=True)
	pdf.add_font(fontFamily, 'I', os.sep.join([filePath, "fonts", "DejaVuSansCondensed-Oblique.ttf"]), uni=True)

	# New page
	newChapter("INFORMATION REPORT", "OPEN SOURCE INTELLIGENCE")

	# Identity

	if person.firstname != None or \
		person.middlenames != [] or\
		person.lastname != None or \
		person.usernames != []:

		newSection("IDENTITY")
		newLine(2)

		if person.firstname != None:
			newValue(description="Firstname: {}", values=person.firstname)
		if person.middlenames != []:
			newValue(description="Middlenames: {}", values=", ".join(person.middlenames))
		if person.lastname != None:
			newValue(description="Lastname: {}", values=person.lastname)
		if person.usernames != []:
			newValue(description="Usernames: {}", values=", ".join(person.usernames))


	#Emails

	if person.emails:

		newSection("EMAILS")

		for email in person.emails:

			newLine(2)
			newValue(indentation=1, values=email.address)

			if len(email.leaks) > 0:
				newValue(indentation=2, values="Leaks found:")

				for leak in email.leaks:
					newValue(indentation=3, description="From {}, ({}):\n{}\n\n", values=[leak["source"], leak["type"], leak["value"]])
			else:
				newValue(indentation=2, values="No leaks found.")

			newLine()


	# Phones
	if len(person.phoneNumbers) > 0:

		newSection("PHONE NUMBERS")

		for phone in person.phoneNumbers:
			newLine(2)
			location = ", ({})".format(phone.location) if phone.location != None else ""
			newValue(indentation=1, description="{} ({})\nCountry: {}{}", values=[phone.number, phone.deviceType, phone.country, location])


	# Accounts

	if len(person.websites) > 0:

		for website in person.websites:

			category = " (" + website.serviceCategory + ")" if (website.serviceCategory != None) else ""
			newSection(website.serviceName + category)
			newLink(website.url, align="R")
			newLine()

			if (website.qrcode != None) and (website.qrcode.isDownloaded):
				newImage(os.sep.join([website.qrcode.path, website.qrcode.name]), 30, x=20, y=pdf.get_y(), link = website.url, protocol=website.qrcode.protocol)
				newLine()

			if website.__class__.__name__ == "Instagram":

				newValue(indentation=5, description="{} ({}, ID: {})", values=[website.username, "Private account" if website.isPrivate else "Public account", website.userId])
				if website.name != None:
					newValue(indentation=5, description="Real name: {}", values=website.name)
				if website.email != None:
					newValue(indentation=5, description="Email: {}", values=website.email)
				if website.address != None:
					newValue(indentation=5, description="Address: {}", values=website.address)
				if website.phone != None:
					newValue(indentation=5, description="Phone number: {}", values=website.phone)
				newValue(indentation=5, description="Followers: {}    Followings: {}    Posts: {}", values=[website.followersCount, website.friendsCount, website.postsCount])
				newLine()
				if (website.avatar != None) and (website.avatar.isDownloaded):
					newImage(os.sep.join([website.avatar.path, website.avatar.name]), 50, x=pdf.get_x()+10, y=100, protocol=website.avatar.protocol, link=website.avatar.url)
				if website.description != None:
					newValue(indentation=7, description="Biography:\n{}", values=website.description)
				
				if (website.avatar != None) or (website.description != None):
					newLine(10)
				
				pdf.add_page()
				newGallery(website.photos)


			elif website.__class__.__name__ == "Twitter":

				userId = " (ID:" + website.userId + ")" if (website.userId != None) else ""
				newValue(indentation=5, description="{}{}", values=[website.username, userId])

				if website.isPrivate:
					newValue(indentation=5, description="Private account")

				else:
					newLine(5)
					if website.tweetsChart.isDownloaded:
						newImage(os.sep.join([website.tweetsChart.path, website.tweetsChart.name]), 180, protocol=website.tweetsChart.protocol)
						newLine(10)
					if website.repliesChart.isDownloaded:
						newImage(os.sep.join([website.repliesChart.path, website.repliesChart.name]), 180, protocol=website.repliesChart.protocol)
						newLine(10)
					if website.retweetsChart.isDownloaded:
						newImage(os.sep.join([website.retweetsChart.path, website.retweetsChart.name]), 180, protocol=website.retweetsChart.protocol)
						newLine(10)
					if website.likesChart.isDownloaded:
						newImage(os.sep.join([website.likesChart.path, website.likesChart.name]), 180, protocol=website.likesChart.protocol)
						newLine(10)
						pdf.add_page()
					if website.hoursChart.isDownloaded:
						newImage(os.sep.join([website.hoursChart.path, website.hoursChart.name]), 180, x=10, protocol=website.hoursChart.protocol)
						newLine(20)
					if website.wordcloud.isDownloaded:
						pdf.add_page()
						newImage(os.sep.join([website.wordcloud.path, website.wordcloud.name]), 150, x=30, y=pdf.get_x() + 30, protocol=website.wordcloud.protocol)

			elif website.__class__.__name__ == "Wikipedia":

				newLine(5)
				newValue(indentation=0, values=website.text)
				pdf.add_page()
				
				newGallery(website.images)


			else:
				newValue(indentation=5, description="Data extraction from this website is not yet fully automated.")
				newLine(5)
				newGallery(website.images)


	# Export
	reportPath = os.sep.join([resultsPath, "{}.pdf".format(identity)])
	
	if not os.path.exists(resultsPath):
		os.makedirs(resultsPath)
	
	pdf.output(reportPath, 'F')

	print("\nFinal report available at {}".format(reportPath))