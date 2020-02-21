import pickle
import sys
from steiner import process_routers

from parse import H, W, R, Pb, Pr, B, br, bc, DATA

#(coverage, _) = pickle.load(open(sys.argv[1] + ".1", "rb"))
routers = pickle.load(open(sys.argv[1] + ".2", "rb"))
while len(routers) * Pr > B:
  routers.pop()

deleted_routers = list()
while True:
  print("Connecting %d routers" % len(routers))
  mst, size = process_routers(routers + [(br,bc)])

  backbone = set()
  for (_, (x1, y1), (x2, y2)) in mst:
    i = x1
    j = y1

    dx = -1 if x2 < x1 else 1
    dy = -1 if y2 < y1 else 1

    while i != x2 and j != y2:
      backbone.add((i,j))
      i += dx
      j += dy

    while i != x2:
      backbone.add((i,j))
      i += dx

    while j != y2:
      backbone.add((i,j))
      j += dy

    backbone.add((i,j))

  cost = len(routers) * Pr + len(backbone) * Pb - 1

  print("%d / %d -> %d" % (cost, B, B - cost))
  if B - cost == 105:
      break
  if cost <= B:
    if B - cost < Pr or not deleted_routers:
      break
    else:
      routers.append(deleted_routers.pop())
  else:
    extra = (cost - B) // Pr
    N = len(routers)
    deleted_routers = routers[-extra:][::-1]
    routers = routers[:-extra]
    assert len(routers) + len(deleted_routers) == N

for (i,j) in backbone:
    DATA[i][j] = 'b'

for (i,j) in routers:
    DATA[i][j] = 'R'

with open(sys.argv[1]+".3", 'wb') as f:
  pickle.dump((routers, backbone), f)


# for row in DATA:
  # print(''.join(row))
