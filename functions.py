import json
import itertools
import copy


# constants
ALPHA = 2  # start val weight


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


def getValue(roster):
    """
    get the score from a roster where the roster is a dict:
     - qb
     - rb
     - wr
     - te
    each of these are sorted lists of tuples (name, value)
    returns start value, bench value
    """

    roster = copy.deepcopy(roster)  # inefficient

    start_val = 0
    bench_val = 0

    # get s val
    for _ in range(min(1, len(roster['qb']))):
        start_val += roster['qb'].pop()[1]
    for _ in range(min(2, len(roster['rb']))):
        start_val += roster['rb'].pop()[1]
    for _ in range(min(2, len(roster['wr']))):
        start_val += roster['wr'].pop()[1]
    for _ in range(min(1, len(roster['te']))):
        start_val += roster['te'].pop()[1]

    flex = []
    flex.extend(roster['rb'])
    flex.extend(roster['wr'])
    flex.extend(roster['te'])
    flex.sort(key=lambda e:e[1])
    for _ in range(min(1, len(flex))):
        start_val += flex.pop()[1]

    # bench val
    for _, v in roster['qb']:
        bench_val += v
    for _, v in roster['rb']:
        bench_val += v
    for _, v in roster['wr']:
        bench_val += v
    for _, v in roster['te']:
        bench_val += v

    return start_val, bench_val


def getPlayerCombos(roster, n):
    """
    get all combos of n players
    returns a list of tuples where each tuple is
     - a list of the players being traded
        - (player, pos, val)
     - the roster without the players
    """

    # get the players
    players = []
    for key in roster.keys():
        for p, v in roster[key]:
            players.append((p, key, v))
    
    # get combos of players
    player_combos = itertools.combinations(players, n)

    # get the roster for each combo and add to data
    data = []
    for combo in player_combos:
        combo_roster = copy.deepcopy(roster)

        for name, pos, _ in combo:
            for n, (p, _) in enumerate(combo_roster[pos]):
                if p == name:
                    del combo_roster[pos][n]
                    break

        data.append((combo, combo_roster))

    return data


def getScore(start_val, bench_val):
    """
    returns the score bases on start val and bench val
    """

    return ALPHA * start_val + bench_val


def addPlayers(roster, players):
    """
    returns the roster with the players added
    """

    roster = copy.deepcopy(roster)

    to_sort = []
    for p, pos, v in players:
        if pos not in to_sort:
            to_sort.append(pos)
        roster[pos].append((p, v))

    for pos in to_sort:
        roster[pos].sort(key=lambda e:e[1])

    return roster
