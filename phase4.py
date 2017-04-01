from collections import deque
from parse import H, W, R, Pb, Pr, B, br, bc, DATA
import sys
import pickle

(routers, backbone) = pickle.load(open(sys.argv[1] + ".3", "rb"))

print(len(backbone)-1)

backbone = deque(backbone)

CONNECTED = [[False for _ in range(W)] for _ in range(H)]
CONNECTED[br][bc] = True
while backbone:
    (x, y) = backbone.popleft()
    if x == br and y == bc:
        continue
    valid = False
    for i in range(max(0, x-1), min(x+2, H)):
        for j in range(max(0, y-1), min(y+2, W)):
            if CONNECTED[i][j]:
                valid = True
                break
    if valid:
        CONNECTED[x][y] = True
        print(x, y)
    else:
        backbone.append((x,y))

print(len(routers))
for (x, y) in routers:
    print(x, y)
