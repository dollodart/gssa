import pathlib
import requests
from time import time, sleep
from serp.env import core_logger
from serp.env import cited_by_dictionary, cite_dictionary, search_dictionary, pagination_dictionary
from serp.env import CACHE_DIR
from serp.env import global_indent, global_checker, global_cache
from serp.query import query, load_cache_paginated, extract_orgres, cache, load_cache, json_request
from serp.ids import title2file
from .citation import Citation
import json as jsonlib

class Publication:
    publist = dict()
    def __init__(self,
                 title,
                 position,
                 result_id,
                 cites_id,
                 abstract,
                 publication_summary,
                 authors_summary,
                 cited_by_count,
                 link
                 ):
        self.title = title
        self.result_id = result_id
        self.cites_id = cites_id
        self.abstract = abstract
        self.publication_summary = publication_summary
        self.authors_summary = authors_summary
        self.cited_by_count = cited_by_count

        # these attributes must exist to check, but can be None type
        self._cite = None
        self._cited_by = None

        try:
            self.__class__.publist[self.title]
            core_logger.warn('initialized publication when there already exists'
            ' a publication with the same title in application memory')
        except KeyError:
            self.__class__.publist[self.title] = self

    @classmethod
    def from_json(cls, json):
        """
        Initialize a publication from a search result.
        """

        try:
            r = cls.publist[json['title']]
            core_logger.info(global_indent + f'Publication object with title {json["title"]}\n' + 
                         global_indent + 'already in memory, returning') 
            return r
        except KeyError:
            pass

        d = dict()
        for k in 'title', 'position', 'result_id', 'link':
            try:
                d[k] = json[k]
            except KeyError:
                d[k] = None

        try:
            d['abstract'] = json['snippet']
        except KeyError:
            d['abstract'] = ''
        try:
            d['publication_summary'] = json['publication_info']['summary']
        except KeyError:
            d['publication_summary'] = ''
        try:
            d['authors_summary'] = [x['name']
                                    for x in json['publication_info']['authors']]
        except KeyError:
            d['authors_summary'] = []
        try:
            d['cited_by_count'] = json['inline_links']['cited_by']['total']
        except KeyError:
            d['cited_by_count'] = 0
        try:
            d['cites_id'] = json['inline_links']['cited_by']['cites_id']
        except KeyError:
            d['cites_id'] = None

        inst = cls(**d)
        cache(json, title2file(inst.title), 'publication')
        return inst

    def get_cited_by(self, nres=None, overwrite=False):
        if overwrite:
            self.query_cited_by()
        elif self.cites_id is None:
            core_logger.info(global_indent + f'no citing articles for {self.title}')
            self._cited_by = []
        elif self._cited_by is None: 
            queries = self.query_cited_by(nres, overwrite) # note this checks the cache
            self._cited_by = [Publication.from_json(result) for result in extract_orgres(queries)]

        return self._cited_by

    def query_cited_by(self, nres=None, overwrite=False):
        cited_by_dictionary['cites'] = self.cites_id
        core_logger.info(global_indent + f'getting cited by results for {self.title}')
        return query(cited_by_dictionary, nres, overwrite)

    def set_cited_by(self, cited_by):
        self._cited_by = cited_by

    def get_cite(self, overwrite=False):
        if overwrite:
            self.query_cite()
        elif self._cite is None:
            cache_res = load_cache(title2file(self.title), 'cite')
            if cache_res is None:
                self.query_cite()
            else:
                self._cite = Citation.from_json(cache_res)
        return self._cite

    def query_cite(self):
        cite_dictionary['q'] = self.result_id
        core_logger.info(global_indent + f'getting cite data for {self.title}')
        dt, data = json_request(cite_dictionary)
        core_logger.info(global_indent + f'took {dt}s')
        global_checker.increment()
        self._cite = Citation.from_json(data)
        cache(data, title2file(self.title), 'cite')

    def set_cite(self, cite):
        self._cite = cite
