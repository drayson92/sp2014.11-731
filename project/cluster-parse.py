#!/usr/bin/env python2

import sys
import codecs
from collections import defaultdict

trunc_len = 250

clusters = defaultdict(set)

for line in codecs.open(sys.argv[1], encoding='utf-8'):
  (word, bitstring, freq) = line.split()
  cluster_key = bitstring[:trunc_len]
  clusters[cluster_key].add(word)

for cluster in clusters.values():
  print cluster
