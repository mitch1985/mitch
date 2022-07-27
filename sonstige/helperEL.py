import requests
import re
from requests.api import request
from bs4 import BeautifulSoup
import time


def doLogin():
    # print ("###Starte Login-Script###")
    y = 0
    captcha = 0
    # barneyPudge = [int(item) for item in input("Barney(1)Pudge(2) : ").split()]
    while y < 50:
        # Login Daten senden
        urlLogin = 'http://www.earthlost.de/login.phtml'
        # if barneyPudge==2:
        loginDaten = {'user': 'fr34kscht@gmail.com', 'pwd': 'ostern'}
        # else:
        # loginDaten = {'user': 'barney.stinson.el@gmail.com', 'pwd' : 'ostern'}

        responseLogin = requests.post(urlLogin, data=loginDaten)
        # SID auslesen
        sids = re.findall('sid=(.+?)"', responseLogin.text)
        sid = sids[0]

        x = 0
        while x < 4:
            # Aufruf des Botschutz fuer Sehbehinderte und einfach einen Leer-Code schicken
            urlLoginKlick = 'http://www.earthlost.de/intro.phtml?blind=1'
            loginKoords = {'sid': sid, 'captcha_id': captcha, 'code': ''}
            responseLoginErfolg = requests.post(urlLoginKlick, data=loginKoords).text
            if responseLoginErfolg.__contains__('Pudge') or responseLoginErfolg.__contains__('FanClub'):
                # Beim fehlschlag einfach die captchaid des neuen captcha auslesen, das geht jetzt
                # print ("###Login Erfolgreich FanClub")
                # print ("###"+sid)
                break
            else:
                captchas = re.findall('name=\"captcha_id\" value=\"(.+?)\"', responseLoginErfolg)
                captcha = int(captchas[1])
            x = x + 1
        if x < 4:
            break
        y = y + 1
    # print (sid)
    return sid


def isBotSchutzOderNichtEingeloggt(response):
    if re.findall('eingeloggt', response): print(f'Nicht eingeloggt')
    if re.findall('Bot-Schutz', response): print(f'Bot-Schutz')
    return re.findall('Bot-Schutz', response) or re.findall('eingeloggt', response)


def welcherPlanetHatKeinenAuftrag(sid):
    isBotschutz = True
    while isBotschutz:
        response = requests.get(f'http://www.earthlost.de/construction.phtml?planetindex=1600&sid={sid}').text
        if isBotSchutzOderNichtEingeloggt(response):
            sid = doLogin()
            continue
        isBotschutz = False

    soup = BeautifulSoup(response, "html.parser")
    links = soup.find_all('a', attrs={'class': 'smalllink'})
    if len(links) == 0:
        return 0
    attrs = links[0].__getattribute__('attrs')
    planetenIndexWoGebautWerdenKann = re.findall(f'planetindex=(.+)\&', attrs['href'])
    return planetenIndexWoGebautWerdenKann


print("Start")
sid = doLogin()
# Dauerschleife
while True:
    isPlanetOhneBauauftragVorhanden = True
    while isPlanetOhneBauauftragVorhanden:
        # Ermitteln welcher Planet keien Bauauftrag hat
        planetID = welcherPlanetHatKeinenAuftrag(sid)
        if planetID == 0:
            isPlanetOhneBauauftragVorhanden = False
        else:
            planetID = str(planetID).replace('[', '')
            planetID = str(planetID).replace(']', '')
            planetID = str(planetID).replace('\'', '')
            print(planetID)
            bauParameter = {'sid': sid, 'gebaeude': '1'}
            response = requests.post(f'http://www.earthlost.de/construction.phtml?planetindex={planetID}',
                                     data=bauParameter).text
            if (isBotSchutzOderNichtEingeloggt(response)):
                sid = doLogin()
                continue
    print("Fertig - Warten jetzt, je nach Einstellung.")
    time.sleep(60)
