import pathlib
import requests
from time import time, sleep
from env import cited_by_dictionary, cite_dictionary, query_dictionary, pagination_dictionary
from env import CACHE_DIR, URL
from env import logging
import json as jsonlib


def title2file(string):
    """Makes a filename from a publication title by replacing special
    characters with escape codes."""

    for replacee, replacement in (('-', '.dash.'),
                                  (', ', ','),  # commas are allowed
                                  (' ', '-'),
                                  ('/', '.fslash.'),
                                  ('(', '.lparan.'),
                                  (')', '.rparan.'),
                                  ('?', '.qmark.'),
                                  ('*', '.star.')):
        string = string.replace(replacee, replacement)

    return string

class Checker:
    hourly_limit = 1000

    def __init__(self, cum_search=0, fail_thresh=10):
        self.cum_search = cum_search
        self.fail = 0
        self.fail_thresh = fail_thresh

    def increment(self):
        self.cum_search += 1
        if self.cum_search > self.hourly_limit * 0.95:
            logging.info('##\n'
                         f'past hourly limit of {self.hourly_limit}, sleeping until limit refresh')
            sleep(3600)
            self.cum_search = 0

    def increment_failure(self):
        self.fail += 1
        if self.fail > self.fail_thresh:
            i = input(
                'there have been greater than 10 failures, continue? [y/N]: ')
            if i == 'y':
                fail_thresh = input(
                    'input an integer number for failure threshold [10]: ')
                while True:
                    if fail_thresh:
                        try:
                            self.fail_thresh = int(fail_thresh)
                            break
                        except ValueError:
                            fail_thresh = input(
                                'try again, input an integer number of failures [10]: ')
                    else:
                        self.fail_thresh = 10
                        break
            self.fail = 0


class Indent:
    def __init__(self):
        self.indent = 0
    def __add__(self, other): 
        # should also be used for __radd__ in case of `3 + indent` or similar
        if type(other) is int:
            self.indent += other
            return self
        elif type(other) is Indent:
            self.indent += other.indent
            return self
        elif type(other) is str:
            return str(self) + other
    def __sub__(self, other):
        if type(other) is int:
            self.indent -= other
        elif type(other) is Indent:
            self.indent += other.indent
        return self
    def __str__(self):
        if self.indent > 0:
            return ' '*self.indent
        return ''

# decleration of global instances (all references should come later)
global_indent = Indent()
global_checker = Checker()
global_cache = [f.name for f in pathlib.Path(f'{CACHE_DIR}').iterdir()]

def json_request(parameters):
    t0 = time()
    data = requests.get(URL, params=parameters)
    return time() - t0, data.json()

def cache(data, filename):
    global_cache.append(filename)
    with open(f'{CACHE_DIR}/{filename}', 'w') as _:
        _.write(jsonlib.dumps(data))
    return None

def flatten_pagination(data):
    """Given data with a link to more pages, get all the data and then
    return a flattened data structure."""

    t0 = time()
    lst = []
    while True:
        lst.extend(data['organic_results'])
        try:
            link = data['serpapi_pagination']['next']
            dt, data = json_request(link, pagination_dictionary)
            logging.info(global_indent + 'pulled another page')
            global_checker.increment()
        except KeyError:
            break
    return time() - t0, lst

class Citation:
    def __init__(self,
                 mla,
                 apa,
                 chicago,
                 harvard,
                 vancouver,
                 bibtex,
                 endnote,
                 refman,
                 refworks):
        self.mla = mla
        self.apa = apa
        self.chicago = chicago
        self.harvard = harvard
        self.vancouver = vancouver
        self.bibtex = bibtex
        self.endnote = endnote
        self.refman = refman
        self.refworks = refworks

    @classmethod
    def from_json(cls, json):
        d = {d['title'].lower(): d['snippet'] for d in json['citations']}
        for ldct in json['links']:
            # eventually, follow some of these links
            d[ldct['name'].lower()] = ldct['link']
        return cls(**d)

class Publication:
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

    @classmethod
    def from_json(cls, json):
        """
        Initialize a publication from a search result.
        """

        d = dict(
            title=json['title'],
            position=json['position'],
            result_id=json['result_id'],
            abstract=json['snippet'],
            publication_summary=json['publication_info']['summary'],
            link=json['link']
            )
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
        cache(json, title2file(inst.title))
        return inst

    def get_cited_by(self, overwrite=False):
        if overwrite:
            self.query_cited_by()
        elif self.cites_id is None:
            logging.info(global_indent + f'no citing articles for {self.title}')
            self._cited_by = []
        elif self._cited_by is None: 
            self.query_cited_by()
        return self._cited_by

    def query_cited_by(self):
        cited_by_dictionary['cites'] = self.cites_id
        logging.info(global_indent + f'getting cited by results for {self.title}')
        dt, data = json_request(cited_by_dictionary)
        logging.info(global_indent + f'took {dt}s')
        global_checker.increment()
        # flatten the pagination (makes queries)
        logging.info(global_indent + 'querying and flattening paginated results')
        dt, data = flatten_pagination(data)
        logging.info(global_indent + f'took {dt}s for {len(data)} results')
        self._cited_by = [Publication.from_json(result) for result in data]

    def set_cited_by(self, cited_by):
        self._cited_by = cited_by

    def get_cite(self, overwrite=False):
        if overwrite:
            self.query_cite()
        elif self._cite is None:
            self.query_cite()
        return self._cite

    def query_cite(self):
        cite_dictionary['q'] = self.result_id
        logging.info(global_indent + f'getting cite data for {self.title}')
        dt, data = json_request(cite_dictionary)
        logging.info(global_indent + f'took {dt}s')
        global_checker.increment()
        self._cite = Citation.from_json(data)
        cache(data, title2file(self.title) + '-cite')

    def set_cite(self, cite):
        self._cite = cite


def query(query_term):
    query_dictionary['q'] = query_term
    logging.info(f'finding first page in query for term:{query_term}')
    dt, data = json_request(query_dictionary)
    logging.info(f'found in {dt}s')
    global_checker.increment()
    logging.info(f'querying and flattening pagination')
    dt, data = flatten_pagination(data)
    logging.info(f'took {dt}s for {len(data)} results')
    global_checker.increment()
    return [Publication.from_json(d) for d in data]
