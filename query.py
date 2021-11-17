import requests
from .env import CACHE_DIR, URL
from .env import query_dictionary, pagination_dictionary
from .env import core_logger
from .env import global_checker, global_cache, global_indent
from time import time
import json as jsonlib

def reqget(URL, params): # can be overridden
    t0 = time()
    data = requests.get(URL, params=params)
    return time() - t0, data

def json_request(parameters):
    dt, data = reqget(URL, params=parameters)
    return dt, data.json()

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

    org_res = []
    meta = []
    dtt = 0
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
            core_logger.info(global_indent + 'pulled another page')
            global_checker.increment()
            dtt += dt
        except KeyError:
            break
    return dtt, org_res, meta
