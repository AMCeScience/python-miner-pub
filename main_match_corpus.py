import Match_search.search as match_search
import Match_search.fetch as match_fetch
import Preprocessing.delete_unwanted as clean
import pickle

if __name__ == '__main__':
  # Search pubmed
  num_found = match_search.execute_search()
  # Fetch from pubmed
  num_inserted = match_fetch.execute_fetch()

  metadata = {'searched': num_found, 'fetched': num_inserted}

  with open('Metadata/match_results.pickle', 'wb') as handle:
    pickle.dump(metadata, handle, protocol = pickle.HIGHEST_PROTOCOL)

  # Clean corpus
  removal_metadata = clean.remove_all('match')

  with open('Metadata/match_cleaning.pickle', 'wb') as handle:
    pickle.dump(removal_metadata, handle, protocol = pickle.HIGHEST_PROTOCOL)