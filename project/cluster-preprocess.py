#!/usr/bin/env python2

import sys
import codecs
import os
import time

def parse_wcluster_output(out_file):
  clusters = {}
  for line in codecs.open(out_file, encoding='utf-8'):
    (bitstring, word, freq) = line.split()
    clusters[word] = bitstring

  return clusters

def words_to_clusters(in_file, out_file, clusters):
  f = codecs.open(out_file, 'a', encoding='utf-8')
  for line in codecs.open(in_file, encoding='utf-8'):
    words = line.split()
    new_words = [clusters[w] for w in words]
    new_line = u' '.join(new_words) + '\n'
    f.write(new_line)

def preprocess_file(in_file, out_file, remove_stopwords=False):
  f = codecs.open(out_file, 'a', encoding='utf-8')
  for line in codecs.open(in_file, encoding='utf-8'):
    words = line.strip().split()
    if remove_stopwords:
      #TODO
      pass
    new_line = u' '.join(words)
    f.write(new_line)

if __name__ == '__main__':
  in_file = sys.argv[1]
  cluster_file = sys.argv[2]
  out_file = sys.argv[3]

  clusters = parse_wcluster_output(cluster_file)

  words_to_clusters(in_file, out_file, clusters)
