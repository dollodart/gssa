import requests
from .env import CACHE_DIR, URL, NUM_RESULTS_PAGE
from .env import search_dictionary, pagination_dictionary
from .env import core_logger
from .env import global_checker, global_cache, global_indent
from .ids import hash_dict
from time import time
import json as jsonlib

def reqget(URL, params): # can be overridden
    t0 = time()
    data = requests.get(URL, params=params)
    return time() - t0, data

def json_request(parameters):
    dt, data = reqget(URL, params=parameters)
    return dt, data.json()

def cache(data, filename, datatype=None):
    if datatype is not None:
        filepath = f'{CACHE_DIR}/{datatype}/{filename}'
    else:
        filepath = f'{CACHE_DIR}/{filename}'
    global_cache.append(filepath)
    with open(filepath, 'w') as _:
        _.write(jsonlib.dumps(data))
    return None

def load_cache(filename, datatype=None):
    if datatype is not None:
        filepath = f'{CACHE_DIR}/{datatype}/{filename}'
    else:
        filepath = f'{CACHE_DIR}/{filename}'
    if filepath in global_cache:
        with open(filepath, 'r') as _:
            return jsonlib.load(_)
    return None

def load_cache_paginated(fileprefix, datatype=None):
    counter = 1
    data = load_cache(f'{fileprefix}-{counter}', datatype)
    queries = []
    #while data := load_cache(f'{fileprefix}-{counter}') is not None: # strange error of only bool results for data
    while data is not None:
        queries.append(data)
        counter += 1
        data = load_cache(f'{fileprefix}-{counter}', datatype)
    if queries == []:
        return None
    return queries

def pagination_query(queryresult, fileprefix, datatype=None, nres=None):
    """
    Assumes correct queryresult is input (run load_cache_paginated beforehand).
    Specify number of desired results, not number of pages (multiply number of
    pages by MAX_NUM_PAGES to get number results).
    """
    if nres is None:
        nres = 1e10
    n = dtt = dt = 0
    queries = []
    while n < nres:
        try:
            link = queryresult['serpapi_pagination']['next']
            dt, queryresult = reqget(link, params=pagination_dictionary)
            core_logger.info(global_indent + f'pulled another page in {dt}s')
            global_checker.increment()
            dtt += dt
            n += len(queryresult['organic_results'])

            page = queryresult['serpapi_pagination']['current']
            cache(queryresult, f'{fileprefix}-{page}', datatype)
            queries.append(queryresult)
        except KeyError:
            break
    return dtt, queries

def extract_orgres(queries):
    orgres = []
    for q in queries:
        orgres.extend(q['organic_results'])
    return orgres

def query(qdict, nres=None, overwrite=False):

    if 'q' in qdict.keys():
        search_key = 'q'
        datatype= 'search'
    else:
        search_key = 'cites'
        datatype = 'cited_by'

    search_term = qdict[search_key]

    if nres is not None and nres < NUM_RESULTS_PAGE:
        raise Exception(f'cannot query {nres} < {NUM_RESULTS_PAGE} for {search_term}')

    query_hash = hash_dict(qdict)
    queries = load_cache_paginated(query_hash)

    if queries is not None and not overwrite:
        orgres = extract_orgres(queries)
        n = len(orgres)
        
        if (nres is None) or (n > nres):
            core_logger.info(f'search results (type {search_key}) ' +
                             f'for search term {search_term} ' + 
                             f'up to {n} results cached, returning')
            return queries
        else:
            squery = orgres[-1]
            nres -= n # only get the additional results
    else:
        core_logger.info(f'finding first page in search (type {search_key}) for term:{search_term}')
        dt, squery = json_request(qdict)
        core_logger.info(f'found in {dt}s')
        global_checker.increment()
        cache(squery, f'{query_hash}-1', datatype) # important, otherwise load_cache_pagination will return None

    core_logger.info(f'getting pages and flattening pagination')
    dt, queries2 = pagination_query(squery, query_hash, datatype, nres)
    core_logger.info(f'took {dt}s for {len(queries2)} pages')
    global_checker.increment()

    queries2.insert(0, squery) # add original page
    if queries is not None:
        queries2 = queries[:-1] + queries2
        # queries[:-1] == squery when queries is not None
    
    return queries2
