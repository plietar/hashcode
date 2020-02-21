#!/usr/bin/env python3
import sys
from collections import *
import pickle
from itertools import permutations

Library = namedtuple('Library', 'id books sorted_books schedule signup throughput scoring')
Data = namedtuple('Data', 'B L DAYS BOOKS LIBS')

with open(sys.argv[1],'rb') as f:
    data = pickle.load(f)

print("Loaded ", sys.argv[1], file=sys.stderr)

B, L, DAYS, BOOKS, LIBS = data

book_feeds = [iter(l.sorted_books) for l in LIBS]

pending_days = None
pending_library = None

registered = set()
remaining = set(range(L))

registraton_schedule = []
sending_schedule = defaultdict(list)

submitted = set()
for d in range(DAYS):
    if d % 100 == 0:
        print(sys.argv[1], d)

    if pending_library is not None:
        pending_days -= 1
        if pending_days == 0:
            registered.add(pending_library.id)
            pending_library = None

    dead_libraries = set()
    for i in registered:
        l = LIBS[i]
        try:
          n = 0
          while n < l.throughput:
              book = next(book_feeds[l.id])
              if book not in submitted:
                  submitted.add(book)
                  n += 1
                  sending_schedule[i].append(book)

        except StopIteration:
            dead_libraries.add(i)

    registered -= dead_libraries

    if pending_library is None and remaining:
        # selected_i = max(remaining, key=lambda i: LIBS[i].scoring[d])
        # selected_i = max(remaining, key=lambda i: LIBS[i].scoring[d] / (LIBS[i].signup * LIBS[i].signup))
        N = min(10, len(remaining))
        indices = sorted(remaining, key=lambda i: LIBS[i].scoring[d] / LIBS[i].signup)[-N:]
        perms = permutations(indices, len(indices))
        def perm_score(p):
            s = 0
            d2 = d
            for i in p:
                if d2 < len(LIBS[i].scoring):
                    s += LIBS[i].scoring[d2]
                d2 += LIBS[i].signup
            return s
        selected_i = max(perms, key=perm_score)[0]

        # selected_i = max(remaining, key=lambda i: LIBS[i].scoring[d] / LIBS[i].signup)
        # selected_i = max(remaining, key=lambda i: (- LIBS[i].signup, LIBS[i].scoring[d]))
        if LIBS[selected_i].scoring[d] > 0:
            pending_library = LIBS[selected_i]
            remaining.remove(selected_i)
            pending_days = pending_library.signup
            registraton_schedule.append(selected_i)

with open(sys.argv[2], "w") as f:
  print(len(registraton_schedule), file=f)
  for i in registraton_schedule:
      print(i, len(sending_schedule[i]), file=f)
      print(*sending_schedule[i], file=f)
  
