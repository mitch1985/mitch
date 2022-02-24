import requests
import re
from requests.api import request
from bs4 import BeautifulSoup
import time
import datetime
import Util.login as login
import Util.botschutz as isBotSchutzOderNichtEingeloggt
import Util.planetenListe as planetenListe

def welcherPlanetHatKeinenAuftrag():
    isBotschutz = True
    global sid
    while isBotschutz:
        responseErsterPlanet = requests.get(f'http://www.earthlost.de/construction.phtml?planetindex=1600&sid={sid}').text
        if isBotSchutzOderNichtEingeloggt(responseErsterPlanet):
            print ("welcherPlanetHatKeinenAuftrag")
            sid = login.doLogin()
            continue
        isBotschutz = False

    soup = BeautifulSoup(responseErsterPlanet, "html.parser")
    links = soup.find_all('a', attrs={'class': 'smalllink'})
    if len(links) == 0:
        return 0
    attrs = links[0].__getattribute__('attrs')
    planetenIndexWoGebautWerdenKann = re.findall(f'planetindex=(.+)\&',
                                                 attrs['href'])
    return planetenIndexWoGebautWerdenKann

def planetUebersicht(planetId):
    isBotschutz = True
    global sid
    while isBotschutz:
        response = requests.get(f'http://www.earthlost.de/construction.phtml?planetindex={planetId}&sid={sid}').text
        if isBotSchutzOderNichtEingeloggt(response):
            sid = login.doLogin()
            continue
        isBotschutz = False
    

#Login
sid = login.doLogin()
meinePlaneten = planetenListe.allePlanetenKoordinatenUndId(sid)
gebaeude = 16
tempId = 0

#Dauerschleife
while True:
    try:
        print("Start")
        print(datetime.datetime.now().time())
        for key, value in meinePlaneten.items():
            #Ermitteln welcher Planet keien Bauauftrag hat
            planetRessourcen = planetUebersicht(key)
        print("Alles abgearbeitet, warte 120 Sekunden.")
        time.sleep(120)
    except Exception as e: 
        print(e)
        time.sleep(120)
