from time import time
from serp.env import query_dictionary, core_logger, global_checker
from serp.query import json_request, flatten_pagination, cache, load_cache
from serp.ids import hash_dict
from .publication import Publication

def search(query_term, overwrite=False):
    query_dictionary['q'] = query_term
    query_hash = hash_dict(query_dictionary)
    res = load_cache(query_hash)

    if res is not None and not overwrite:
        core_logger.info(f'search results for query {query_term} cached, returning')
        return res

    core_logger.info(f'finding first page in search for term:{query_term}')
    dt, data = json_request(query_dictionary)
    core_logger.info(f'found in {dt}s')
    global_checker.increment()
    core_logger.info(f'getting pages and flattening pagination')
    dt, data, meta = flatten_pagination(data)
    core_logger.info(f'took {dt}s for {len(data)} results')
    global_checker.increment()
    cache(data, query_hash)
    cache(meta, query_hash + '-meta')
    return [Publication.from_json(d) for d in data]
