import requests
import re
import login as login
from bs4 import BeautifulSoup
import locale

#sid = login.doLogin()
locale.setlocale(locale.LC_ALL, '')

def spielerliste(sid):
    start=0
    data = []
    while start <= 1000:
        response = requests.get(f'http://www.earthlost.de/highscore.phtml?start={start}&sid={sid}').text
        if re.findall('Bot-Schutz',response):
            sid = login.doLogin()
            start=start-50
        soup = BeautifulSoup(response, "html.parser")
        tables = soup.find_all('table', attrs={'class':'nurzeilen'})
        x=0
        for table in tables:
            if x == 3 :
                rows = table.find_all('tr')
                rows.pop(0)
                for row in rows:
                    cols = row.find_all('td')
                    cols = [ele.text.strip() for ele in cols]
                    isDigit = str(cols[0]).replace('.','')
                    if isDigit.isdigit():
                        data.append(cols) # Get rid of empty values
            x=x+1
        start = start + 50
    return data