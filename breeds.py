import requests
import json

dog = requests.get('https://api.thedogapi.com/v1/breeds').content
full = json.loads(dog.decode('utf-8'))

def getbreed(b):
	perfect = False
	for dict in full:
		if dict["name"] == b:
			perfect = True
			return dict
			break
	while not perfect:
		for dict in full:
			if b in dict["name"]:
				perfect = True
				return dict
				break
		perfect = True
			
			
			

#print(json.dumps(full, sort_keys=True, indent=4))

