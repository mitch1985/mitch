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

isBotschutz = True
while isBotschutz:
    response = requests.get(f'http://www.earthlost.de/flotten.phtml?showview=114008&sid={sid}').text
    if isBotSchutzOderNichtEingeloggt(response):
        sid = login.doLogin()
        continue
    flottenIds = re.findall("OPTION value=\"(.+?)\"", response)
    for flottenId in flottenIds:
        #Kolos
        #hrFlotteVerstaerken = {'sid' : sid, 'ship8' : 8, 'addtofleet':flottenId, 'max':9999}
        hrFlotteVerstaerken = {'sid' : sid, 'ship4' : 20000, 'addtofleet':flottenId, 'max':10}
        responseFlottenVerstaerkung = requests.post(f'http://www.earthlost.de/flotten.phtml?', data=hrFlotteVerstaerken).text
        if (isBotSchutzOderNichtEingeloggt(responseFlottenVerstaerkung)):
            sid = login.doLogin()
            flottenIds.append(flottenId)
            continue
        #sid=npqcd89eqoqr88at9igvh8ak44&ship3=0&ship4=20000&ship6=0&ship8=0&ship18=0&ship20=0&addtofleet=183507383&max=9999&sid=npqcd89eqoqr88at9igvh8ak44
    isBotschutz=False