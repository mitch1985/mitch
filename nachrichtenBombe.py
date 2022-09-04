import requests
import re
import login as login

sid = login.doLogin()

x=0
while True:
    url =f'http://www.earthlost.de/messages.phtml'
    requests.get(url)
    nachricht = {'receiver': 'Pudge','subject' : 'test', 'user_eingabe' :'test', 'sid' : sid}
    response = requests.post(url, data = nachricht)
    if re.findall('Bot-Schutz',response.text):
        sid = login.doLogin()