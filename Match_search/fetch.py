from PmedConnect import PubmedAPI as api
import Database.db_connector as db, config
import progressbar
# import pickle

def execute_db_fetch(db):
  searcher.set_search_database(db)
  pubmed_ids = connector.get_unfetched_search_results(db, 'match')

  return fetch_loop(pubmed_ids)

def fetch_loop(ids):
  total_inserted = 0

  bar = progressbar.ProgressBar()

  step = 10000
  # i = 0

  for idx in bar(range(0, len(ids), step)):
    id_subset = ids[idx:idx + step]

    # i = i + 1
    
    try:  
      articles = searcher.fetch(id_subset)
    except:
      print('Failed, moving on.')

      continue

    # with open('dataset_%i.pickle' % i, 'wb') as handle:
    #   pickle.dump(articles, handle, protocol = pickle.HIGHEST_PROTOCOL)

    connector.set_search_results_fetched(id_subset)
  
    pubmed_ids_inserted = connector.insert_fetched_articles(id_subset, articles, 'match')

    total_inserted = total_inserted + len(pubmed_ids_inserted)

  return total_inserted

# def insert_loop():
#   for i in range(1, 65):
#     try:
#       with open('dataset_%i.pickle' % i, 'rb') as handle:
#         data = pickle.load(handle)

#         pubmed_ids_inserted = connector.insert_fetched_articles([], data, 'match')
#     except FileNotFoundError:
#       continue

def execute_fetch():
  # insert_loop()
  pubmed_inserted = execute_db_fetch('pubmed')
  pmc_inserted = execute_db_fetch('pmc')

  print(pubmed_inserted)
  print(pmc_inserted)

  # return pubmed_inserted + pmc_inserted

searcher = api.PubmedAPI(config.PUBMED_EMAIL)
connector = db.Connector()