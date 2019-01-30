import Initial_search.search as bd_search
import Initial_search.fetch as bd_fetch
import Preprocessing.delete_unwanted as clean
import pickle

if __name__ == '__main__':
  # Search pubmed
  num_found = bd_search.execute_search()
  # Fetch from pubmed
  num_inserted = bd_fetch.execute_fetch()

  metadata = {'searched': num_found, 'fetched': num_inserted}

  with open('Metadata/bd_initial_results.pickle', 'wb') as handle:
    pickle.dump(metadata, handle, protocol = pickle.HIGHEST_PROTOCOL)

  # Clean the corpus
  removal_metadata = clean.remove_all()

  with open('Metadata/bd_cleaning.pickle', 'wb') as handle:
    pickle.dump(removal_metadata, handle, protocol = pickle.HIGHEST_PROTOCOL)