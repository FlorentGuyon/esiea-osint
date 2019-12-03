from colorama import init, Fore,  Back,  Style
from .instagramSearchTool import instagramSearchTool
from .shortCutUrl import shortCutUrl
import os

warning = "["+Fore.RED+"!"+Fore.RESET+"]"
question = "["+Fore.YELLOW+"?"+Fore.RESET+"]"
found = "["+Fore.GREEN+"+"+Fore.RESET+"]"
wait = "["+Fore.MAGENTA+"*"+Fore.RESET+"]"

def extractInstagram(urlProfil, imagesPath):

	insta = instagramSearchTool()
	insta.getInfo(urlProfil)
	
	pictureInfo = insta.get_picturesInfo(urlProfil)

	photos = []

	for i in pictureInfo:

		path = os.sep.join((imagesPath, insta.username))
		filename = "{}_{}.jpg".format(insta.username, str(i))
		media = pictureInfo[i]['display']

		insta.downloadPictures(media, path, filename)

		photos.append({
			"media": media,
			"typeMedia": pictureInfo[i]['type_media'],
			"date": pictureInfo[i]['date'],
			"view": pictureInfo[i]['info'],
			"loc": pictureInfo[i]['localisation'],
			"path": os.sep.join((path, filename))
			})

	return {
		"name": insta.name, 
		"id": insta.id,
		"profilPhoto": insta.profi_pic_hd, 
		"username": insta.username, 
		"private": insta.private, 
		"followers": insta.followers, 
		"friends": insta.friends,
		"medias": insta.medias,
		"biography": insta.biography,
		"url": insta.url,
		"email": insta.email,
		"adresse": insta.adresse,
		"phone": insta.phone,
		"photos": photos
	}

def searchInstagram(user = None):

	if user == None:
		user = input(" Username: ")

	urlProfil = "https://instagram.com/"+user

	insta = instagramSearchTool()
	insta.getInfo(user)

	name = insta.name
	userId = insta.id
	images = insta.profi_pic_hd
	images = shortCutUrl(images)
	username = insta.username
	private = insta.private
	followers = insta.followers
	friend = insta.friends
	publication = insta.medias
	bio = insta.biography
	url = insta.url
	email = insta.email
	adresse = insta.adresse
	phone = insta.phone

	print("\n[%s]\n" % (username))
	print(found+" Name: %s" % (name))
	print(found+" Pictures: %s" % (images))
	print(found+" ID: %s" % (userId))
	print(found+" Protected: %s" % (private))
	print(found+" Abonnés: %s  |  Abonnements: %s" % (followers, friend))
	print(found+" Publication: %s" % (publication))
	print(found+" Bio: %s" % (bio))

	if url:
		print(found+" Url: %s" % (url))
	if email:
		print(found+" Email: %s" % (email))
	if phone:
		print(found+" Telephone: %s" % (phone))
	if adresse:
		print(found+" Lieux: %s" % (adresse))

	if not private:
		print("\n"+question+" Voulez vous télécharger les 12 dernières photos postées ?")

		while True:
			choix = input("\n [o/N]: ")

			if choix == "" or choix.upper() == "N":
				break
			
			elif choix.upper() == "O":
				print("\n"+question+" Ou voulez-vous enregistrer les photos ?")
				pathDefault = os.getcwd()
				print(Fore.YELLOW+" Default path: "+pathDefault+Fore.RESET)
				path = input("\n Path: ")
				print("\n"+wait+" Téléchargement des photos de '%s'\n" % (user))
			
				if not path:
					path = pathDefault
			
				pictureInfo = insta.get_picturesInfo(urlProfil)

				for i in pictureInfo:
					media = pictureInfo[i]['display']
					typeMedia = pictureInfo[i]['type_media']
					date = pictureInfo[i]['date']
					view = pictureInfo[i]['info']
					loc = pictureInfo[i]['localisation'] 
					filename = user+'_'+str(i)+".jpg"

					if not loc:
						loc = ''

					insta.downloadPictures(media, path, filename)
					print("(%s) %s %s [%s] %s téléchargé." % (str(i), typeMedia, date, view, loc))

				print("\n"+found+" Téléchargement fini.")
				break