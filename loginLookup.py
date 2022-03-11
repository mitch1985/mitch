import requests
import re


url = 'http://forum.earthlost.de/ucp.php?mode=login'
parameter = {'username': 'Pudge', 'password' : 'oster', 'redirect':'index.php', 'login':'Anmelden'}

responseLogin = requests.post(url, data = parameter)
#SID auslesen
loginFail = re.findall('fehlgeschlagen',responseLogin.text)
if len(loginFail)>0:
    print("Fehlgeschlagen login")
else:
    print("Login")
