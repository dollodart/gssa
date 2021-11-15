import requests
from serp.env import CACHE_DIR, URL
from serp.env import query_dictionary, pagination_dictionary
from serp.env import core_logger
from serp.env import global_checker
from time import time
from serp.query import json_request, flatten_pagination
from .publication import Publication

def search(query_term):
    query_dictionary['q'] = query_term
    core_logger.info(f'finding first page in query for term:{query_term}')
    dt, data = json_request(query_dictionary)
    core_logger.info(f'found in {dt}s')
    global_checker.increment()
    core_logger.info(f'querying and flattening pagination')
    dt, data = flatten_pagination(data)
    core_logger.info(f'took {dt}s for {len(data)} results')
    global_checker.increment()
    return [Publication.from_json(d) for d in data]
