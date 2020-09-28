import json

from functions import getPlayers, getData, getInfo


MIN_VALUE = 3

r = getPlayers()
# just want the names
rostered = []
for p in r:
    rostered.append(p[0].lower())

# free agents

free_agents = []
with open('data/player_values.json', 'r') as file:
    player_values = json.loads(file.read())
for player in player_values.keys():
    if player not in rostered:
        free_agents.append([player, player_values[player]])

# print free agents in descending order of value, with value greater than the min
free_agents.sort(key=lambda e:-e[1])
print('Free agents:')
for p, v in free_agents:
    if v >= MIN_VALUE:
        print(f"{p} -- {v}")

# print your team
data = getData()
info = getInfo()
t = data[info['me']]
t.sort(key=lambda e:e[2])
print('\nMy team:')
for p, _, v in t:
    print(f"{p} -- {v}")

