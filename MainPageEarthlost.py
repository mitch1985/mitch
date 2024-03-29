import requests
import re
import login as login
import botschutz as botschutz
# from Util import findeKolonisierbarePlanetenMitPunkten as findKoloPlanis
from bs4 import BeautifulSoup
import time
from keep_alive import keep_alive
import datetime
import random

print("los gehts")
keep_alive()
# Login
sid = login.doLogin()
galaxy = 1


# Die Methode schaut, ob ein HQ ausgebaut werden muss <120 HQ
def welchesGebaeuteIstDran(planetenIndex):
    isAllesLaeuftNormal = True
    global sid
    while isAllesLaeuftNormal:
        responsePlanet = requests.get(
            f'http://www.earthlost.de/construction.phtml?planetindex={planetenIndex}&sid={sid}'
        ).text
        if botschutz.isBotSchutzOderNichtEingeloggt(responsePlanet):
            print(
                "Botschutz oder nicht Eingeloggt in der Methode: isHqAusbauNoetig"
            )
            sid = login.doLogin()
            continue
        isAllesLaeuftNormal = False
        planetenGebaeudeStatus = re.findall('gebaeude\((.*?)\)\;',
                                            responsePlanet)
        planetHqAttribute = planetenGebaeudeStatus[0].split(',')
        for planiGebaeute in planetenGebaeudeStatus:
            planiGebaeuteSplit = planiGebaeute.split(',')
            print (planiGebaeuteSplit[2])
            test = str(planiGebaeuteSplit[2])
            if (test.__contains__("Hauptquartier") and int(planiGebaeuteSplit[4]) < 120):
                return 0
            elif (test.__contains__("Biozelle") and int(planiGebaeuteSplit[4]) < 120):
                return 1
            elif (test.__contains__("Farm") and int(planiGebaeuteSplit[4]) < 200):
                return 3
            elif (test.__contains__("Bohrturm") and int(planiGebaeuteSplit[4]) < 200):
                return 6
            elif (test.__contains__("Schiffsfabrik") and int(planiGebaeuteSplit[4]) < 120):
                return 16
            elif (test.__contains__("Verteidigungsstation") and int(planiGebaeuteSplit[4]) < 100):
                return 17
        return 0


# Welcher Planet baut gerade nicht?
def welcherPlanetHatKeinenAuftrag():
    isAllesLaeuftNormal = True
    global sid
    while isAllesLaeuftNormal:
        responseErsterPlanet = requests.get(
            f'http://www.earthlost.de/construction.phtml?planetindex=1600&sid={sid}'
        ).text
        if botschutz.isBotSchutzOderNichtEingeloggt(responseErsterPlanet):
            # print("welcherPlanetHatKeinenAuftrag()")
            sid = login.doLogin()
            continue
        isAllesLaeuftNormal = False

    soup = BeautifulSoup(responseErsterPlanet, "html.parser")
    links = soup.find_all('a', attrs={'class': 'smalllink'})
    if len(links) == 0:
        return 0
    attrs = links[0].__getattribute__('attrs')
    planetenIndexWoGebautWerdenKann = re.findall(f'planetindex=(.+)\&',
                                                 attrs['href'])

    planetenIndexWoGebautWerdenKann = str(
        planetenIndexWoGebautWerdenKann).replace('[', '')
    planetenIndexWoGebautWerdenKann = str(
        planetenIndexWoGebautWerdenKann).replace(']', '')
    planetenIndexWoGebautWerdenKann = str(
        planetenIndexWoGebautWerdenKann).replace('\'', '')

    return planetenIndexWoGebautWerdenKann


# 16 Schiffsfabrik

tempId = 0
wartezeit = 240
# Dauerschleife
while True:
    try:
        isPlanetOhneBauauftragVorhanden = True
        print(datetime.datetime.now().time())
        while isPlanetOhneBauauftragVorhanden:
            gebaeude = 16
            # Ermitteln welcher Planet keien Bauauftrag hat
            planetID = welcherPlanetHatKeinenAuftrag()
            if planetID == 0:
                isPlanetOhneBauauftragVorhanden = False
            else:
                gebaeude = welchesGebaeuteIstDran(planetID)

                if tempId == planetID:
                    gebaeude = random.randint(0, 25)
                    print(
                        "Keine Ressourcen mehr. Versuchen irgendwas anderes zu bauen."
                    )
                tempId = planetID
                bauParameter = {'sid': sid, 'gebaeude': gebaeude}
                response = requests.post(
                    f'http://www.earthlost.de/construction.phtml?planetindex={planetID}',
                    data=bauParameter).text
                if botschutz.isBotSchutzOderNichtEingeloggt(response):
                    sid = login.doLogin()
                    continue
        # print('Forschung starten...wenn nicht läuft.')
        forschungsParams = {'sid': sid, 'forschung': '5'}
        response = requests.post(
            f'http://www.earthlost.de/research.phtml?planetindex=78651',
            data=forschungsParams).text
        print(f'Alles abgearbeitet, warte {wartezeit} Sekunden.')
        # print(
        #    f'Alle Planeten haben einen Bauauftrag. Suche nach freien Planeten starten.'
        # )
        # findKoloPlanis.findeKolonisierbarePlanetenMitPunkten(
        # random.randint(1, 25), sid)
        time.sleep(wartezeit)
    except Exception as e:
        print(f'Unerwarteter Fehler in der MainPageEarthlost.py{e}')
        time.sleep(wartezeit)
