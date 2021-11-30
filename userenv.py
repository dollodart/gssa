import pathlib

TOP_LEVEL_DIR = pathlib.Path(__file__).parent

DUMMY_CACHE_DIR = TOP_LEVEL_DIR.joinpath('dummy_cache')
SERP_CACHE_DIR = TOP_LEVEL_DIR.joinpath('serp_cache')
GPROFILE_INPUT_DIR = TOP_LEVEL_DIR.joinpath('input')

# default directories (can be overwritten by user)
CACHE_DIR = SERP_CACHE_DIR
INPUT_DIR = GPROFILE_INPUT_DIR

# string types
CITED_BY_SDIR = 'cited_by'
CITE_SDIR = 'cite'
PUBLICATION_SDIR = 'publication'
SEARCH_SDIR = 'search'
