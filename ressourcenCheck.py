import requests
import login as login
import botschutz as botschutz
import planetenListe as planiListe
# from Util import findeKolonisierbarePlanetenMitPunkten as findKoloPlanis
from bs4 import BeautifulSoup
from keep_alive import keep_alive

print("los gehts")
keep_alive()
# Login
sid = login.doLogin()
galaxy = 1

planis = planiListe.allePlanetenIndex(sid)
for plani in planis:
    isAllesLaeuftNormal = True
    while isAllesLaeuftNormal:
        responsePlanet = requests.get(
            f'http://www.earthlost.de/construction.phtml?planetindex={plani}&sid={sid}'
        ).text
        if botschutz.isBotSchutzOderNichtEingeloggt(responsePlanet):
            print(
                "Botschutz oder nicht Eingeloggt in der Methode: isHqAusbauNoetig"
            )
            sid = login.doLogin()
            continue
        isAllesLaeuftNormal = False
        soup = BeautifulSoup(responsePlanet, "html.parser")
        links = soup.find_all('div', attrs={'class': 'resource_header2_2'})
        for td in links[0].find_all('td'):
            if td.text:
                print(f'hier zahlen: {td.text}')