#!/usr/bin/env python

# Von andre at hamburg.freifunk.net , basierend auf https://github.com/freifunkhamburg/ffmap-backend/blob/dev/node_number.py

#Bibliotheken importieren
import time
import datetime
import json
import shutil

Aemter={
	"schleswig":["","",""],
	"oeversee":["Amt Oversee","",""]
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
Knoten_pro_Amt = num_nodes / len(Aemter)

#Zeit holen
thetime = datetime.datetime.now().isoformat()


for Amt in Aemter:
	AmtAPI = path+Amt+appendix

	#Aus dem Original eine Datei fuer jeden Landkreis erzeugen
	#shutil.copy2(path+'Original'+appendix,AmtAPI)

	#Freifunk API-Datei einladen und JSON lesen
    slfl = None
	with open(AmtAPI, 'r') as fp:
        	slfl = json.load(fp)

	#Attribute Zeitstempel und Knotenanzahl setzen
	slfl['state']['lastchange'] = thetime
	slfl['state']['nodes'] = Knoten_pro_Amt
	slfl['location']['city'] = Aemter[Amt][0]
	slfl['location']['lat'] = Aemter[Amt][1]
	slfl['location']['long'] = Aemter[Amt][2]

	#Freifunk API-Datein mit geaenderten werten schreiben
	with open(AmtAPI, 'w') as fp:
		json.dump(slfl, fp, indent=2, separators=(',', ': '))
