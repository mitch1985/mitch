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

#Login und Planeten holen
sid = login.doLogin()
meinePlaneten = planetenListe.allePlanetenKoordinaten(sid)

#Jeden einzelnen Planenten durchlaufen
for planetenIndexAndKoords in meinePlaneten:
    planetenIndexAndKoordsSplit = planetenIndexAndKoords.split('|')
    einzelKoordinaten = planetenIndexAndKoordsSplit[1].split(':')
    if int(einzelKoordinaten[0]) < 10:
        einzelKoordinaten[0] = "0" + einzelKoordinaten[0]
    if int(einzelKoordinaten[1]) < 10:
        einzelKoordinaten[1] = "00" + einzelKoordinaten[1]
    if int(einzelKoordinaten[1]) < 100 and int(einzelKoordinaten[1]) > 10:
        einzelKoordinaten[1] = "0" + einzelKoordinaten[1]
    if int(einzelKoordinaten[2]) < 10:
        einzelKoordinaten[2] = "0" + einzelKoordinaten[2]
    
    print (f'Index: {planetenIndexAndKoordsSplit[0]}')
    print (f'Koords: {planetenIndexAndKoordsSplit[1]}')
    isBotschutz = True
    while isBotschutz:
        response = requests.get(f'http://www.earthlost.de/construction.phtml?planetindex={planetenIndexAndKoordsSplit[0]}&sid={sid}').text
        hrFlotteErstellen = {'sid' : sid, 'newfleetname' : 'HR '+einzelKoordinaten[0]+':'+einzelKoordinaten[1]+':'+einzelKoordinaten[2]}
        response = requests.post(f'http://www.earthlost.de/flotten.phtml?', data=hrFlotteErstellen).text
        if (isBotSchutzOderNichtEingeloggt(response)):
            sid = login.doLogin()
            continue
        isBotschutz=False
print("Ende")
