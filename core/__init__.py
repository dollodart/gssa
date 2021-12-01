from .publication import Publication
from .citation import Citation
from .search import search
from gssa.env import global_cache, PUBLICATION_DIR, CITE_DIR, CITED_BY_DIR
from gssa.env import cited_by_dictionary
from gssa.env import core_logger
from gssa.cache import load_cache, load_cache_paginated
from gssa.query import extract_orgres
from gssa.ids import title2file, hash_dict
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
                core_logger.error(f'delete {f}, corrupted data')
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


def load_cached_publications_all_data():
    """
    To be used for testing purposes (to avoid making queries when calling get_* commands).
    Note this changes a mutable property of a publication, which will cause the
    publication to appear to have less citations than it actually does.
    """
    filters = has_cached_cite, has_cached_cited_by
    publist = load_cached_publications(filters)
    for pub in publist:
        try:
            cited_by = pub.get_cited_by()
        except Exception as e:
            core_logger.error(
                f'delete cited_by for {pub.title}, corrupted data')
            cited_by = []
        ncited_by = [p for p in cited_by if has_cached_cite(p)]
        pub.set_cited_by(ncited_by)
    return publist
