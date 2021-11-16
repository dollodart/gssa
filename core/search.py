from time import time
from serp.env import NUM_RESULTS_PAGE
from serp.env import query_dictionary, core_logger, global_checker
from serp.query import json_request, flatten_pagination, cache, load_cache
from serp.ids import hash_dict
from .publication import Publication

def search(query_term, nres=None, overwrite=False):
    query_dictionary['q'] = query_term
    query_hash = hash_dict(query_dictionary)
    res = load_cache(query_hash)

    prepend = None

    if res is not None and not overwrite:
        n = len(res)
        if nres is None or n > nres:
            core_logger.info(f'search results for query {query_term} cached, returning')
            return res
        else: # change the page from first 
            meta = load_cache(query_hash + '-meta')
            index = n // (NUM_RESULTS_PAGE + 1)
            data = meta[index]
            data['organic_results'] = res # may result in some duplicates
            # organic results are flattened into a list, but the meta results
            # are single dicts and not done so
            prepend = meta[:index]
            nres -= n # only get the additional results
    else:
        core_logger.info(f'finding first page in search for term:{query_term}')
        dt, data = json_request(query_dictionary)
        core_logger.info(f'found in {dt}s')
        global_checker.increment()

    core_logger.info(f'getting pages and flattening pagination')
    dt, data, meta = flatten_pagination(data, nres)
    core_logger.info(f'took {dt}s for {len(data)} results')
    global_checker.increment()

    cache(data, query_hash)
    if prepend is not None:
        meta = prepend + meta
    cache(meta, query_hash + '-meta')

    return [Publication.from_json(d) for d in data]
