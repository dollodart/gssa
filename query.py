import requests
from .env import CACHE_DIR, URL
from .env import query_dictionary, pagination_dictionary
from .env import logging
from .env import global_checker, global_cache
from time import time
import json as jsonlib

def reqget(URL, params): # can be overridden
    return requests.get(URL, params=params)

def json_request(parameters):
    t0 = time()
    data = reqget(URL, params=parameters)
    return time() - t0, data.json()

def cache(data, filename):
    global_cache.append(filename)
    with open(f'{CACHE_DIR}/{filename}', 'w') as _:
        _.write(jsonlib.dumps(data))
    return None

def load_cache(filename):
    if filename in global_cache:
        with open(f'{CACHE_DIR}/{filename}', 'r') as _:
            return jsonlib.load(_)
    return None

def flatten_pagination(data, nres=None):
    """Given data with a link to more pages, get all the data and then
    return a flattened data structure."""

    t0 = time()
    org_res = []
    meta = []
    if nres is None:
        nres = 1e10
    nres += len(data['organic_results']) # initial organic results discounted
    while True:
        org_res.extend(data.pop('organic_results'))
        meta.append(data)
        if len(org_res) > nres:
            break
        try:
            link = data['serpapi_pagination']['next']
            dt, data = reqget(link, params=pagination_dictionary)
            logging.info(global_indent + 'pulled another page')
            global_checker.increment()
        except KeyError:
            break
    return time() - t0, org_res, meta
