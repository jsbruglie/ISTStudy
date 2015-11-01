import json
import requests
import re
from pprint import pprint

ENDPOINT = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'
OUTPUT = 'spaces.csv'
START = '2448131360897' #Alameda
BLACKLIST='blacklist.txt'

AVOID = [
	'Secção de Folhas',
	'Complexo Interdisciplinar',
	'Infantário',
	'Pavilhão da Associação dos  Estudantes',
	'Pavilhão do Jardim Norte',
	'Pavilhão do Jardim Sul',
	'Pavilhão de Acção Social'
]

def visitSpace(id,path,out,blacklist):

	response = requests.get(ENDPOINT + id)
	jsonData = json.loads(response.text)

	if jsonData['type'] == 'ROOM':
		name, id = jsonData['name'], jsonData['id']
		if name:
			for entry in blacklist:
				if re.search(entry, name, re.IGNORECASE):
					return
			path = path[9:-2] # Lazy string formatting, Yay Python
			string = '"' + path + '","' + name + '",' + id
			out.write(string+'\n')
			out.flush()
			print(string)
		return

	containedSpaces = jsonData['containedSpaces']
	local_path = path + jsonData['name'] + ', '
	for space in containedSpaces:
		if space['name'] not in AVOID:
			visitSpace(space['id'],local_path,out,blacklist)

	return

def readToList(file):
    with open(file,'r') as fileRead:
        lines = fileRead.read().splitlines()
        fileRead.close()
    return lines

def main():

	blacklist = readToList(BLACKLIST)

	with open(OUTPUT, mode='w') as out:
		out.write('path,name,id\n')
		visitSpace(START,'',out,blacklist)
		out.close()
		quit()

if __name__ == "__main__":
	main()
