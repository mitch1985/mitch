import requests
import re
from requests.api import request
import Util.login as login
import time
from bs4 import BeautifulSoup
import locale
from datetime import datetime, timedelta

sid = login.doLogin()
locale.setlocale(locale.LC_ALL, '')
dictAngreifer = {}
dictVerteidiger = {}
dictSchilde = {}
locale.setlocale(locale.LC_ALL, '')

account = input("Account-Name : ")


#/news.phtml?time=1630773348&sid=
x=0
while x < 9:
    time =  datetime.now() - timedelta(x)
    x=x+1
    response = requests.get(f'http://www.earthlost.de//news.phtml?time={time.timestamp()}&sid={sid}').text
    if re.findall('Bot-Schutz',response):
        #print("BOT-Schutz")
        x=x-1
        sid = login.doLogin()
    soup = BeautifulSoup(response, "html.parser")
    all_text = '|'.join(soup.findAll(text=True))
    kaempfe = re.findall(f'Kampf um einen Planeten(.+?)(vs.)(.+?)\|PopUp\|(.+?):', all_text)

    for kampf in kaempfe:
        angreiferSchilde = kampf[0]
        schilde = re.findall('\(Verluste: (.+?)\)',angreiferSchilde)
        schilde = str(schilde[0]).replace('.','')
        dictSchilde[schilde]=f'{time.day}.{time.month}'
        alleAngreifer = str(angreiferSchilde).split('|')
        uhrzeit = re.findall('\d{4}-\d{2}-\d{2} (.+)', kampf[3])
        #print (f'Schilde: {schilde}')
        alleAngreifer.pop(0)
        for angreifer in alleAngreifer:
            #print (f'Angreifer: {angreifer}')
            if angreifer in dictAngreifer and angreifer != '' and angreifer != ' ':
                zaehler = dictAngreifer.get(angreifer)
                dictAngreifer[angreifer] = zaehler+1
            #if angreifer == account:
                #dictAngreifer[angreifer] = time.hour
            #    print (f'{uhrzeit[0]}')
            else:
                dictAngreifer[angreifer]=1
        
        alleVerteidiger = kampf[2]
        alleVerteidiger = str(alleVerteidiger).split('|')
        for verteidiger in alleVerteidiger:
            if verteidiger in dictVerteidiger and verteidiger is not '' and verteidiger is not ' ':
                zaehler = dictVerteidiger.get(verteidiger)
                dictVerteidiger[verteidiger] = zaehler+1
            else:
                dictVerteidiger[verteidiger]=1

print (f'Angreifer: {dict(sorted(dictAngreifer.items(), key=lambda item: item[1]))}')
#print (f'Verteidiger: {dict(sorted(dictVerteidiger.items(), key=lambda item: item[1]))}')
#print (f'Schilde: {dict(sorted(dictSchilde.items(), key=lambda item: item[0]))}')

