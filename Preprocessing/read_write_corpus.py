import config
import pickle

def load_split(search_type):
  with open(config.TEXT_DATA_LOCATION + '/%s_cleaned_titles.pickle' % search_type, 'rb') as handle:
    titles = pickle.load(handle)

  with open(config.TEXT_DATA_LOCATION + '/%s_cleaned_abstracts.pickle' % search_type, 'rb') as handle:
    abstracts = pickle.load(handle)

  return titles, abstracts

def store_split(clean_titles, clean_abstracts, search_type):
  with open(config.TEXT_DATA_LOCATION + '/%s_cleaned_titles.pickle' % search_type, 'wb') as handle:
    pickle.dump(clean_titles, handle, protocol = pickle.HIGHEST_PROTOCOL)

  with open(config.TEXT_DATA_LOCATION + '/%s_cleaned_abstracts.pickle' % search_type, 'wb') as handle:
    pickle.dump(clean_abstracts, handle, protocol = pickle.HIGHEST_PROTOCOL)

def load_full(search_type):
  with open(config.TEXT_DATA_LOCATION + '/%s_corpus.pickle' % search_type, 'rb') as handle:
    corpus = pickle.load(handle)

  return corpus

def store_full(corpus, search_type):
  with open(config.TEXT_DATA_LOCATION + '/%s_corpus.pickle' % search_type, 'wb') as handle:
    pickle.dump(corpus, handle, protocol = pickle.HIGHEST_PROTOCOL)