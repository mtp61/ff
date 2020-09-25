import json


def getInfo():
    """
    returns info
    """

    with open('info.json', 'r') as file:
        info = json.loads(file.read())

    return info
    

def getData():
    """
    returns data
    """

    with open('data/data.json', 'r') as file:
        data = json.loads(file.read())
    
    return data


def getPlayers():
    """
    returns all rostered players
    """
    p = []
    data = getData()

    for owner in data.keys():
        for player in data[owner]:
            p.append(player)

    return p



