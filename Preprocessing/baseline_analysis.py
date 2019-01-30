import Preprocessing.tokenize as tokenize
import Preprocessing.read_write_corpus as corpus_handle
import Preprocessing.tokenize as tokenize
import config

import numpy
from sklearn.feature_extraction.text import CountVectorizer
import pickle
import os
from os.path import exists

filename_str = 'Metadata/%s_baseline_data.pickle'
vectorizer = CountVectorizer()

def get_word_metadata(matrix, unique):
  if unique is True:
    matrix = matrix > 0
    matrix = matrix.astype(int)

  row_sums = matrix.sum(axis = 1)

  indices = [i for i, x in enumerate(row_sums) if x == 0]

  for index in indices:
    numpy.delete(row_sums, index, 0)

  mean_words = numpy.mean(row_sums)
  min_words = int(min(row_sums))
  max_words = int(max(row_sums))
  
  return {'mean': mean_words, 'min': min_words, 'max': max_words}

def get_number_of_words(titles_matrix, abstracts_matrix, corpus_matrix, unique = False):
  title_meta = get_word_metadata(titles_matrix, unique)
  abstract_meta = get_word_metadata(abstracts_matrix, unique)
  corpus_meta = get_word_metadata(corpus_matrix, unique)

  return {'all': corpus_meta, 'title': title_meta, 'abstract': abstract_meta}

def get_number_of_docs(corpus):
  return len(corpus)

def store_baseline_data(baseline_data, search_type):
  file_name = filename_str % search_type

  with open(file_name, 'wb') as handle:
    pickle.dump(baseline_data, handle, protocol = pickle.HIGHEST_PROTOCOL)

def load_baseline_data(search_type):
  file_name = filename_str % search_type

  if exists(file_name):
    with open(file_name, 'rb') as handle:
      baseline_data = pickle.load(handle)
  else:
    baseline_data = {
      'num_docs': 0,
      'num_words': {
        'all': {'mean': 0, 'min': 0, 'max': 0},
        'title': {'mean': 0, 'min': 0, 'max': 0},
        'abstract': {'mean': 0, 'min': 0, 'max': 0},
      },
      'num_unique_words': {
        'all': {'mean': 0, 'min': 0, 'max': 0},
        'title': {'mean': 0, 'min': 0, 'max': 0},
        'abstract': {'mean': 0, 'min': 0, 'max': 0},
      }
    }

  return baseline_data

def get_vectorized(corpus):
  vectorizer = tokenize.create_vectorizer(corpus, CountVectorizer)

  feature_matrix = vectorizer.transform(corpus)

  return feature_matrix

def full_analysis():
  print('fetching')
  baseline_data = load_baseline_data('full')

  initial_corpus = corpus_handle.load_full('initial')
  initial_titles, initial_abstracts = corpus_handle.load_split('initial')

  match_corpus = corpus_handle.load_full('match')
  match_titles, match_abstracts = corpus_handle.load_split('match')

  print('merging')
  initial_titles = tokenize.merge_documents_as_string(initial_titles)
  initial_abstracts = tokenize.merge_documents_as_string(initial_abstracts)

  match_titles = tokenize.merge_documents_as_string(match_titles)
  match_abstracts = tokenize.merge_documents_as_string(match_abstracts)

  merged_corpus = initial_corpus + match_corpus
  merged_titles = initial_titles + match_titles
  merged_abstracts = initial_abstracts + match_abstracts

  print('get vectorized')
  corpus_matrix = get_vectorized(merged_corpus)
  titles_matrix = get_vectorized(merged_titles)
  abstracts_matrix = get_vectorized(merged_abstracts)

  print('get number of words')
  baseline_data['num_words'] = get_number_of_words(titles_matrix, abstracts_matrix, corpus_matrix)
  baseline_data['num_unique_words'] = get_number_of_words(titles_matrix, abstracts_matrix, corpus_matrix, unique = True)

  baseline_data['num_docs'] = get_number_of_docs(merged_corpus)

  print('storing')
  store_baseline_data(baseline_data, 'full')

def do_analysis(search_type = 'initial'):
  print('fetching')
  baseline_data = load_baseline_data(search_type)

  corpus = corpus_handle.load_full(search_type)
  titles, abstracts = corpus_handle.load_split(search_type)
  
  print('merging')
  titles = tokenize.merge_documents_as_string(titles)
  abstracts = tokenize.merge_documents_as_string(abstracts)

  print('get vectorized')
  corpus_matrix = get_vectorized(corpus)
  titles_matrix = get_vectorized(titles)
  abstracts_matrix = get_vectorized(abstracts)

  print('get number of words')
  baseline_data['num_words'] = get_number_of_words(titles_matrix, abstracts_matrix, corpus_matrix)
  baseline_data['num_unique_words'] = get_number_of_words(titles_matrix, abstracts_matrix, corpus_matrix, unique = True)

  baseline_data['num_docs'] = get_number_of_docs(corpus)

  print('storing')
  store_baseline_data(baseline_data, search_type)