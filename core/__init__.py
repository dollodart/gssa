from .publication import Publication
from .citation import Citation
from .search import search
from serp.env import global_cache, PUBLICATION_DIR, CITE_DIR, CITED_BY_DIR
from serp.env import cited_by_dictionary 
from serp.cache import load_cache, load_cache_paginated
from serp.query import extract_orgres
from serp.ids import title2file, hash_dict
import json as jsonlib

# filters
def has_cached_cite(pub):
    filepath = CITE_DIR.joinpath(title2file(pub.title))
    if filepath.exists():
        return True
    return False

def has_cached_cited_by(pub):
    # note need to add suffix -1 since queries are necessarily paginated
    cited_by_dictionary['cites'] = pub.cites_id
    filepath = CITED_BY_DIR.joinpath(hash_dict(cited_by_dictionary) + '-1')
    if filepath.exists():
        return True
    return False

def load_cached_publications(filters=tuple()):
    """
    Filters are dictionary of attribute and function.
    """

    pubs = []
    for f in global_cache:
        if f.parent == PUBLICATION_DIR:
            try:
                with open(f, 'r') as _:
                    pub = Publication.from_json(jsonlib.load(_))
            except Exception as e:
                print('should delete', f, 'corrupted data')
                continue
        else:
            continue
        pss = True
        for func in filters:
            if not func(pub):
                pss = False
        if pss:
            pubs.append(pub)
    return pubs

def load_cached_publications_hq(filters=tuple()):
    publist = load_cached_publications(filters)
    npublist = []
    for pub in publist:
        try:
            cite = pub.get_cite()
            assert cite.authors is not None
            pub.get_cited_by()
            for p in cited_by:
                cite = p.get_cite() # some may be none
            npublist.append(pub)
        except Exception as e:
            continue
    return npublist
