#!/usr/bin/env python3
import sys
from collections import *
import pickle
import math

EarlyLibrary = namedtuple('EarlyLibrary', 'id books signup throughput')
Library = namedtuple('Library', 'id books sorted_books schedule signup throughput scoring')
Data = namedtuple('Data', 'B L DAYS BOOKS LIBS')

def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))

IN = sys.stdin
B, L, DAYS = map(int, IN.readline().split())
BOOKS = list(map(int, IN.readline().split()))

parent = defaultdict(list)

def parse_library(i):
    N, T, M = map(int, IN.readline().split())
    books = list(map(int, IN.readline().split()))
    for b in books:
        parent[b].append(i)

    return EarlyLibrary(i, books, T, M)

LIBS = [parse_library(i) for i in range(L)]
storage = defaultdict(list)

for i, ps in parent.items():
    l = min(ps, key=lambda l: len(storage[l]))
    storage[l].append(i)

BOOKS_W = [BOOKS[b] * BOOKS[b] / (math.sqrt(len(parent[b])) + 1) for b in range(len(BOOKS))]
NEW_LIBS = []
for l in LIBS:
    # books = storage[l.id]
    books = l.books
    sorted_books = sorted(books, key=lambda b: -BOOKS_W[b])
    chunked_books = iter(list(chunks(sorted_books, l.throughput)))
    scoring = [0] * l.signup
    score = 0
    try:
        for j in range(DAYS - l.signup):
            score += sum(map(lambda b: BOOKS_W[b], next(chunked_books)))
            scoring.append(score)
    except StopIteration:
        while j < DAYS - l.signup:
            scoring.append(score)
            j += 1

    scoring.reverse()
    NEW_LIBS.append(Library(l.id, books, sorted_books, None, l.signup, l.throughput, scoring))

with open(sys.argv[1],'wb') as f:
    pickle.dump(Data(B, L, DAYS, BOOKS, NEW_LIBS), f)

