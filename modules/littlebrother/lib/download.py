import requests, os, errno

def download(url, path, filename):
	r = requests.get(url)

	if not os.path.exists(path):
	    try:
	        os.makedirs(path)
	    except OSError as exc: # Guard against race condition
	        if exc.errno != errno.EEXIST:
	            raise

	with open(os.sep.join((path, filename)), 'wb') as f:

		for chunk in r.iter_content(chunk_size=255): 
			if chunk:
				f.write(chunk)