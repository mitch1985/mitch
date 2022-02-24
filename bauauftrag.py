import requests
import re
from requests.api import request
import Util.login as login
import Util.botschutz as isBotSchutzOderNichtEingeloggt
from bs4 import BeautifulSoup
import time
import datetime

#Login
sid = login.doLogin()

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


print("Start")
gebaeude = 16
tempId = 0

#Dauerschleife
while True:
    try:
        isPlanetOhneBauauftragVorhanden = True
        print(datetime.datetime.now().time())
        while isPlanetOhneBauauftragVorhanden:
            #Ermitteln welcher Planet keien Bauauftrag hat
            planetID = welcherPlanetHatKeinenAuftrag()
            print (planetID)
            if planetID == 0:
                isPlanetOhneBauauftragVorhanden = False
            else:
                planetID = str(planetID).replace('[', '')
                planetID = str(planetID).replace(']', '')
                planetID = str(planetID).replace('\'', '')
                if (planetID == tempId):
                    if (gebaeude == 25):
                        gebaeude = 0
                    gebaeude = gebaeude + 1
                    print(gebaeude)
                tempId = planetID
                print(planetID)
                bauParameter = {'sid': sid, 'gebaeude': gebaeude}
                response = requests.post(
                    f'http://www.earthlost.de/construction.phtml?planetindex={planetID}',
                    data=bauParameter).text
                if (isBotSchutzOderNichtEingeloggt(response)):
                    print("bauauftrag Main")
                    sid = login.doLogin()
                    continue
        print ('Forschung starten...wenn nicht läuft.')
        forschungsParams = {'sid': sid, 'forschung': '18'}
        response = requests.post(
                  f'http://www.earthlost.de/research.phtml?planetindex=78651',
                  data=forschungsParams).text
        print("Alles abgearbeitet, warte 120 Sekunden.")
        time.sleep(120)
    except:
        print("Except-Block Bauauftrag - Womöglich kein Internet.")
        time.sleep(120)
