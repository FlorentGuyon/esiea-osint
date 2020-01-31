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


def newValue(indentation=0, description="{}", values=[], align="L"):

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
	
	pdf.set_font(fontFamily, size=fontSize["normal"])
	pdf.multi_cell(0, 5, txt=description, align=align)


def newLine(number = 1):

	pdf.ln(lineHeight * number)


def newImage(path, size, x=None, y=None, link=None):

	if x == None:
		x = pdf.get_x()

	if y == None:
		y = pdf.get_y()

	pdf.image(path, x, y, size, link=link)


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

	if len(person.accounts) > 0:

		for account in person.accounts:

			category = " (" + account.serviceCategory + ")" if (account.serviceCategory != None) else ""
			newSection(account.serviceName + category)
			newLink(account.profileLink, align="R")
			newLine()

			if account.qrcode != None:
				newImage(os.sep.join([account.qrcode.path, account.qrcode.name]), 30, x=20, y=pdf.get_y(), link = account.profileLink)
				newLine()

			if account.__class__.__name__ == "InstagramAccount":

				newValue(indentation=5, description="{} ({}, ID: {})", values=[account.username, "Private account" if account.isPrivate else "Public account", account.userId])
				if account.name != None:
					newValue(indentation=5, description="Real name: {}", values=account.name)
				if account.email != None:
					newValue(indentation=5, description="Email: {}", values=account.email)
				if account.address != None:
					newValue(indentation=5, description="Address: {}", values=account.address)
				if account.phone != None:
					newValue(indentation=5, description="Phone number: {}", values=account.phone)
				newValue(indentation=5, description="Followers: {}    Followings: {}    Posts: {}", values=[account.followersCount, account.friendsCount, account.postsCount])
				newLine()
				if (account.avatar != None) and (account.avatar.isDownloaded):
					newImage(os.sep.join([account.avatar.path, account.avatar.name]), 50, x=pdf.get_x()+10, y=100)
				if account.description != None:
					newValue(indentation=7, description="Biography:\n{}", values=account.description)
				
				if (account.avatar != None) or (account.description != None):
					newLine(10)
				newLine(5)

				if len(account.photos) > 0:

					imagesByLine = 4
					imageMargin = 5
					imageSize = (areaWidth / imagesByLine) - (imageMargin * 2)

					for photo in account.photos:

						if photo.isDownloaded:
							if pdf.get_x() + imageSize > 200:

								newLine((imageSize * 1.5) / lineHeight)
								pdf.set_x(leftMargin)

							if pdf.get_y() + (imageSize *2) > areaHeight: 

								pdf.add_page()

							pdf.set_x(pdf.get_x() + imageMargin)

							newImage(os.sep.join([photo.path, photo.name]), imageSize)
							
							pdf.set_x(pdf.get_x() + imageSize + imageMargin)

							newLine((imageSize * 1.5) / lineHeight)

				else:
					newLine(3)

			elif account.__class__.__name__ == "TwitterAccount":

				userId = " (ID:" + account.userId + ")" if (account.userId != None) else ""
				newValue(indentation=5, description="{}{}", values=[account.username, userId])

				if account.isPrivate:
					newValue(indentation=5, description="Private account")

				else:
					newLine(5)
					if account.tweetsChart.isDownloaded:
						newImage(os.sep.join([account.tweetsChart.path, account.tweetsChart.name]), 180)
						newLine(10)
					if account.repliesChart.isDownloaded:
						newImage(os.sep.join([account.repliesChart.path, account.repliesChart.name]), 180)
						newLine(10)
					if account.retweetsChart.isDownloaded:
						newImage(os.sep.join([account.retweetsChart.path, account.retweetsChart.name]), 180)
						newLine(10)
					if account.likesChart.isDownloaded:
						newImage(os.sep.join([account.likesChart.path, account.likesChart.name]), 180)
						newLine(10)
						pdf.add_page()
					if account.hoursChart.isDownloaded:
						newImage(os.sep.join([account.hoursChart.path, account.hoursChart.name]), 180, x=10)
						newLine(20)
					if account.wordcloud.isDownloaded:
						pdf.add_page()
						newImage(os.sep.join([account.wordcloud.path, account.wordcloud.name]), 150, x=30, y=pdf.get_x() + 30)
			
			else:
				newValue(indentation=5, description="Data extraction from this website is not yet automated.")


	# Export
	reportPath = os.sep.join([resultsPath, "{}.pdf".format(identity)])
	
	if not os.path.exists(resultsPath):
		os.makedirs(resultsPath)
	
	pdf.output(reportPath, 'F')

	print("\nFinal report available at {}".format(reportPath))