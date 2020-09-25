from functions import getData, getInfo


info = getInfo()
data = getData()

# need to get each teams starting and bench value
team_info = []
for owner in data.keys():
    t = data[owner]
    value_lookup = {}
    qb = []
    rb = []
    wr = []
    te = []
    total_value = 0
    for p, pos, v in t:
        total_value += v
        value_lookup[p] = v
        if pos == "QB":
            qb.append(p)
        elif pos == "RB":
            rb.append(p)
        elif pos == "WR":
            wr.append(p)
        elif pos == "TE":
            te.append(p)
    # sort
    qb.sort(key=lambda e:value_lookup[e])
    rb.sort(key=lambda e:value_lookup[e])
    wr.sort(key=lambda e:value_lookup[e])
    te.sort(key=lambda e:value_lookup[e])
    
    starters = []
    for _ in range(info['roster']['qb']):
        starters.append(qb.pop())
    for _ in range(info['roster']['rb']):
        starters.append(rb.pop())
    for _ in range(info['roster']['wr']):
        starters.append(wr.pop())
    for _ in range(info['roster']['te']):
        starters.append(te.pop())
    flex = []
    flex.extend(rb)
    flex.extend(wr)
    flex.extend(te)
    flex.sort(key=lambda e:value_lookup[e])
    for _ in range(info['roster']['flex']):
        starters.append(flex.pop())

    starter_value = 0
    for p in starters:
        starter_value += value_lookup[p]

    team_info.append({
        'owner': owner,
        'start_val': starter_value,
        'bench_val': total_value - starter_value
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

# find possible trades with each owner (other than me)
trades = []
for owner in data.keys():
    if owner == info['me']:
        continue



    break 


# print trades
for trade in trades:
    print(trade)
