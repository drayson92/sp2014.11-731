import pickle
import codecs
import sys
import collections
from math import exp

def read_clusters(file):
  clusters = collections.defaultdict(set)
  for line in codecs.open(file, encoding='utf-8'):
    (bitstring, word, freq) = line.split()
    cluster_key = bitstring
    clusters[cluster_key].add(word) 
  return clusters

def read_fast_align_table(file):
  tbl = collections.defaultdict(dict)
  for line in codecs.open(file, encoding='utf-8'):
    f, e, lp = line.split()
    tbl[e][f] = exp(float(lp))
  return tbl


def make_cluster_model(word_counts, word_clusters):
	cluster_by_source = collections.defaultdict(dict)
	for cluster in word_clusters:
		total_count = 0
		for word in word_clusters[cluster]:
			total_count = total_count + word_counts[word]

		for word in word_clusters[cluster]:
			cluster_by_source[cluster][word] = word_counts[word] / total_count

	return cluster_by_source

def multiply_models(target_by_cluster, cluster_by_source):
	source_by_target = collections.defaultdict(dict)

	for target_word in target_by_cluster:
		for cluster in target_by_cluster[target_word]:
			cluster_score = target_by_cluster[target_word][cluster]
			for source_word in cluster_by_source[cluster]:
				source_by_target[source_word][target_word] = cluster_score * \
				cluster_by_source[cluster][source_word]

	
	return source_by_target

def read_phrase_model(filename):
	f = codecs.open(filename,'r', encoding='utf-8')
	source_by_target = collections.defaultdict(dict)
	for line in f:
		splits = line.split('|||')
		french_phrase = splits[0]
		englifh_phrase = splits[1]
		probs = splits[2]
		alignments = splits[3]
		rest = splits[4]
		probs_splits = probs.split()
		probs = (probs_splits[0], probs_splits[1])

		source_by_target[french_phrase][englifh_phrase] = (probs , alignments, rest)

	return source_by_target

def combine_phrase_models(cluster_model, phrase_model ,l):
	for key in cluster_model:
		if key not in phrase_model:
			phrase_model[key] = {}
			cluter_targets = cluster_model[key]
			sorted_targets = sorted(cluster_targets.iteritems(), key=operator.itemgetter(1))
			for i in xrange(len(sorted_targets)):
				target = sorted_targets[i]
				target_word = target[0]
				prob = float(target[1]) * l
				alignments = "0-0"
				rest = "1 1 1"
				phrase_model[key][target] = ( (prob , prob) , alignments, rest)

def write_phrase_model(filename,phrase_model):
	f = codecs.open('filename' , 'w', encoding='utf-8')
	for source in sorted(phrase_model):
		for target in sorted(phrase_model):
			((prob1, prob2) , alignments, rest) = phrase_model[source][target]
			outstring = ""
			outstring = outstring + source + "|||" + target + "|||"
			outstring = outstring + prob1 + " " + prob2 + "|||"
			outstring = outstring + alignments + "|||" + rest + "\n"

if __name__ == '__main__':
  cluster_file = sys.argv[2]
  cluster_aligntable_file = sys.argv[2]
  phrase_model_file = sys.argv[3]
  word_count_file = sys.argv[4]
  out_file = sys.argv[5]
  
  word_counts = pickle.load(open(word_count_file))

  print "calling read_clusters"
  clusters = read_clusters(cluster_file)

  print "calling read_fast_align_table"
  cluster_align_table = read_fast_align_table(cluster_aligntable_file)

  print "calling read_phrase_model"
  phrase_model = read_phrase_model(phrase_model_file)

  print "calling make_cluster_model"
  cluster_by_source = make_cluster_model(word_counts, clusters)

  print "calling multiply_models"
  source_by_target = multiply_models(cluster_align_table, cluster_by_source)

  print "calling combine_phrase_models"
  combine_phrase_models(source_by_target, phrase_model, 1.0)

  print "calling write_phrase_model"
  write_phrase_model(out_file, phrase_model)
