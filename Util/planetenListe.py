import sys
import requests
import re
from requests.api import request
#import login as login

def allePlanetenMitAttributen(sid):
    response = requests.get(f'http://www.earthlost.de/intro.phtml?sid={sid}')

    # Alle Planeten von mir als String 
    allePlaneten = re.findall('\[\[(.+?)\]\]',response.text)
    #allePlaneten[0] = str(allePlaneten[0]).replace("[","")
    allePlaneten[0] = str(allePlaneten[0]).replace("],[","|")
    allePlaneten[2] = str(allePlaneten[2]).replace("],[","|")
    #allePlaneten[2] = str(allePlaneten[2]).replace("[","")
    # Den String von allePlaneten von unnötigen Klammern befreien
    allePlanetenArray1 = allePlaneten[0].split("|")
    allePlanetenArray2 = allePlaneten[1].split("|")
    allePlanetenArray3 = allePlaneten[2].split("|")
    #allePlanetenArray2 = re.findall('\[(.+?)\]', allePlaneten[1])
    #allePlanetenArray3 = re.findall('\[(.+?)\]', allePlaneten[2])

    allePlanetenArray = allePlanetenArray1+allePlanetenArray2+allePlanetenArray3

    allePlanetenArray = [w.replace('"', '') for w in allePlanetenArray]
    allePlanetenArray = [w.split(',') for w in allePlanetenArray]

    return allePlanetenArray     

def ausgewaehltePlaneten(sid):
    print('---Hole Meine Planeten---')
    galaxyList = [int(item) for item in input("Galaxy : ").split()]
    systemList = [int(item) for item in input("System : ").split()]
    allePlanetenArray = allePlanetenMitAttributen(sid)    
    allePlanetenIndizes = []
    for planet in allePlanetenArray:
        #planetAttribute = planet.split(',')
        if (int(planet[1]) in galaxyList or planet[2] in systemList) or (len(galaxyList)==0 and len(systemList)==0):
            planetId = planet[0]
            planetId = str(planetId).replace('"','')
            allePlanetenIndizes.append(planetId)
    return allePlanetenIndizes

def allePlanetenIndex(sid):
    print('---Hole Alle Planeten---')
    allePlanetenArray = allePlanetenMitAttributen(sid)    
    allePlanetenIndizes = []
    for planet in allePlanetenArray:
        #planetAttribute = planet.split(',')
        planetId = planet[0]
        planetId = str(planetId).replace('"','')
        allePlanetenIndizes.append(planetId)
    return allePlanetenIndizes
    
def allePlanetenKoordinaten(sid):
    print('---Hole Alle Planetenkoordinaten---')
    allePlanetenArray = allePlanetenMitAttributen(sid)    
    allePlanetenKoords = []
    for planet in allePlanetenArray:
        #planetAttribute = planet.split(',')
        planetenKoordinaten = planet[0]+"|"+planet[1]+":"+ planet[2]+":"+ planet[3]
        planetenKoordinaten = str(planetenKoordinaten).replace('"','')
        allePlanetenKoords.append(planetenKoordinaten)
    return allePlanetenKoords

def allePlanetenKoordinatenUndId(sid):
    print('---Hole Alle Planetenkoordinaten und Ids---')
    allePlanetenArray = allePlanetenMitAttributen(sid)    
    planetenKoordinaten = dict()
    for planet in allePlanetenArray:
        #planetAttribute = planet.split(',')
        planetenKoordinaten[planet[0]] = [planet[1], planet[2], planet[3]]
        #planetenKoordinaten = str(planetenKoordinaten).replace('"','')
    return planetenKoordinaten
#sid = login.login()planetenKoordinaten
#planeten(sid)