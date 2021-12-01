from time import time
from gssa.env import search_dictionary
from gssa.query import query, extract_orgres
from .publication import Publication


def search(search_term, nres=None, overwrite=False):
    search_dictionary['q'] = search_term
    queries = query(search_dictionary, nres, overwrite)
    try:
        return [Publication.from_json(d) for d in extract_orgres(queries)]
    except Exception:  # current hack for queries which return only 1 result
        # find why this occurs, since it would cause data loss generally otherwise
        return [Publication.from_json(queries[0])]
