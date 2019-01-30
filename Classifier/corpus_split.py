import Preprocessing.read_write_corpus as corpus_handle
import Preprocessing.tokenize as tokenize
import config

import csv
import sys
import pickle
import random
from sklearn.model_selection import train_test_split

def get_random_index(start, end, number):
  random_index = set()

  while len(random_index) < number:
    random_index.add(random.randint(start, end))
  
  return list(random_index)

def select_match(initial_corpus, match_corpus):
  num_to_match = len(initial_corpus)
  max_index = len(match_corpus) - 1

  if config.CLEAN_TEST_DATA:
    num_to_match = 5

  random_idx = get_random_index(0, max_index, num_to_match)

  sliced_corpus = [match_corpus[i] for i in random_idx]

  if len(sliced_corpus) != num_to_match:
    print('error in dataset length subset: %i, length initial %i' % (len(sliced_corpus), num_to_match))

  return sliced_corpus, random_idx

def filter_and_create_matrix(number, initial_corpus, match_corpus):
  num_initial = len(initial_corpus)
  num_match = len(match_corpus)

  merged_corpus = initial_corpus + match_corpus

  print('creating vectorizer')
  vectorizer = tokenize.create_vectorizer(merged_corpus)

  print('creating feature matrix')
  feature_matrix = vectorizer.transform(merged_corpus)

  matrix_obj = {
    'matrix': feature_matrix,
    'initial_size': num_initial,
    'match_size': num_match,
    'vocabulary': list(vectorizer.vocabulary_.keys())
  }

  return matrix_obj, vectorizer

def create_labels(initial_corpus, match_corpus):
  y = [1] * len(initial_corpus)
  y = y + [0] * len(match_corpus)

  return y

def store_R_data(dataset, number):
  with open(config.R_LOCATION + 'originals/datasets/corpus_%i.csv' % number, 'w') as handle:
    writer = csv.writer(handle)
    
    for i in dataset:
      try:
        writer.writerow([i,])
      except UnicodeEncodeError as e:
        print('err')
        continue

def store_dataset(dataset, number):
  with open('Datasets/%i_dataset.pickle' % number, 'wb') as handle:
    pickle.dump(dataset, handle, protocol = pickle.HIGHEST_PROTOCOL)

def split_train_test(X, y):
  seed = random.randint(0, 2**32 - 1)

  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = config.TEST_SET_SIZE, random_state = seed, stratify = y)

  return {'X_train': X_train, 'X_test': X_test, 'y_train': y_train, 'y_test': y_test, 'seed': seed}

def prepare():
  print('fetching')
  initial_corpus = corpus_handle.load_full('initial')
  match_corpus = corpus_handle.load_full('match')

  if config.CLEAN_TEST_DATA is True:
    config.NUM_DATASETS = 5
    config.TEST_SET_SIZE = 0.25

  for i in range(config.NUM_DATASETS):
    match_subset, selected_indexes = select_match(initial_corpus, match_corpus)
    
    matrix_obj, vectorizer = filter_and_create_matrix(i, initial_corpus, match_subset)

    X = matrix_obj['matrix']
    y = create_labels(initial_corpus, match_subset)
    
    dataset = split_train_test(X, y)

    data = {**matrix_obj, **dataset, 'vectorizer': vectorizer, 'match_index': selected_indexes}

    store_R_data(initial_corpus + match_subset, i)
    store_dataset(data, i)