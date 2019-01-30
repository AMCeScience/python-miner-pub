import Preprocessing.tokenize as tokenize
import Preprocessing.read_write_corpus as corpus_handle
import Preprocessing.tokenize as tokenize
import config

from itertools import groupby
import numpy
from sklearn.feature_extraction.text import CountVectorizer
import pickle
import os
from os.path import exists

vectorizer = CountVectorizer()

def get_word_metadata(matrix, unique):
  if unique is True:
    matrix = matrix > 0
    matrix = matrix.astype(int)

  row_sums = matrix.sum(axis = 1)

  max_words = int(max(row_sums))
  
  row_sums = row_sums.tolist()

  counts = [0] * (max_words + 1)

  for i, g in groupby(sorted(row_sums), key = lambda x: x[0]):
    f = [v for v in g]

    counts[i] = len(f)
  
  return counts

def get_number_of_docs(corpus):
  return len(corpus)

def remove_vocab(corpus, vocabulary):
  vectorizer = tokenize.create_vectorizer(corpus, CountVectorizer)

  feature_matrix = vectorizer.transform(corpus)

  return feature_matrix

def get_full_vocab():
  initial_corpus = corpus_handle.load_full('initial')
  match_corpus =  corpus_handle.load_full('match')

  merged_corpus = initial_corpus + match_corpus

  vectorizer = tokenize.create_vectorizer(merged_corpus, CountVectorizer)

  return vectorizer.get_feature_names()

def do_analysis():
  initial_corpus = corpus_handle.load_full('initial')
  match_corpus = corpus_handle.load_full('match')

  vocabulary = []
  
  print('remove vocabulary')
  initial_corpus_matrix = remove_vocab(initial_corpus, vocabulary)
  match_corpus_matrix = remove_vocab(match_corpus, vocabulary)

  print('get number of words')
  initial_counts = get_word_metadata(initial_corpus_matrix, False)
  match_counts = get_word_metadata(match_corpus_matrix, False)
  
  counts = {'initial': initial_counts, 'match': match_counts}

  print('storing')
  with open('Metadata/word_counts.pickle', 'wb') as handle:
    pickle.dump(counts, handle, protocol = pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
  do_analysis()