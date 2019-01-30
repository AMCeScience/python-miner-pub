import os

CWD = os.getcwd()

DB_FILE = CWD + '/Database/miner_database.db'
DB_INSERT_LIMIT = 100

### Unwanted document types
EXCLUDED_DOCTYPES = ['Addresses', 'Bibliography', 'Biography', 'Book', 'Clinical Conference', 'Comment', 'Congresses', 'Consensus Development Conference', 'Consensus Development Conference, NIH', 'Dataset', 'Directory', 'Editorial', 'Guideline', 'Interview', 'Lectures', 'Letter', 'News', 'Published Erratum']

EXCLUDED_JOURNALS = ['2167-647X', '1537-744X', '1758-0463', '2167-6461', '1932-6203', '1424-8220', '0036-8075', '2045-2322', '1873-1457', '1879-2782', '2356-6140', '1749-6632', '2168-2275', '2162-2388', '1364-503X', '0272-1716', '0162-1459', '1549-960X', '0036-8733', '1361-6528', '1941-0042', '1079-7114', '1941-0506', '1878-4372', '1361-6609', '2045-7758', '0017-8012', '1879-1026', '1939-1854', '2193-1801', '2167-8359', '2196-1115']

### Pubmed API config
PUBMED_EMAIL = 'a.j.vanaltena@amc.uva.nl'

CLEAN_TEST_DATA = False
TEXT_DATA_LOCATION = 'Text_data'

STEM_TEXT = False
KEEP_NUMBERS = False
KEEP_DASHES = False

EXTRA_STOPWORDS = ['big_data', 'big']

SPARSE_TERM_REMOVE = 0.9999

MAX_DOCFREQ = 0.9

NUM_DATASETS = 20
TEST_SET_SIZE = 0.1

ALPHA_ESTIMATION_CF = 2
THRESHOLD_ESTIMATION_CF = 2

R_LOCATION = '../R/'