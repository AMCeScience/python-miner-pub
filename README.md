# Python Miner: Big Data Publications

This repository contains the scripts that implement part of the methods described in the publications: "".
The scripts handle data fetching, preparation, and visualisation.
Classification is implemented in R, found in the [R-contrast-pub](https://github.com/AMCeScience/R-contrast-pub) repository.
The scripts handle the following research steps:

#### [Get initial corpus](main_initial_corpus.py)

Searching PubMed and PubMed Central for articles with a specific query ([esearch]).
Article data is fetched ([efetch]) and stored into a [SQLite database](Database/db.py).
After the fetch, unwanted articles are [removed](#remove-articles) and the remaining are [cleaned](#cleaning-articles).

#### [Get matching corpus](main_match_corpus.py)

Searching for matching PubMed and PubMed Central articles based on journal and publication date range ([esearch]) and fetching results ([efetch]).
Article data is fetched ([efetch]) and stored into a [SQLite database](Database/db.py).
After the fetch, unwanted articles are [removed](#remove-articles) and the remaining are [cleaned](#cleaning-articles).

#### [Remove articles](Preprocessing/delete_unwanted.py)

Unwanted articles are removed from the database by the following criteria:

1. They have an empty abstract;
2. Their doctype is defined in the `EXCLUDED_DOCTYPES` variable in the [config];
3. Their journal ISSN is defined in the `EXCLUDED_JOURNALS` variable in the [config];
4. They are a double, based on their title (with all symbols removed, regex: `[^a-z]`);
5. They are a double, based on their DOI.

#### [Cleaning articles](clean_articles.py)

Articles in the database are cleaned by performing the following steps:

1. Special characters are removed from article titles and abstracts ([script](Preprocessing/remove_characters.py))
2. Tokenizing the titles and abstracts
3. Removing stopwords from the tokenized titles and abstracts ([script](Preprocessing/remove_stopwords.py))
4. (Optional) Stemming the tokenized titles and abstracts
5. Removing very small and very big tokens (unlikely real words, [script](Preprocessing/token_length.py))

#### [Preparing datasets](prepare_datasets.py)

The initial and matching corpora are retrieved.
A predetermined number of datasets is created by taking the complete initial corpus and matching a random set from the matching corpus.
The dataset is then [vectorized](Preprocessing/tokenize.py) and turned into a feature matrix.
Lastly, the matrix and original dataset are stored as an pickle object.

#### Other

The following scripts were used for various tasks to perform the research, for example: analyse datasets, gather metadata, create figures.

1. [baseline_data.py](baseline_data.py) fetches some baseline metadata about the initial and matching corpora such as word counts and document counts.
2. [word_distribution.py](word_distribution.py) fetches word distribution metadata over the documents in the initial and matching corpora.
3. [doc_word_freqs.py](Plotting_scripts/doc_word_freqs.py) and [docs_per_year.py](Plotting_scripts/docs_per_year.py) create figures using Matplotlib for respectively the word to document frequency and the number of documents per (publication) year.

[esearch]: https://www.ncbi.nlm.nih.gov/books/NBK25499/#_chapter4_ESearch_
[efetch]: https://www.ncbi.nlm.nih.gov/books/NBK25499/#_chapter4_EFetch_
[config]: config.py
