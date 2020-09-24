import json


with open('data/league_paste.txt', 'r') as file:
    f = file.readlines()

data = {}

# loop thru the lines in f
current_owner = None
current_player = None
for l in f:
    line = l.strip()

    if line:
        if line == 'View Team' or line == 'Propose Trade':
            current_owner = None
            continue
        
        if current_owner is None:
            current_owner = line
            data[current_owner] = []
            continue

        if line in ['RB', 'WR', 'QB', 'TE', 'K', 'D/ST']:
            if current_player is not None:
                data[current_owner].append((current_player, line))
                current_player = None
            continue

        if len(line) % 2 == 0 and line[:len(line) // 2] == line[len(line) // 2:]:
            current_player = line[:len(line) // 2]

# save data
with open('data/data.json', 'w') as file:
    file.write(json.dumps(data))

# save the csv
with open('data/data.csv','w') as file:
    for owner in data.keys():
        for player in data[owner]:
            file.write(f"{owner},{player[0]},{player[1]}\n")
