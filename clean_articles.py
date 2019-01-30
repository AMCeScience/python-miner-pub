import Preprocessing.remove_characters as clean
import Preprocessing.tokenize as tokenize
import Preprocessing.stemming as stemmer
import Preprocessing.remove_stopwords as stopwords
import Preprocessing.token_length as token_length
import Preprocessing.read_write_corpus as corpus_handle
import config

import Text_data.test_file as test_data

import Database.db_connector as db
import pickle

import nltk

def get_corpus(search_type):
  if config.CLEAN_TEST_DATA is True:
    return test_data.titles, test_data.abstracts

  conn = db.Connector()

  articles = conn.get_articles(search_type)

  titles = []
  abstracts = []

  for article in articles:
    titles.append(article.title)
    abstracts.append(article.abstract)

  return titles, abstracts

def clean_corpus(titles, abstracts):
  cleaned_titles, cleaned_abstracts = clean.remove_all(titles, abstracts)
  print('cleaned')

  tokenized_titles = list(map(tokenize.tokenize_item, cleaned_titles))
  tokenized_abstracts = list(map(tokenize.tokenize_item, cleaned_abstracts))
  print('tokenized')

  cleaned_titles, cleaned_abstracts = stopwords.remove_all(tokenized_titles, tokenized_abstracts)
  print('stopwords removed')

  if config.STEM_TEXT is True:
    cleaned_titles, cleaned_abstracts = stemmer.stem_all(cleaned_titles, cleaned_abstracts)
    print('stemmed')

  cleaned_titles, cleaned_abstracts = token_length.remove_all(cleaned_titles, cleaned_abstracts)
  print('length removed')

  return cleaned_titles, cleaned_abstracts

def run_corpus(search_type = 'initial'):
  print('fetching')
  raw_titles, raw_abstracts = get_corpus(search_type)
  
  print('cleaning')
  titles, abstracts = clean_corpus(raw_titles, raw_abstracts)

  print('storing')
  corpus_handle.store_split(titles, abstracts, search_type)

def merge_corpus(search_type):
  # Get a list of titles and a list of abstracts
  print('fetching')
  titles, abstracts = corpus_handle.load_split(search_type)

  # Merge the title and abstract lists into one
  print('merging title+abstract')
  corpus = tokenize.merge_title_abstract(titles, abstracts)
  # Merge the documents into strings, yields a list of strings
  print('merging documents')
  corpus = tokenize.merge_documents_as_string(corpus)

  # Store the merged corpus
  print('storing')
  corpus_handle.store_full(corpus, search_type)

def run_corpora():
  # Run cleanup procedures that are not influenced by corpus frequencies
  run_corpus('initial')
  run_corpus('match')

  # Build a corpus of merged titles + abstracts, needed for filtering
  merge_corpus('initial')
  merge_corpus('match')

if __name__ == '__main__':
  run_corpora()