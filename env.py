from .secretenv import SERP_API_KEY
import yaml
import logging
import logging.config as lconfig
import pathlib
from gssa.util import Indent, Checker

from gssa.userenv import (TOP_LEVEL_DIR, CACHE_DIR, INPUT_DIR,
                          CITED_BY_SDIR, CITE_SDIR, PUBLICATION_SDIR,
                          SEARCH_SDIR)

CITED_BY_DIR = CACHE_DIR.joinpath(CITED_BY_SDIR)
CITE_DIR = CACHE_DIR.joinpath(CITE_SDIR)
PUBLICATION_DIR = CACHE_DIR.joinpath(PUBLICATION_SDIR)
SEARCH_DIR = CACHE_DIR.joinpath(SEARCH_SDIR)

MAX_FILENAME_LEN = 40


URL = 'https://serpapi.com/search'
NUM_RESULTS_PAGE = 20  # don't change this and keep at maximum value
OUTPUT_FORMAT = 'json'
ORDERED_KEYS = 'q', 'cites', 'engine', 'output', 'num', 'serp_api_key'

cited_by_dictionary = dict(engine='google_scholar',
                           serp_api_key=SERP_API_KEY,
                           cites=None,
                           num=NUM_RESULTS_PAGE,
                           output=OUTPUT_FORMAT)
cite_dictionary = dict(engine='google_scholar_cite',
                       serp_api_key=SERP_API_KEY,
                       q=None,
                       output=OUTPUT_FORMAT)
search_dictionary = dict(engine='google_scholar',
                         serp_api_key=SERP_API_KEY,
                         q=None,
                         num=NUM_RESULTS_PAGE,
                         output=OUTPUT_FORMAT)
pagination_dictionary = dict(serp_api_key=SERP_API_KEY)


with open(TOP_LEVEL_DIR.joinpath('logger.yaml'), 'r') as _:
    dct = yaml.load(_, Loader=yaml.Loader)
    lconfig.dictConfig(dct)

core_logger = logging.getLogger('core_logger')
test_logger = logging.getLogger('test_logger')

# declaration of global instances (all references should come later)
global_indent = Indent()
global_checker = Checker(core_logger)
global_cache = []
for dr in CITED_BY_DIR, CITE_DIR, PUBLICATION_DIR, SEARCH_DIR:
    global_cache.extend([f for f in dr.iterdir()])
