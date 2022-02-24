import requests
import re
from requests.api import request
import Util.login as login
from bs4 import BeautifulSoup
import locale

sid = login.doLogin()

response = requests.get(f'http://www.earthlost.de/messages.phtml?view=4&sid={sid}')
spionageBerichteIds = re.findall('read\=(.+?)\&',response.text)
locale.setlocale(locale.LC_ALL, '')

def schiffsklasseAuslesen(schiff):
    anzahl = re.findall(f'{schiff}(.+?)[A-Za-z]', all_text)
    if len(anzahl)>0:
        return int(str(anzahl[0]).replace('.',''))
    else:
        return 0

for spionageBerichtId in spionageBerichteIds:
    response = requests.get(f'http://www.earthlost.de/messages.phtml?read={spionageBerichtId}&sid={sid}')
    soup = BeautifulSoup(response.text, "html.parser")
    all_text = ''.join(soup.findAll(text=True))
    hrs = schiffsklasseAuslesen("Handelsriese")
    nouls= schiffsklasseAuslesen("Noulon")
    violo= schiffsklasseAuslesen("Violo")
    narubu= schiffsklasseAuslesen("Narubu")
    bloods= schiffsklasseAuslesen("Bloodhound")
    neos= schiffsklasseAuslesen("Neomar")
    zems= schiffsklasseAuslesen("Zemar")
    grandor= schiffsklasseAuslesen("Grandor")
    snatcher= schiffsklasseAuslesen("Snatcher")
    retter= schiffsklasseAuslesen("Rettungsschiff")

    if hrs>100000 or nouls >200000 or violo > 100000 or narubu > 100000 or bloods > 10000 or neos > 10000 or zems > 1000 or grandor > 1000 or snatcher > 1000000:
        zielObjekt = re.findall('wurde ausspioniert Planet (.+?) wurde', all_text)
        print (f'{zielObjekt}')
        print (f'HRs:{hrs:n}') if hrs > 0 else 0
        print (f'Noulon:{nouls:n}') if nouls > 0 else 0
        print (f'Violo:{violo:n}') if violo > 0 else 0
        print (f'Narubu:{narubu:n}') if narubu > 0 else 0
        print (f'Bloods:{bloods:n}') if bloods > 0 else 0
        print (f'Neos:{neos:n}') if neos > 0 else 0
        print (f'Zems:{zems:n}') if zems > 0 else 0
        print (f'Grandor:{grandor:n}') if grandor > 0 else 0
        print (f'Snatcher:{snatcher:n}')  if snatcher > 0 else 0
        print (f'Retter:{retter:n}') if retter > 0 else 0
        print (f'-----------------------------------')
    if re.findall('Bot-Schutz',response.text):
        sid = login.doLogin()
        spionageBerichteIds.append(spionageBerichtId)
print("Ende")