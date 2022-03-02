import requests
import re
from requests.api import request
import Util.login as login
import Util.planetenListe as planetenListe

#Botschutz detektor
def isBotSchutzOderNichtEingeloggt(response):
    if re.findall('eingeloggt', response) : print (f'Nicht eingeloggt')
    if re.findall('Bot-Schutz', response) : print (f'Bot-Schutz')
    return re.findall('Bot-Schutz',response) or re.findall('eingeloggt', response)

def schiffsschleifeLoeschen(response):
    #Finde alle Schiffe in den Schleifen -> "[Schiff1] [Schiff2] [Schiff3]"
    produktionsUebersicht = re.findall("addBuildS\(\[(.+?)\]\)\;", response)
    #Aufteilung der [Schiff1][...][...] in ein Array ohne "[]"
    produktionsListe=[]
        
    if len(produktionsUebersicht)>0:
        produktionsListe = re.findall('\[(.+?)\]', produktionsUebersicht[0])
        produktionsListe = [w.replace('"', '') for w in produktionsListe]
        print(f'len{produktionsListe}')

    for produktionAttributeString in produktionsListe:
        produktionAttributeArray = str(produktionAttributeString).split(',')
        responseLoescheSchiffe = requests.get(f'http://www.earthlost.de/produktion.phtml?action=delete&sid={sid}&item={produktionAttributeArray[0]}').text
        if isBotSchutzOderNichtEingeloggt(responseLoescheSchiffe):
            login.doLogin()

#Login und Planeten holen
sid = login.doLogin()
meinePlaneten = planetenListe.allePlanetenIndex(sid)

#Sollen die Schleifen gelöscht werden?
print("Schiffsbauschleifen")
loescheSchiffsschleifen = True if 'j' ==input("Schleifen löschen (j/n) : ") else False

#Jeden einzelnen Planenten durchlaufen
for planetenIndex in meinePlaneten:
    #Jeden Planeten anwählen und die Seite Produktion wählen (Schiffeproduktion)
    responsePlanetProduktion = requests.get(f'http://www.earthlost.de/produktion.phtml?planetindex={planetenIndex}&sid={sid}').text
    print(f'Es wird der Planet bearbeitet: {planetenIndex}')
    #Sollen die Schiffsschleifen gelöscht werden? 
    if (isBotSchutzOderNichtEingeloggt(responsePlanetProduktion)):
        meinePlaneten.append(planetenIndex)
        sid = login.doLogin()
        continue
    #print(f'Schleifen werden gelöscht.')
    elif (loescheSchiffsschleifen):
        schiffsschleifeLoeschen(responsePlanetProduktion)

    schiffsproduktion = {'sid' : sid, 'sr6' : '9999', 'action' : 'build' }
    responseSchiffeproduzieren = requests.post(f'http://www.earthlost.de/produktion.phtml?planetindex={planetenIndex}', data=schiffsproduktion).text
    if isBotSchutzOderNichtEingeloggt(responseSchiffeproduzieren):
        meinePlaneten.append(planetenIndex)
        sid = login.doLogin()
        continue
#s18=grandor
#sr1=snatcher
#sid=r1ek2vg99auk5me3i39str4pn1&action=build&sr0=&sr1=999&sr2=&sr3=&sr4=&sr5=&sr6=&sr7=&s8=&sr9=&sr10=&sr11=&sr13=&sr14=&s15=&s17=&s18=&s19=&sid=r1ek2vg99auk5me3i39str4pn1
print("Ende")
