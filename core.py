import pathlib
import requests
from time import time, sleep
from env import cited_by_dictionary, cite_dictionary, query_dictionary, pagination_dictionary
from env import CACHE_DIR, URL
from env import logging



def title2file(string):
    """Makes a filename from a publication title by replacing special characters with escape codes."""
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

def json_request(parameters):
    t0 = time()
    data = requests.get(URL, params=parameters)
    return time() - t0, data.json()

def flatten_pagination(data, level=0):
    """Given data with a link to more pages, get all the data and then
    return a flattened data structure."""

    t0 = time()
    lst = []
    while True:
        lst.extend(data['organic_results'])
        try:
            link = data['serpapi_pagination']['next']
            dt, data = json_request(link, pagination_dictionary)
            logging.info(2 * level * ' ' + 'pulled another page')
            global_checker.increment()
        except KeyError:
            break
    return time() - t0, lst


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


global_checker = Checker()
global_cache = [f.name for f in pathlib(f'{CACHE_DIR}').iterdir()]


class Citation:
    def __init__(self,
                 mla,
                 apa,
                 harvard,
                 vancouver,
                 bibtex,
                 endnote,
                 refman,
                 refworks):
        self.mla = mla
        self.apa = apa
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
            d[ldct['name']] = ldct['link']
        return cls(**d)



class Publication:
    def __init__(self,
                 title,
                 position,
                 result_id,
                 cites_id,
                 publication_summary,
                 authors_summary,
                 cited_by_count,
                 level=0
                 ):
        self.title = title
        self.file = title2file(self.title)
        self.result_id = result_id
        self.cites_id = cites_id
        self.publication_summary = publication_summary
        self.authors_summary = authors_summary
        self.cited_by_count = cited_by_count
        self.level = level

        self.indent = self.level * 2 * ' '

    @classmethod
    def from_json(cls, json, level=0):
        """
        Initialize a publication from a search result.
        """

        d = dict(
            title=json['title'],
            position=json['position'],
            result_id=json['result_id'],
            abstract=json['snippet'],
            publication_summary=json['publication_info']['summary'],
            level=level)
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

        inst = cls(d)
        inst.cache_json(json)
        return inst

    def cache_json(self, json):
        global_cache.append(self.file)
        with open(f'{CACHE_DIR}/{self.file}', 'w') as _:
            _.write(json)
        return None

    def get_cited_by(self):
        if self.cites_id is None:
            logging.info(self.indent + 'no citing articles for {self.title}')
            self.neighbors = []
            return self.neighbors
        cited_by_dictionary['cites'] = self.cites_id
        logging.info(self.indent + 'getting cited by results for {self.title}')
        dt, data = json_request(cited_by_dictionary)
        logging.info(self.indent + f'took {dt}s')
        global_checker.increment()
        # flatten the pagination (makes queries)
        logging.info(self.indent + 'querying and flattening paginated results')
        dt, data = flatten_pagination(data, level=self.level)
        logging.info(self.indent + f'took {dt}s for {len(data)} results')
        self.neighbors = [Publication.from_json(
            result, level=self.level+1) for result in data]
        return self.neighbors

    def get_cite(self, result_id):
        cite_dictionary['q'] = self.result_id
        logging.info(self.indent + 'getting cite data for {self.title}')
        dt, data = json_request(cite_dictionary)
        logging.info(self.indent + 'took {dt}s')
        global_checker.increment()
        self.cite = Citation.from_json(data)
        return self.cite

def query(query_term):
    query_dictionary['q'] = query_term
    logging.info(f'finding first page in query for term:{query_term}')
    dt, data = json_request(query_dictionary)
    logging.info(f'found in {dt}s')
    logging.info(f'querying and flattening pagination')
    dt, data = flatten_pagination(data)
    logging.info(f'took {dt}s for {len(data)} results')
    return [Publication.from_json(d) for d in data]
