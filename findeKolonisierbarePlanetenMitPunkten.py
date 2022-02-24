import requests
import re
import Util.login as login
from bs4 import BeautifulSoup
import locale

sid = login.doLogin()

universe = 3

galaxy = 1
while galaxy <= 25:
    system = 1
    while system <= 500:
        url =f'http://www.earthlost.de/galaxy.phtml?universe={universe}&galaxy={galaxy}&system={system}&sid={sid}'
        response = requests.get(url)
        planetenListe = re.findall('drawPlanet(.+?)\);',response.text)
        i=0
        if len(planetenListe)!=0:
            for planet in planetenListe:
                planetAttribute = planet.split(',')         
                try:
                    if len(planetAttribute)!=16:
                        while len(planetAttribute) > 16:
                            planetAttribute.pop(4)
                    
                    if (re.search('""',planetAttribute[3]) and int(planetAttribute[7]) > 1500) or (int(planetAttribute[11]) == 10 and int(planetAttribute[7]) > 1500) :
                        freiOderGelb= 'gelb' if planetAttribute[11]==' 10' else 'frei'
                        print (f'{galaxy}:{system}:{i} - {planetAttribute[7]} Punkte - {freiOderGelb}')
                except:
                    print (f'Fehler: {galaxy}:{system}')
                i=i+1
        else:
            sid = login.doLogin()
            continue
        system = system + 1
    galaxy = galaxy+1