import json


# get players
p = []
with open('data/data.json', 'r') as file:
    data = json.loads(file.read())
    for owner in data.keys():
        for player in data[owner]:
            p.append(player[0].lower())

# get the values
with open('data/value_paste.txt', 'r') as file:
    f = file.readlines()

player_values = {}
# loop thru f
for l in f:
    line = l.strip()
    
    # get player name
    if '\t' not in line:
        raise Exception('tab not in line')

    name, value = line.split('\t')
    player_values[name] = float(value)

    # check if in p
    if name not in p:
        print(f"{name} {value} -- not owned")

with open('data/player_values.json', 'w') as file:
    file.write(json.dumps(player_values))

# update data
data_new = {}
for owner in data.keys():
    data_new[owner] = []
    for player in data[owner]:
        if player[0].lower() in player_values.keys():
            value = player_values[player[0].lower()]
        else:
            value = 0
        data_new[owner].append([player[0], player[1], value])

with open('data/data.json', 'w') as file:
    file.write(json.dumps(data_new))
