#!/usr/bin/env python

# Von andre at hamburg.freifunk.net , basierend auf https://github.com/freifunkhamburg/ffmap-backend/blob/dev/node_number.py

#Bibliotheken importieren
import time
import datetime
import json
import shutil
import os
import urllib
from collections import Mapping

NODELISTS_DIR = './nodelists/'

# For every line in the file
for url_raw in open('urls.txt'):
	url = url_raw.rstrip().split(" ")
	name = url[1] + ".json"

	# Combine the name and the downloads directory to get the local filename
	filename = os.path.join(NODELISTS_DIR, name)

	# Download the files
	urllib.urlretrieve(url[0], filename)

nodelist = json.loads("{}");
for url_raw in open('urls.txt'):
	url = url_raw.rstrip().split(" ")
	name = url[1] + ".json"
	nodelists = None
	with open(os.path.join(NODELISTS_DIR, name), 'r') as fp:
		nodelists = json.load(fp)

	for key, value in nodelists.iteritems():
		if key in nodelist:
			original_value = nodelist[key]
			if isinstance(value, Mapping) and isinstance(original_value, Mapping):
				merge_dicts(original_value, value)
			elif not (isinstance(value, Mapping) or isinstance(original_value, Mapping)):
				if type(value) is list:
					nodelist[key] = original_value + value
				else:
                        	        nodelist[key] = value
			else:
				print("raise")
				raise ValueError('Attempting to merge {} with value {}'.format(key, original_value))
		else:
			nodelist[key] = value

#Nodelist-Datei mit geaenderten werten schreiben
with open('./nodelist.json', 'w') as fp:
	json.dump(nodelist, fp, indent=2, separators=(',', ': '))


Aemter={
	"schafflund":["Amt Schafflund","54.7631344","9.1691851"],
	"handewitt":["Gemeinde Handewitt","54.757954","9.327019"],
	"harrislee":["Gemeinde Harrislee","54.811805","9.388123"],
	"eggebek":["Amt Eggebek","54.619662","9.379866"],
	"oeversee":["Amt Oversee","54.663209","9.401545"],
	"arensharde":["Amt Arensharde","54.517","9.3648113"],
	"schleswig":["Stadt Schleswig","54.523680","9.561518"],
	"kropp-stapelholm":["Amt Kropp-Stapelholm","54.400150","9.450043"],
	"haddeby":["Amt Haddeby","54.466693","9.566664"],
	"suedangeln":["Amt Suedangeln","54.600174","9.566979"],
	"huerup":["Amt Huerup","54.7542725","9.5324292"],
	"mittelangeln":["Amt Mittelangeln","54.69458","9.60183"],
	"suederbrarup":["Amt Suederbrarup","54.634902474251625","9.7723388671875"],
	"kappeln-land":["Amt Kappeln-Land","54.62814577657538","9.933013916015623"],
	"kappeln":["Stadt Kappeln","54.66310949098682","9.935760498046875"],
	"geltinger_bucht":["Amt Geltinger Bucht","54.750440","9.900150"],
	"langballig":["Amt Langballig","54.807276","9.640116"],
	"gluecksburg":["Stadt Gluecksburg","54.838054","9.563276"]
}

path="./aemter/"
appendix="-api.json"

#Datei oeffnen
f = open('./nodelist.json')

#JSON einlesen
data = json.load(f)

#Nodes attribut aussortieren
nodes = data['nodes']

#Zaehler mit Wert 0 anlegen
num_nodes = 0

#Fuer jeden Knoten in nodes
for node in nodes:
        #Status Attribut aussortieren
        status = node['status']

        #Wenn der Status online entaehlt, hochzaehlen
        if status['online']:
                num_nodes += 1

#Knoten pro Landkreis
Knoten_pro_Amt = num_nodes / len(Aemter)
if Knoten_pro_Amt < 1:
	Knoten_pro_Amt = 1

#Zeit holen
thetime = datetime.datetime.now().isoformat()


for Amt in Aemter:
	AmtAPI = path+Amt+appendix

	#Aus dem Original eine Datei fuer jeden Landkreis erzeugen
	shutil.copy2('./Original-api.json',AmtAPI)

	#Freifunk API-Datei einladen und JSON lesen
	slfl = None
	with open(AmtAPI, 'r') as fp:
        	slfl = json.load(fp)

	#Attribute Zeitstempel und Knotenanzahl setzen
	slfl['state']['lastchange'] = thetime
	slfl['state']['nodes'] = Knoten_pro_Amt
	slfl['location']['city'] = Aemter[Amt][0]
	slfl['location']['lat'] = float(Aemter[Amt][1])
	slfl['location']['lon'] = float(Aemter[Amt][2])
	slfl['location']['name'] = "Freifunk " + Aemter[Amt][0]

	#Freifunk API-Datein mit geaenderten werten schreiben
	with open(AmtAPI, 'w') as fp:
		json.dump(slfl, fp, indent=2, separators=(',', ': '))
