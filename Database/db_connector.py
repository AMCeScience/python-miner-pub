import Database.db as db, config
import progressbar, re
from peewee import *

class Connector:
  inserts = 0

  def insert_search_results(self, pubmed_ids, query, search_db, search_type = 'initial'):
    data_list = []

    for pubmed_id in pubmed_ids:
      data_list.append(dict(pubmed_id = pubmed_id, search_query = query, db = search_db, search_type = search_type))

    # Calculate maximum number of inserts,
    # the length of the list above plus two extra parameters are inserted for each data_list item
    insert_size = (db.SQLITE_MAX_VARIABLE_NUMBER // (len(data_list[0]) + 2))
    
    with db.conn.atomic():
      for idx in range(0, len(data_list), insert_size):
        db.Search_results.insert_many(data_list[idx:idx + insert_size]).execute()

  def set_search_results_fetched(self, pubmed_ids):
    insert_size = (db.SQLITE_MAX_VARIABLE_NUMBER // 1)

    for idx in range(0, len(pubmed_ids), insert_size):
      list_subset = pubmed_ids[idx:idx + insert_size]

      query = db.Search_results.update(fetched = True).where(db.Search_results.pubmed_id << list_subset).execute()

  def get_unfetched_search_results(self, search_db = 'pubmed', search_type = 'initial'):
    result = (db.Search_results.select(db.Search_results.pubmed_id)
                               .where(db.Search_results.fetched == False, db.Search_results.db == search_db, db.Search_results.search_type == search_type))

    return [i.pubmed_id for i in result]

  def insert_fetched_articles(self, pmids, articles, search_type = 'initial'):
    pubmed_ids = []
    article_list = []

    print('Inserting %i articles.' % len(articles))

    # Build formatted list of articles
    bar = progressbar.ProgressBar()

    article_list = []

    for idx in bar(range(0, len(articles))):
      article = articles[idx]

      pubmed_ids.append(article['pmid'])
      
      journal_id = self.get_create_journal(article)
      publication_date = self.get_publication_date(article)
      self.insert_keywords(article['pmid'], article['keywords'])

      if article['doc_type'] == 'Other':
        print('Document problem with %s.' % article['pmid'])

      if article['title'] is None:
        print('Title problem with %s.' % article['pmid'])

        continue
        
      try:
        article_list.append({
          'pubmed_id': article['pmid'],
          'document_type': article['doc_type'],
          'title': article['title'],
          'title_stripped': re.sub('[^a-z]', '', article['title'].lower()),
          'abstract': article['abstract'],
          'journal': journal_id,
          'publication_date': publication_date,
          'doi': article['doi'],
          'search_type': search_type
        })
      except TypeError:
        print('Document problem with %s.' % article['pmid'])

        raise

    # Mass insert list of articles
    with db.conn.atomic():
      # remove one to avoid issue if peewee adds some variable
      insert_size = (db.SQLITE_MAX_VARIABLE_NUMBER // (len(article_list[0]) + 1))

      for idx in range(0, len(article_list), insert_size):        
        db.Article.insert_many(article_list[idx:idx + insert_size]).execute()

    self.set_search_results_fetched(pmids)

    return pubmed_ids

  def insert_keywords(self, article_id, keywords):
    try:
      for keyword in keywords:
        keyword, created = db.Keyword.get_or_create(keyword = keyword)

        db.Keyword_to_article.create(article_id = article_id, keyword_id = keyword.id)
    except TypeError:
      print('No keywords for %s.' % article_id)

  def get_create_journal(self, article):
    try:
      journal = {
        'title': article['journal_title'],
        'iso': article['journal_iso'],
        'iso_stripped': re.sub('[^a-zA-Z]', '', article['journal_iso']),
        'issn': article['journal_issn'],
      }
    except TypeError:
      print('Journal problem with %s.' % article['pmid'])

      return None

    try:
      found_journal = db.Journal.get(
          (db.Journal.title == journal['title'])
          or (db.Journal.iso == journal['iso'])
          or (db.Journal.iso_stripped == journal['iso_stripped'])
          or (db.Journal.issn == journal['issn']))
    except db.Journal.DoesNotExist:
      found_journal = db.Journal.create(**journal)

    return found_journal.id

  def get_publication_date(self, article):
    if article['pub_year'] is not None and article['pub_month'] is not None and article['pub_day'] is not None:
      return '%s-%s-%s' % (article['pub_year'], article['pub_month'].zfill(2), article['pub_day'].zfill(2))

    if article['date_pubmed_published'] is not None:
      return article['date_pubmed_published']

    if article['date_medline_published'] is not None:
      return article['date_medline_published']

  def get_match_metadata(self):
    return (db.Article.select(
                        fn.strftime('%Y', fn.MIN(db.Article.publication_date)).alias('min_date'),
                        fn.strftime('%Y', fn.MAX(db.Article.publication_date)).alias('max_date'),
                        db.Journal.issn,
                        db.Journal.iso
                      )
                      .join(db.Journal)
                      .group_by(db.Article.journal_id)
                      ).execute()

  def get_articles(self, search_type = 'initial'):
    return db.Article.select(db.Article.title, db.Article.abstract).where(db.Article.search_type == search_type).execute()

  def get_articles_by_year(self, start, end, search_type = 'initial'):
    return db.Article.select(db.Article.title, db.Article.abstract).where(db.Article.search_type == search_type, db.Article.publication_date.between(start, end)).execute()