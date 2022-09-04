import requests
import re
import login as login

import botschutz as botschutz

# def findeKolonisierbarePlanetenMitPunkten(galaxy, sid):
# global response
universe = 3
system = 1
galaxy = 14
sid = login.doLogin()
# print(f'Finde Kolo Planis startet mit der Galaxy: {galaxy}')
while galaxy < 25:
    galaxy = galaxy + 1
    system = 1
    while system <= 500:
        isAllesLaeuftNormal = True
        while isAllesLaeuftNormal:
            url = f'http://www.earthlost.de/galaxy.phtml?universe={universe}&galaxy={galaxy}&system={system}&sid={sid}'
            response = requests.get(url)
            if botschutz.isBotSchutzOderNichtEingeloggt(response.text):
                sid = login.doLogin()
                continue
            isAllesLaeuftNormal = False
        planetenListe = re.findall('drawPlanet(.+?)\);', response.text)
        i = 0
        for planet in planetenListe:
            planetAttribute = planet.split(',')
            try:
                if len(planetAttribute) != 16:
                    while len(planetAttribute) > 16:
                        planetAttribute.pop(4)

                if (re.search('""', planetAttribute[3])
                        and int(planetAttribute[7]) > 1500) or (
                            int(planetAttribute[11]) == 10
                            and int(planetAttribute[7]) > 1500):
                    freiOderGelb = 'gelb' if planetAttribute[
                        11] == ' 10' else 'frei'
                    print(
                        f'{galaxy}:{system}:{i} - {planetAttribute[7]} Punkte - {freiOderGelb}'
                    )
            except:
                print(f'Fehler: {galaxy}:{system}')
            i = i + 1
        system = system + 1
