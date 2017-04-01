import pickle
import sys

from parse import H, W, R, Pb, Pr, B, br, bc, DATA

(coverage, sorted_coverage) = pickle.load(open(sys.argv[1] + ".1", "rb"))
routers = list()

sorted_coverage.sort(key=lambda d: len(d[2]))
print("Sorted")

PRINT=list(map(lambda row: list(map(lambda x: x+"   ", row)), DATA))
while sorted_coverage:
  (x, y, cov) = sorted_coverage.pop()
  if len(cov) == 0:
    break

  routers.append((x,y))

  PRINT[x][y] = "%03d " % len(cov)

  for i in range(max(0,x-2*R), min(x+2*R,H-1)+1):
    for j in range(max(0, y-2*R), min(y+2*R,W-1)+1):
      if i == x and j == y:
        continue

      coverage[i][j] -= cov

  sorted_coverage.sort(key=lambda d: len(d[2]))

for (x,y) in routers:
  for (i,j) in coverage[x][y]:
    if PRINT[i][j] == '.   ':
      PRINT[i][j] = "*   "

# for row in PRINT:
  # print(''.join(row))

print("Routers: " + str(len(routers)))

with open(sys.argv[1]+".2", 'wb') as f:
  pickle.dump(routers, f)
