import re

def isBotSchutzOderNichtEingeloggt(response):
    if re.findall('eingeloggt', response): print(f'Nicht eingeloggt')
    if re.findall('Bot-Schutz', response): print(f'Bot-Schutz')
    return re.findall('Bot-Schutz', response) or re.findall(
        'eingeloggt', response)