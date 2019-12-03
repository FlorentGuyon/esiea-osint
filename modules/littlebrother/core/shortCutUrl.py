import requests, re

def shortCutUrl(url):
	domain = 'https://is.gd/'
	site = "http://is.gd/create.php?forsimple&url="
	site += url

	req = requests.get(site)
	page = req.text
	
	if req.status_code == 200:
		shorted = re.findall(r"https://is\.gd/([a-zA-Z0-9]{6})", page)[0]
		shorted = domain+shorted
	else:
		shorted = None

	return(shorted)
