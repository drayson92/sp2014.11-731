#!/usr/bin/env python2

import sys
import codecs
from nltk.tokenize.regexp import WordPunctTokenizer

src_file, target_file = sys.argv[1:3]
src_f = codecs.open(src_file, encoding='utf-8')
target_f = codecs.open(target_file, encoding='utf-8')
for (s_s, t_s) in zip(src_f, target_f):
  s_t = u' '.join(WordPunctTokenizer().tokenize(s_s))
  t_t = u' '.join(WordPunctTokenizer().tokenize(t_s))
  print u"{0} ||| {1}".format(s_t,t_t).encode('ascii', 'ignore')
