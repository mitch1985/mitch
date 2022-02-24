import requests
import re
from requests.api import request
import Util.login as login
import Util.planetenListe as planetenListe

sid = login.doLogin()
meinePlaneten = planetenListe.planeten(sid)
geschwindigkeit = input("Auf wieviel Prozent soll Produziert werden: ")

for planetenIndex in meinePlaneten:
    response = requests.get(f'http://www.earthlost.de/produktion.phtml?planetindex={planetenIndex}&speedperc={geschwindigkeit}&sid={sid}')
    if re.findall('Bot-Schutz',response.text):
        sid = login.doLogin()
        print (f'Bot-Schutz, Planet: {planetenIndex} wird wiederholt.')
        meinePlaneten.append(planetenIndex)
print("Ende")



