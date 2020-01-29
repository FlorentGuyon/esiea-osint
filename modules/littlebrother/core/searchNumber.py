import requests, sys

from .searchPJ import searchPJ
from .searchInfoNumero import searchInfoNumero
from .searchLocalCH import searchLocalCH
from .searchYellowLU import searchYellowLU
from terminaltables import SingleTable

def searchNumberAPI(number):

	return searchNumber(number = number, verbose = False)


def searchNumber(codemonpays = "FR", number = None, verbose = True):

	if number == None:
		num = input(" Téléphone: ")
	else:
		num = number

	headers = {
		'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
	    'referrer': 'https://google.com',
    	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    	'Accept-Encoding': 'gzip, deflate, br',
    	'Accept-Language': 'en-US,en;q=0.9',
    	'Pragma': 'no-cache'
    }

	if codemonpays == "FR":
		url = "https://www.pagesjaunes.fr/annuaireinverse/recherche?quoiqui="
		requete = requests.get(url+num, headers=headers)
		searchPJ(requete=requete, num=num, verbose = verbose)
		phone = searchInfoNumero()
		phone.search(num)

		TABLE_DATA = []

		country = phone.country
		location = phone.location
		_type = phone.phone_type

		infos = ("Numero", num)
		TABLE_DATA.append(infos)
		infos = ("Type", _type)
		TABLE_DATA.append(infos)
		infos = ("Pays", country)
		TABLE_DATA.append(infos)
		infos = ("Localisation", location)
		TABLE_DATA.append(infos)

		table = SingleTable(TABLE_DATA)
		if verbose:
			print("\n"+table.table)

	elif codemonpays == "CH":
		# search CH
		url = "https://tel.local.ch/fr/q?ext=1&rid=NV3M&name=&company=&street=&city=&area=&phone="
		searchLocalCH(url+num)

	elif codemonpays == "LU":
		url = "https://www.yellow.lu/fr/annuaire-inverse/recherche?query="
		searchYellowLU(url+num)

	else:
		# !!!! c'est deguelasse je sais... mais je n'avais pas le choix.. sa sera propre dans une prochaine MAJ... encore desole..
		url = "https://www.pagesjaunes.fr/annuaireinverse/recherche?quoiqui="
		requete = requests.get(url+num, headers=headers)
		searchPJ(requete=requete, num=num)
		phone = searchInfoNumero()
		phone.search(num)

		TABLE_DATA = []

		city = phone.city
		operator = phone.operator
		location = phone.location
		_type = phone.phone_type

		infos = ("Numero", num)
		TABLE_DATA.append(infos)
		infos = ("Type", _type)
		TABLE_DATA.append(infos)
		infos = ("Operateur", operator)
		TABLE_DATA.append(infos)
		infos = ("City", city)
		TABLE_DATA.append(infos)
		infos = ("Localisation", location)
		TABLE_DATA.append(infos)

		table = SingleTable(TABLE_DATA)
		if verbose:
			print("\n"+table.table)

		url = "https://tel.local.ch/fr/q?ext=1&rid=NV3M&name=&company=&street=&city=&area=&phone="
		searchLocalCH(url+num)

		url = "https://www.yellow.lu/fr/annuaire-inverse/recherche?query="
		searchYellowLU(url+num)

	results = {
		"number": num,
		"deviceType": _type,
		"country": country,
		"location": location 
	}

	return results