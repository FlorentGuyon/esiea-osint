import requests
from bs4 import BeautifulSoup

class searchInfoNumero:

	def search(self, num):
		def mob_fix(pfx):
			if pfx == '06' or pfx == '07':
				return("Portable")
			elif pfx == '08' or pfx == '09':
				return("internet")
			else:
				return("Fixe")

		location = {
			"01": "Ile de France.",
			"02": "Nord-Ouest de la France ou Océan Indien. (Bretagne, Centre Val de loire, Normandie, Pays de la Loire, Réunion, Mayotte)",
			"03": "Nord-Est de la France. (Bourgogne-Franche-Compté, Grand Est, Hauts-de-France)",
			"04": "Sud-Est de la France. (Auvergne-Rhône-Alpes, Corse, Occitanie Secteur Est, Provence-Alpes-Côtes d'Azur)",
			"05": "Sud-Ouest de la France ou Outre-Mer. (Nouvelle-Aquitaine, Occitanie Secteur Ouest, Guadeloupe, Martinique, Guyane)"
		}

		num = num.replace(" ","").replace("+33", "0")
		pfx = num[0:2]

		url = 'https://www.infos-numero.com/numero/'
		page = requests.get(url+num).content.decode('utf-8')
		p = []
		soup = BeautifulSoup(page, "html.parser")
		tags = soup("p")

		for n in tags:
			line = n.text
			p.append(line)

		self.location = location.get(pfx)
		self.country = p[3]

		if mob_fix(pfx) == 'Portable':
			self.phone_type = "Portable"
		elif mob_fix(pfx) == 'internet':
			self.phone_type = "Voip/FAI"
		else:
			self.phone_type = "Fixe"