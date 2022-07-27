import requests
import re


def doLogin():
    print("starte login")
    try:
        y = 0
        captcha = 0
        while y < 50:
            #Login Daten senden
            urlLogin = 'http://www.earthlost.de/login.phtml'
            loginDaten = {'user': 'fr34kscht@gmail.com', 'pwd': 'ostern'}

            responseLogin = requests.post(urlLogin, data=loginDaten)
            #SID auslesen
            sids = re.findall('sid=(.+?)"', responseLogin.text)
            sid = sids[0]

            x = 0
            while x < 4:
                #Aufruf des Botschutz fuer Sehbehinderte und einfach einen Leer-Code schicken
                urlLoginKlick = 'http://www.earthlost.de/intro.phtml?blind=1'
                loginKoords = {'sid': sid, 'captcha_id': captcha, 'code': ''}
                responseLoginErfolg = requests.post(urlLoginKlick,
                                                    data=loginKoords).text
                if responseLoginErfolg.__contains__('Pudge'):
                    break
                else:
                    captchas = re.findall(
                        'name=\"captcha_id\" value=\"(.+?)\"',
                        responseLoginErfolg)
                    captcha = int(captchas[1])
                x = x + 1
            if x < 4:
                break
            y = y + 1
        return sid
    except:
        print("Fehler Internet.")
