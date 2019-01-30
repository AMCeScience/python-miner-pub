from PmedConnect import PubmedAPI as api
import Database.db_connector as db, config
import progressbar

def db_search(search_db, journal_meta):
  searcher = api.PubmedAPI(config.PUBMED_EMAIL)

  # Search PubMed
  searcher.set_search_database(search_db)
  searcher.set_search_date(journal_meta.min_date, journal_meta.max_date)
  search = searcher.search(get_query(journal_meta))
  
  print(search['summary'])
  
  if search['summary']['retrieved'] > 0:
    connector.insert_search_results(search['pmids'], search['summary']['translated_query'], search_db, 'match')

  return search['summary']['retrieved']

def get_query(journal_meta):
  journal_id = journal_meta.journal.issn

  if journal_id is None:
    journal_id = journal_meta.journal.iso

  query = '"%s"[Journal]' % journal_id

  return query

def execute_search():
  match_metadata = connector.get_match_metadata()

  pubmed_retrieved = 0
  pmc_retrieved = 0

  for journal_meta in match_metadata:
    pubmed_retrieved = pubmed_retrieved + db_search('pubmed', journal_meta)
    pmc_retrieved = pmc_retrieved + db_search('pmc', journal_meta)

  return {'pubmed': pubmed_retrieved, 'pmc': pmc_retrieved}

connector = db.Connector()