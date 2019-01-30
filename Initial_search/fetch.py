from PmedConnect import PubmedAPI as api
import Database.db_connector as db, config

def execute_db_fetch(db):
  searcher.set_search_database(db)
  pubmed_ids = connector.get_unfetched_search_results(db)

  return fetch_loop(pubmed_ids)

def fetch_loop(ids):
  total_inserted = 0

  for idx in range(0, len(ids), 1000):
    articles = searcher.fetch(ids[idx:idx + 1000])
  
    pubmed_ids_inserted = connector.insert_fetched_articles(ids, articles)

    total_inserted = total_inserted + len(pubmed_ids_inserted)

  return total_inserted

def execute_fetch():
  pubmed_inserted = execute_db_fetch('pubmed')
  pmc_inserted = execute_db_fetch('pmc')

  return pubmed_inserted + pmc_inserted

searcher = api.PubmedAPI(config.PUBMED_EMAIL)
connector = db.Connector()