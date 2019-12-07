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

font = "Arial"

lineHeigh = 5
indentationWidth = 10

fontSize = {
	
	"tiny": 8,
	"normal": 10,
	"large": 14,
	"veryLarge": 18
}


def newChapter(pdf, title, subtitle):
	
	pdf.add_page()
	pdf.set_font(font, size=fontSize["veryLarge"])
	pdf.multi_cell(0, 10, txt=title, align="C")
	pdf.set_font(font, "I", size=fontSize["large"])
	pdf.multi_cell(0, 5, txt=subtitle, align="C")
	pdf.set_font(font, size=fontSize["normal"])


def newSection(pdf, chapter):

	newLine(pdf, 3)
	pdf.line(pdf.get_x(), pdf.get_y(), areaWidth, pdf.get_y())
	pdf.set_font(font, size=fontSize["large"])
	pdf.cell(23, 10, txt=chapter, ln=1)
	pdf.set_font(font, size=fontSize["normal"])
	newLine(pdf)

def newValue(pdf, indentation=0, description="{}", values=[]):

	if type(values) != list:
		values=[values]

	for value in values:
		if value == None or value == "":
			value="UNKNOW"
		elif type(value) != str:
			value = str(value)
		description=description.replace("{}", value, 1)

	if indentation != 0:
		pdf.cell(indentationWidth * indentation)
	
	pdf.multi_cell(0, 5, txt=description)
	pdf.set_font(font)


def newLine(pdf, number = 1):

	pdf.ln(lineHeigh * number)



def newImage(pdf, path, size, x=None, y=None):

	if x == None:
		x = pdf.get_x()

	if y == None:
		y = pdf.get_y()

	pdf.image(path, x, y, size)

class CustomPDF(FPDF):
 
 	#Header Definition
    def header(self):

        # Set up a logo
        newImage(self, os.sep.join([os.path.dirname(os.path.abspath(__file__)), "..", "images", "Logo-ESIEA.jpg"]), 33, x=170, y=5)

        # Line break
        newLine(self, 4)

	#Footer Definition 
    def footer(self):
    	#Set position to bottom
        self.set_y(-10)
 
 		#Change font to italic
        self.set_font(font, size=fontSize["tiny"])
 
        # Add a page number
        self.cell(0, 10, str(self.page_no()) + " | " + "{nb}", align='R')

def create_pdf(person, resultsPath):

	#Create header and footer
	pdf = CustomPDF()

	#Get total number of pages
	pdf.alias_nb_pages()

	# New page
	newChapter(pdf, "INFORMATION REPORT", "OPEN SOURCE INTELLIGENCE")
	

	# Identity

	newSection(pdf, "IDENTITY")

	newValue(pdf, description="Firstname: {}", values=person.firstname)
	newValue(pdf, description="Middlenames: {}", values=", ".join(person.middlenames))
	newValue(pdf, description="Lastname: {}", values=person.lastname)
	newValue(pdf, description="Usernames: {}", values=", ".join(person.usernames))


	#Emails

	newSection(pdf, "EMAILS")

	if person.emails:

		for email in person.emails:

			newValue(pdf, indentation=1, values=email.address)

			if len(email.leaks) > 0:
				newValue(pdf, indentation=2, values="Leaks found:")

				for leak in email.leaks:
					newValue(pdf, indentation=3, description="From {}, ({}):\n{}\n", values=[leak["source"], leak["type"], leak["value"]])
			else:
				newValue(pdf, indentation=2, values="No leaks found.")

			newLine(pdf)

	else:
		newValue(pdf, indentation=1, values="No email address found.")


	# Phones

	newSection(pdf, "PHONE NUMBERS")

	if len(person.phoneNumbers) > 0:
		
		for phone in person.phoneNumbers:
			newValue(pdf, indentation=1, description="{} ({} - {})\n{}, {}", values=[phone.number, phone.deviceType, phone.provider, phone.city, phone.location])
			newLine(pdf)
	
	else:
		newValue(pdf, indentation=1, values="No phone number found.")


	# Accounts

	newSection(pdf, "ACCOUNTS")

	if len(person.accounts) > 0:

		for account in person.accounts:
			newValue(pdf, indentation=1, description="{} ({})\n{}", values=[account.serviceName, account.serviceCategory, account.profileLink])

			if account.__class__.__name__ == "InstagramAccount":
				newLine(pdf)
				newValue(pdf, indentation=2, description="{} ({}, ID: {}) Real name: {}", values=[account.username, "Private account" if account.isPrivate else "Public account", account.userId, account.name])
				newValue(pdf, indentation=2, description="Email: {}, Address: {}, Phone number: {}", values=[account.email, account.address, account.phone])
				newValue(pdf, indentation=2, description="Followers: {}    Friends: {}    Posts: {}", values=[account.followersCount, account.friendsCount, account.postsCount])
				newLine(pdf)

				if account.avatar != None:

					pdf.set_x(pdf.get_x() + (indentationWidth * 2))
					newImage(pdf, os.sep.join([account.avatar.path, account.avatar.name]), 30)

				newValue(pdf, indentation=4, description="Biography:\n{}", values=account.description)
				newLine(pdf, 5)

				if len(account.photos) > 0:

					imagesByLine = 4
					imageMargin = 5
					imageSize = (areaWidth / imagesByLine) - (imageMargin * 2)

					for photo in account.photos:

						if pdf.get_x() + imageSize > 200:

							newLine(pdf, (imageSize * 1.5) / lineHeigh)
							pdf.set_x(leftMargin)

						if pdf.get_y() + (imageSize *2) > areaHeight: 

							pdf.add_page()

						pdf.set_x(pdf.get_x() + imageMargin)

						newImage(pdf, os.sep.join([photo.path, photo.name]), imageSize)
						
						pdf.set_x(pdf.get_x() + imageSize + imageMargin)


					newLine(pdf, (imageSize * 1.5) / lineHeigh)

				else:
					newLine(pdf, 3)
			
			newLine(pdf)
	
	else:
		newValue(pdf, indentation=1, values="No account found.")


	# Export
	reportPath = os.sep.join([resultsPath, "{} {}.pdf".format(person.firstname, person.lastname)])
	pdf.output(reportPath)

	print("\nFinal report available at {}".format(reportPath))