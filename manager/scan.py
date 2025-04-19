from net import *

neighbors = []
print("Scanning all neighbors...")
while True:
    for neighbor in scan():
        if neighbor['name'] not in [neighbor['name'] for neighbor in neighbors]:
            neighbors.append(neighbor)
        else:
            for nb in neighbors:
                if nb['name'] == neighbor['name']:
                    nb['rssi'] = neighbor['rssi']
    neighbors.sort(key=lambda neighbor: neighbor['rssi'], reverse=True)
    print("\033c")
    print("NEIGHBORS:")
    for c, neighbor in enumerate(neighbors):
        print(c + 1, '\t', neighbor['name'], '\t', neighbor['rssi'])
    print(json.dumps([cricket['name'] for cricket in neighbors]))
    time.sleep(1)
