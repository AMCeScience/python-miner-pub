from PmedConnect import PubmedAPI as api
import Database.db_connector as db, config

def db_search(search_db, search_terms):
  searcher = api.PubmedAPI(config.PUBMED_EMAIL)
  connector = db.Connector()

  # Search PubMed
  searcher.set_search_database(search_db)
  searcher.set_search_date('2011/01/01')
  search = searcher.search(search_terms)
  
  print(search['summary'])
  
  connector.insert_search_results(search['pmids'], search['summary']['translated_query'], search_db)

  return search['summary']['retrieved']

def execute_search():
  pubmed_retrieved = db_search('pubmed', '"big data"[TIAB] AND english[Language]')
  pmc_retrieved = db_search('pmc', '("big data"[TI] OR "big data"[AB])')

  return {'pubmed': pubmed_retrieved, 'pmc': pmc_retrieved}