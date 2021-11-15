import requests
from env import CACHE_DIR, URL
from env import query_dictionary, pagination_dictionary
from env import logging
from env import global_checker
from time import time
from query import json_request, flatten_pagination
from core.publication import Publication

def search(query_term):
    query_dictionary['q'] = query_term
    logging.info(f'finding first page in query for term:{query_term}')
    dt, data = json_request(query_dictionary)
    logging.info(f'found in {dt}s')
    global_checker.increment()
    logging.info(f'querying and flattening pagination')
    dt, data = flatten_pagination(data)
    logging.info(f'took {dt}s for {len(data)} results')
    global_checker.increment()
    return [Publication.from_json(d) for d in data]
