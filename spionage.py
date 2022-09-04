import requests
import re
import login as login

sid = login.doLogin()
universe = 3
nichtSpionieren = ['Amyntas', 'Goldconny123', 'Maulwurf']

galaxy = 25

#355870 - Tor in Uni3
#Fuer Uni3
requests.get(f'http://www.earthlost.de/produktion.phtml?planetindex=355870&speedperc=200&sid={sid}')

while galaxy <= 25:
    system = 1
    while system <= 100:
        #Ich rufe ein System in einer Galaxy auf. Universum 1 interssant für mich
        url =f'http://www.earthlost.de/galaxy.phtml?universe={universe}&galaxy={galaxy}&system={system}&sid={sid}'
        r = requests.get(url)
        
        #Alle Planis in dem System ausfiltern
        planetenListe = re.findall('drawPlanet(.+?)\);',r.text)
        #Ist die Planiliste leer, war es wohl der Bot-Schutz. Neu einloggen und noch mal die seite Scannen
        if len(planetenListe)==0:
            sid = login.doLogin()
            #requests.get(f'http://www.earthlost.de/produktion.phtml?planetindex=355870&speedperc=100&sid={sid}')
            continue

        #Wieviele Planis hat das System
        planetenAnzahlImSystem=len(planetenListe)
        besiedeltePlaneten=[]
        #Alle Planis im System durchlaufen und schauen, welche Planis sind besiedelt
        for planet in planetenListe:
            planetAttribute = planet.split(',')
            try:
                besitzer = str(planetAttribute[3]).replace('"','').strip()
                if int(planetAttribute[7]) != 0 and (besitzer not in nichtSpionieren ):
                    besiedeltePlaneten.append(planetAttribute[2])
                    spioid=planetAttribute[15]
            except:
                print ("Fehler beim einlsesen der besiedelten Planeten.")
        
        print (f'Das System:{system} hat {planetenAnzahlImSystem} Planeten, davon sind {len(besiedeltePlaneten)} Planeten besiedelt.')
        #Alle besiedelten Planis ausspionieren
        for planet in besiedeltePlaneten:
            try:
                #requests.get(f'http://www.earthlost.de/produktion.phtml?planetindex=355870&speedperc=100&sid={sid}')
                url =f'http://www.earthlost.de/galaxy.phtml?spio={spioid}&gotouniverse=3&g={galaxy}&s={system}&p={planet}&sid={sid}&ajax=1'
                r = requests.get(url)
                spioids = re.findall('spioid =(.+?)\;',r.text)
                if len(spioids)==0:
                    sid = login.doLogin()
                    #requests.get(f'http://www.earthlost.de/produktion.phtml?planetindex=355870&speedperc=100&sid={sid}')
                    continue
                spioid= spioids[0]
            except:
                print ("Fehler beim Spionieren.")
        system = system + 1
    galaxy = galaxy+1
print (f'Ende bei Galaxy: {galaxy-1} und System: {system}')