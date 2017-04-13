#!/usr/bin/env python

# Von andre at hamburg.freifunk.net , basierend auf https://github.com/freifunkhamburg/ffmap-backend/blob/dev/node_number.py

#Bibliotheken importieren
import time
import datetime
import json
import shutil

Landkreise={
	"schleswig":[54.521868, 9.561861,"","",""],
	"tarp":[]
}

path="/var/www/html/meshviewer/nord-community-api/"
appendix="-api.json"

#Datei oeffnen
f = open('/var/www/html/meshviewer/data/nodelist.json')

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
Knoten_pro_Landkreis = num_nodes / len(Landkreise)

#Zeit holen
thetime = datetime.datetime.now().isoformat()


for Landkreis in Landkreise:
	LandkreisAPI = path+Landkreis+appendix

	#Aus dem Original eine Datei fuer jeden Landkreis erzeugen
	#shutil.copy2(path+'Original'+appendix,LandkreisAPI)

	#Freifunk API-Datei einladen und JSON lesen
        slfl = None
	with open(LandkreisAPI, 'r') as fp:
        	ffnord = json.load(fp)

	#Attribute Zeitstempel und Knotenanzahl setzen
	slfl['state']['lastchange'] = thetime
	slfl['state']['nodes'] = Knoten_pro_Landkreis

	#Freifunk API-Datein mit geaenderten werten schreiben
	with open(LandkreisAPI, 'w') as fp:
		json.dump(slfl, fp, indent=2, separators=(',', ': '))
