import requests
import re
import Util.login as login

sid = login.doLogin()

x=0
while x < 1000:
    url =f'http://www.earthlost.de/messages.phtml'
    requests.get(url)
    nachricht = {'receiver': 'FanClub','subject' : 'test', 'user_eingabe' :'test', 'sid' : sid}
    response = requests.post(url, data = nachricht)
    if re.findall('Bot-Schutz',response.text):
        sid = login.doLogin()
    else:
        x=x+1
    #sid=dp5pohrlvdsa0204o917fhjtv1&receiver=FanClub&subject=Betreff&user_eingabe=test&sid=dp5pohrlvdsa0204o917fhjtv1