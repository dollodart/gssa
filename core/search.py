from time import time
from serp.env import query_dictionary
from serp.query import query, extract_orgres
from .publication import Publication

def search(search_term, nres=None, overwrite=False):
    query_dictionary['q'] = search_term
    queries = query(query_dictionary, nres, overwrite)
    return [Publication.from_json(d) for d in extract_orgres(queries)]
