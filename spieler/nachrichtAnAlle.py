import requests
import re
import Util.login as login
import Util.listeSpieler as spielerListe

sid = login.doLogin()
listeAllerSpieler = spielerListe.spielerliste(sid)


x=0
for spieler in listeAllerSpieler:
    url =f'http://www.earthlost.de/messages.phtml'
    requests.get(url)
    nachricht = {f'receiver': {spieler[1]},'subject' : 'Aufklaerung', 'user_eingabe' :'Hallo, danke fuer die vielen Rueckmeldungen und Spenden, Drohungen und Beleidigungen. EL ist scheinbar am Leben. :) Es ist viel mehr Response zusammengekommen als Vermutet. Ein Teil des eingenommenen Cashs habe ich schon wieder verteilt an kleinere Spieler. Ihr braucht nicht Spenden, koennt es aber natuerlich. Es ist alles gekommen, von 1 Cash ueber 666 Cash bishin zu 1g Cash. Danke fuer die Hilfe und die zum Teil netten Unterhaltungen. Eine Liste? helleye, b4rn3y,Komposter, Matchball, Caprisonne, jumpy, beerx, PatrickStar, MotherM, Exatmisi, EM_KAY, puerzel, BigBadButtermilch (Heil dem Dino), Laxy, Hetfield, Amy_lee, los7inc, hbunskilled,lordprotektor, go_imperator, zerocks, gamblingwhizard, rule. gruss Pudge ', 'sid' : sid}
    response = requests.post(url, data = nachricht)
    print (f'Spieler: {spieler[1]}')
    if re.findall('Bot-Schutz',response.text):
        sid = login.doLogin()
    else:
        x=x+1
    #sid=dp5pohrlvdsa0204o917fhjtv1&receiver=FanClub&subject=Betreff&user_eingabe=test&sid=dp5pohrlvdsa0204o917fhjtv1
print("Ende")