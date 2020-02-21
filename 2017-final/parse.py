from record import Record
import pickle
import sys

def get_ints(f):
  return map(int, f.readline().strip().split())

with open(sys.argv[1] + '.in') as f:
  [H, W, R] = get_ints(f)
  [Pb, Pr, B] = get_ints(f)
  [br, bc] = get_ints(f)
  DATA = [list(f.readline().strip()) for i in range(H)]
