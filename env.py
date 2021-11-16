import yaml
import logging
import logging.config as lconfig
import pathlib
from serp.util import Indent, Checker

TOP_LEVEL_DIR = pathlib.Path(__file__).parent
CACHE_DIR = TOP_LEVEL_DIR.joinpath('output')
INPUT_DIR = TOP_LEVEL_DIR.joinpath('input')

SERP_API_KEY = 'myapikey'
URL = 'https://serpapi.com/search'
max_page_size = 20
output = 'json'
cited_by_dictionary = dict(engine='google_scholar',
                           serp_api_key=SERP_API_KEY,
                           cites=None,
                           num=max_page_size,
                           output=output)
cite_dictionary = dict(engine='google_scholar_cite',
                       serp_api_key=SERP_API_KEY,
                       q=None,
                       output=output)
query_dictionary = dict(engine='google_scholar',
                       serp_api_key=SERP_API_KEY,
                       q=None,
                       num=max_page_size,
                       output=output)
pagination_dictionary = dict(serp_api_key=SERP_API_KEY)


with open(TOP_LEVEL_DIR.joinpath('logger.yaml'), 'r') as _:
    dct = yaml.load(_, Loader=yaml.Loader)
    lconfig.dictConfig(dct)

core_logger = logging.getLogger('core_logger')

# declaration of global instances (all references should come later)
global_indent = Indent()
global_checker = Checker(core_logger)
global_cache = [f.name for f in pathlib.Path(f'{CACHE_DIR}').iterdir()]
