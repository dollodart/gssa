from time import time
from serp.env import search_dictionary
from serp.query import query, extract_orgres
from .publication import Publication

def search(search_term, nres=None, overwrite=False):
    search_dictionary['q'] = search_term
    queries = query(search_dictionary, nres, overwrite)
    return [Publication.from_json(d) for d in extract_orgres(queries)]
