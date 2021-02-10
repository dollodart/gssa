import yaml
import logging
import logging.config as lconfig

SERP_API_KEY = 'myapikey'
CACHE_DIR = 'output'
INPUT_DIR = 'input'
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

with open('logger.yaml', 'r') as _:
    dct = yaml.load(_, Loader=yaml.Loader)
    lconfig.dictConfig(dct)
