import Database.db as db
import config
from peewee import fn

def remove_empty_abstracts():
  return (db.Article.delete()
                    .where((db.Article.abstract.is_null()) | (db.Article.abstract == ''))
                    .execute())

def remove_by_doctype():
  return (db.Article.delete()
                    .where(db.Article.document_type << config.EXCLUDED_DOCTYPES)
                    .execute())

def remove_by_journal():
  journal_ids = db.Journal.select(db.Journal.id).where(db.Journal.issn << config.EXCLUDED_JOURNALS)

  return db.Article.delete().where(db.Article.journal_id << journal_ids).execute()

def remove_doubles_by_title(search_type = 'initial'):
  # Select one copy of all doubles by id
  select_double_q = (db.Article.select(db.Article.id)
                               .where(db.Article.title_stripped.is_null(False), db.Article.search_type == search_type)
                               .group_by(db.Article.title_stripped)
                               .having(fn.COUNT(db.Article.id) > 1))

  # Select all other documents that only occur once
  select_q = (db.Article.select(db.Article.id)
                        .where(db.Article.title_stripped.is_null(False), db.Article.search_type == search_type)
                        .group_by(db.Article.title_stripped)
                        .having(fn.COUNT(db.Article.id) is 1))

  # Delete all other documents as they are copies
  removed = (db.Article.delete()
                       .where(db.Article.id.not_in(select_q), db.Article.id.not_in(select_double_q), db.Article.search_type == search_type))

  num_removed = removed.execute()

  # Search for matches between the initial search and match search
  # But only delete the doubles from match search
  if search_type == 'match':
    # Find titles that are double
    select_between = (db.Article.select(db.Article.title_stripped)
                                .where(db.Article.title_stripped.is_null(False))
                                .group_by(db.Article.title_stripped)
                                .having(fn.COUNT(db.Article.id) > 1))

    # Select the article ids from the doubles, but only from the match results
    select_match = (db.Article.select(db.Article.id)
                              .where(db.Article.title_stripped << select_between, db.Article.search_type == 'match'))

    # Delete the selected article ids
    removed_between = (db.Article.delete()
                                 .where(db.Article.id << select_match))

    num_removed = num_removed + removed_between.execute()

  return num_removed  

def remove_doubles_by_doi(search_type = 'initial'):
  select_q = (db.Article.select(db.Article.id)
                        .where(db.Article.doi.is_null(False), db.Article.search_type == search_type)
                        .group_by(db.Article.doi)
                        .having(fn.COUNT(db.Article.id) > 1))

  num_removed = db.Article.delete().where(db.Article.id << select_q, db.Article.search_type == search_type).execute()

  # Search for matches between the initial search and match search
  # But only delete the doubles from match search
  if search_type == 'match':
    # Find DOIs that are double
    select_between = (db.Article.select(db.Article.doi)
                                .where(db.Article.doi.is_null(False))
                                .group_by(db.Article.doi)
                                .having(fn.COUNT(db.Article.id) > 1))

    # Select the article ids from the doubles, but only from the match results
    select_match = (db.Article.select(db.Article.id)
                              .where(db.Article.doi << select_between, db.Article.search_type == 'match'))

    # Delete the selected article ids
    removed_between = (db.Article.delete()
                                 .where(db.Article.id << select_match))

    num_removed = num_removed + removed_between.execute()

  return num_removed

def delete_by_publication_date(date):
  remove_upper = db.Article.delete().where(db.Article.publication_date > date, db.Article.search_type == 'match').execute()
  remove_lower = db.Article.delete().where(db.Article.publication_date < '2011-01-01', db.Article.search_type == 'match').execute()

  return remove_upper + remove_lower

def report(removal_type, num_removed):
  print('Removed %i articles by %s' % (num_removed, removal_type))

def remove_all(search_type = 'initial'):
  abstracts_removed = remove_empty_abstracts()
  report('abstract', abstracts_removed)

  doctypes_removed = remove_by_doctype()
  report('doctypes', doctypes_removed)

  journals_removed = remove_by_journal()
  report('journal', journals_removed)

  titles_removed = remove_doubles_by_title(search_type)
  report('title', titles_removed)

  dois_removed = remove_doubles_by_doi(search_type)
  report('doi', dois_removed)

  date_removed = 0

  if search_type == 'match':
    date_removed = delete_by_publication_date('2018-05-13')
    report('date', date_removed)

  return {
    'doctypes': doctypes_removed,
    'empty_abstracts': abstracts_removed,
    'by_journal': {
      'articles': journals_removed,
      'journals': len(config.EXCLUDED_JOURNALS)
    },
    'title': titles_removed,
    'doi': dois_removed,
    'date': date_removed
  }