from .publication import Publication
from .citation import Citation
from .search import search
from serp.env import global_cache, PUBLICATION_DIR

import json as jsonlib

def load_cached_publications(filters=tuple()):
    """
    Filters are dictionary of attribute and function.
    """

    pubs = []
    for f in global_cache:
        if f.parent == PUBLICATION_DIR:
            with open(f, 'r') as _:
                pub = Publication.from_json(jsonlib.load(_))
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
