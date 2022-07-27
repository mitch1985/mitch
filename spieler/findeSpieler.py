import requests
import re

from requests.models import Response
import Util.login as login

sid = login.doLogin()
universe = 3
findeSpieler = 'Xenomorph'
 

galaxy = 1

while galaxy <= 25:
    system = 1
    while system <= 500:
        #Ich rufe ein System in einer Galaxy auf. Universum 1 interssant für mich
        url =f'http://www.earthlost.de/galaxy.phtml?universe={universe}&galaxy={galaxy}&system={system}&sid={sid}'
        response = requests.get(url)
        
        if re.findall('Bot-Schutz',response.text):
            sid = login.doLogin()
            continue

        #Alle Planis in dem System ausfiltern
        if re.findall(findeSpieler,response.text):
            print (f'Glaxy:{galaxy} und System:{system}')
       
        system = system + 1
    galaxy = galaxy+1
print (f'Ende bei Galaxy: {galaxy-1} und System: {system}')