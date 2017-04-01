from record import Record
import pickle
import sys
from parse import H, W, R, Pb, Pr, B, br, bc, DATA

coverage = [[set() for _ in range(W)] for _ in range(H)]
sorted_coverage = list()

def inclusive_range(a, b, inc):
  if inc == 0:
    assert a == b
    return [a]
  else:
    assert inc == 1 or inc == -1
    return range(a, b+inc, inc)

for x in range(H):
  for y in range(W):
    if DATA[x][y] == '#':
      continue

    for i in range(max(0,x-R), min(x+R,H-1)+1):
      for j in range(max(0, y-R), min(y+R,W-1)+1):
        if DATA[i][j] == '.':
          coverage[x][y].add((i, j))

    for i in range(max(0,x-R), min(x+R,H-1)+1):
      for j in range(max(0, y-R), min(y+R,W-1)+1):
        if DATA[i][j] == '#':
          assert i != x or j != y

          dx = -1 if i < x else (1 if i > x else 0)
          dy = -1 if j < y else (1 if j > y else 0)

          if dx == 0:
            for k in range(max(0, min(H-1, x-R)), max(0, min(H-1, x+R))):
              for l in inclusive_range(j, max(0, min(W-1, j+R*dy)), dy):
                if (k,l) in coverage[x][y]:
                  coverage[x][y].remove((k,l))

          elif dy == 0:
            for k in inclusive_range(i, max(0, min(H-1, i+R*dx)), dx):
              for l in range(max(0, min(W-1, y-R)), max(0, min(H-1, y+R))):
                if (k,l) in coverage[x][y]:
                  coverage[x][y].remove((k,l))

          else:
            for k in inclusive_range(i, max(0, min(H-1, i+R*dx)), dx):
              for l in inclusive_range(j, max(0, min(W-1, j+R*dy)), dy):
                if (k,l) in coverage[x][y]:
                  coverage[x][y].remove((k,l))

    if coverage[x][y]:
      sorted_coverage.append((x,y, coverage[x][y]))

sorted_coverage.sort(key=lambda d: len(d[2]))

with open(sys.argv[1]+".1", 'wb') as f:
  pickle.dump((coverage, sorted_coverage), f)

