import requests
import re
from requests.api import request
import Util.login as login
import Util.botschutz as botschutz
from bs4 import BeautifulSoup
import time
from keep_alive import keep_alive
import datetime
import random

keep_alive()
#Login
sid = login.doLogin()
def welcherPlanetHatKeinenAuftrag():
    isBotschutz = True
    global sid
    while isBotschutz:
        responseErsterPlanet = requests.get(
            f'http://www.earthlost.de/construction.phtml?planetindex=1600&sid={sid}'
        ).text
        if botschutz.isBotSchutzOderNichtEingeloggt(responseErsterPlanet):
            print("welcherPlanetHatKeinenAuftrag")
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

#16 Schiffsfabrik

tempId = 0
wartezeit = 240
hqPlanis = {1600, 15628,30853,43758,57445,71490,84835,98291,112828,126635,140630,182174,195744,223081,236625,250030,263462,277426,291406,304550,318649}

#Dauerschleife
while True:
    try:
        isPlanetOhneBauauftragVorhanden = True
        print(datetime.datetime.now().time())
        while isPlanetOhneBauauftragVorhanden:
            gebaeude = 17
            #Ermitteln welcher Planet keien Bauauftrag hat
            planetID = welcherPlanetHatKeinenAuftrag()
            if planetID == 0:
                isPlanetOhneBauauftragVorhanden = False
            else:
                planetID = str(planetID).replace('[', '')
                planetID = str(planetID).replace(']', '')
                planetID = str(planetID).replace('\'', '')
                if planetID in hqPlanis:
                  gebaeude = 0
                if(tempId == planetID):
                    gebaeude = random.randint(0,25)
                    print("Keine Ressourcen mehr. Versuchen irgendwas anderes zu bauen.")
                tempId = planetID
                bauParameter = {'sid': sid, 'gebaeude': gebaeude}
                response = requests.post(
                    f'http://www.earthlost.de/construction.phtml?planetindex={planetID}',
                    data=bauParameter).text
                if (botschutz.isBotSchutzOderNichtEingeloggt(response)):
                    sid = login.doLogin()
                    continue
        print('Forschung starten...wenn nicht läuft.')
        forschungsParams = {'sid': sid, 'forschung': '5'}
        response = requests.post(
            f'http://www.earthlost.de/research.phtml?planetindex=78651',
            data=forschungsParams).text
        print(f'Alles abgearbeitet, warte {wartezeit} Sekunden.')
        time.sleep(wartezeit)
    except Exception as e:
        print(e)
        time.sleep(wartezeit)
