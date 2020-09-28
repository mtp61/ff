from functions import getData, getInfo, getValue, getPlayerCombos, addPlayers, getScore


# constants
TRADE_SIZE_MAX = 2
MIN_DELTA_ME = 10
MIN_DELTA_OWNER = -5

info = getInfo()
data = getData()

# need to get each teams starting and bench value
team_info = []
team_rosters = {}
team_start_val = {}
team_bench_val = {}
for owner in data.keys():
    t = data[owner]
    value_lookup = {}
    
    roster = {
        "qb": [],
        "rb": [],
        "wr": [],
        "te": []
    }
    
    for p, pos, v in t:
        if pos == "QB":
            roster['qb'].append((p, v))
        elif pos == "RB":
            roster['rb'].append((p, v))
        elif pos == "WR":
            roster['wr'].append((p, v))
        elif pos == "TE":
            roster['te'].append((p, v))
    
    # sort
    roster['qb'].sort(key=lambda e:e[1])
    roster['rb'].sort(key=lambda e:e[1])
    roster['wr'].sort(key=lambda e:e[1])
    roster['te'].sort(key=lambda e:e[1])
    
    start_val, bench_val = getValue(roster)
    
    team_rosters[owner] = roster
    team_start_val[owner] = start_val
    team_bench_val[owner] = bench_val

    team_info.append({
        'owner': owner,
        'start_val': start_val,
        'bench_val': bench_val
    })

# print value info
team_info.sort(key=lambda e:-e['start_val'])
print("owner, start_val, bench_val")
start_val = {}
bench_val = {}
for d in team_info:
    print(f"{d['owner']}:{' '*(35 - len(d['owner']))}{d['start_val']}, {d['bench_val']}")
    start_val[d['owner']] = d['start_val']
    bench_val[d['owner']] = d['bench_val']

# get info about my team
me_roster = team_rosters[info['me']]
me_start_val = team_start_val[info['me']]
me_bench_val = team_bench_val[info['me']]
me_score = getScore(me_start_val, me_bench_val)
me_trades = {}
for i in range(1, TRADE_SIZE_MAX + 1):
    me_trades[i] = getPlayerCombos(me_roster, i)

# find possible trades with each owner (other than me)
trades = []
for owner in data.keys():
    if owner == info['me']:
        continue
    
    owner_roster = team_rosters[owner]
    owner_score = getScore(team_start_val[owner], team_bench_val[owner])

    # find owner trades
    owner_trades = {}
    for i in range(1, TRADE_SIZE_MAX + 1):
        owner_trades[i] = getPlayerCombos(owner_roster, i)

    # loop thru trades
    for k in range(1, TRADE_SIZE_MAX + 1):
        for mp, mros in me_trades[k]:
            for op, oros in owner_trades[k]:
                mros_new = addPlayers(mros, op)
                oros_new = addPlayers(oros, mp)
                
                msn, mbn = getValue(mros_new)
                osn, obn = getValue(oros_new)

                mscore_new = getScore(msn, mbn)
                oscore_new = getScore(osn, obn)

                if mscore_new - me_score >= MIN_DELTA_ME and oscore_new - owner_score >= MIN_DELTA_OWNER:
                    trades.append({
                        'with': owner,
                        'my_players': mp,
                        'owner_players': op,
                        'my_change': mscore_new - me_score,
                        'owner_change': oscore_new - owner_score
                    })
            
# print trades
trades.sort(key=lambda e:-e['my_change'])
for t in trades:
    print(f"+{int(t['my_change'])} with {t['with']} ({int(t['owner_change'])}): ", end='')
    for p, _, v in t['my_players']:
        print(f"{p} ({int(v)}) ", end='')
    print('for ', end='')
    for p, _, v in t['owner_players']:
        print(f"{p} ({int(v)}) ", end='')
    print()
