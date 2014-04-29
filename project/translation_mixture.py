import pickle
import codecs
import collections
from math import exp

def read_clusters(file):
  clusters = collections.defaultdict(set)
  for line in codecs.open(file, encoding='utf-8'):
    (bitstring, word, freq) = line.split()
    cluster_key = bitstring[:trunc_len]
    clusters[cluster_key].add(word) 
  return clusters

def read_fast_align_table(file)
  tbl = collections.defaultdict(dict)
  for line in codecs.open(file, encoding='utf-8'):
    f, e, lp = line.split()
    tbl[e][f] = exp(lp)
  return tbl

def cluster_model(word_counts, word_clusters):
	cluster_by_source = {}
	for cluster in word_clusters:
		total_count = 0
		for word in word_clusters[cluster]:
			total_count = total_count + word_counts[word]

		cluster_by_source[cluster] = {}
		for word in word_clusters[cluster]:
			cluster_by_target[cluster][word] = word_counts[word] / total_count

	return cluster_by_source

def multiply_models(target_by_cluster, cluster_by_source):
	source_by_target = {}
	for target_word in target_by_cluster:
		for cluster in target_by_cluster[target_word]:
			cluster_score = target_by_cluster[target_word][cluster]
			for source_word in cluster_by_source[cluster]:
				source_by_target[source_word][target_word] = cluster_score * \
				cluster_by_source[cluster][source_word]
	
	return source_by_target

def read_phrase_model(filename):
	f = open('filename','r')
	source_by_target = {}
	for line in f:
		splits = f.split('|||')
		french_phrase = splits[0]
		englifh_phrase = splits[1]
		probs = splits[2]
		alignments = splits[3]
		rest = splits[4]
		probs_splits = probs.split()
		probs = (probs_splits[0], probs_splits[1])

		source_by_target[french_phrase][englifh_phrase] = (probs , alignments, rest)

	return source_by_target

def combine_phrase_models(cluster_model, phrase_model , lambda , num_terms):
	
	for key in cluster_model:
		if key not in phrase_model:
			phrase_model[key] = {}
			cluter_targets = cluster_model[key]
			sorted_targets = sorted(cluster_targets.iteritems(), key=operator.itemgetter(1))
			for i in xrange(num_terms):
				target = sorted_targets[i]
				target_word = target[0]
				prob = target[1]
				alignments = "0-0"
				rest = "1 1 1"
				phrase_model[key][target] = ( (prob , prob) , alignments, rest)

def write_phrase_model(filename,phrase_model):
	f = open('filename' , 'w')
	for source in phrase_model:
		for target in phrase_model:
			((prob1, prob2) , alignments, rest) = phrase_model[source][target]
			outstring = ""
			outstring = outstring + source + "|||" + target + "|||"
			outstring = outstring + prob1 + " " + prob2 + "|||"
			outstring = outstring + alignments + "|||" + rest + "\n"



