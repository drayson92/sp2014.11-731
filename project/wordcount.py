#!/usr/bin/env python2

import sys
from collections import defaultdict
import pickle

counts = defaultdict(int)

fn = sys.argv[1]
out = sys.argv[2]
for line in open(fn):
  words = line.split()
  for w in words:
    counts[w] += 1

pickle.dump(counts, open(sys.argv[2], 'w'))
