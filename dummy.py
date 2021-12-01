from copy import copy, deepcopy
DUMMY_DATA_SEARCH = {
    'search_metadata': {
        'id': 'he24da18a',
        'status': 'Success',
        'json_endpoint': 'https://dummyurl.com/searches/he24da18a/he24da18a.json',
        'created_at': '2000-01-01 00:00:01 UTC',
        'processed_at': '2000-01-01 00:00:00 UTC',
        'google_scholar_url': 'https://scholar.google.com/scholar?&...',
        'raw_html_file': 'https://dummyurl.com/searches/he24da18a/he24da18a.html',
        'total_time_taken': 0
    },
    'search_information': {
        'total_results': 10000,
        'time_taken_displayed': 0.06,
        'query_displayed': 'dummy'
    },
    'organic_results': [],
    'pagination': {
        'current': 1,
        'next': 'https://scholar.google.com/scholar?start=10&...'
    },
    'serpapi_pagination': {
        'current': 1,
        'next': 'https://dummyurl.com/search.json?as_sdt=0%2C5&engine=google_scholar&hl=en&...'
    }
}

DUMMY_DATA_ORGANIC_RESULT = {
    'title': 'dummy(0)',
    'link': None,
    'position': None,
    'result_id': None,
    'snippet': None,
    'serpapi_pagination': {'link': None},
    'publication_info': {'summary': None,
                         'authors': ({'name': None,
                                      'link': None},)},
    'inline_links': {
        'cited_by': {
            'total': None, 'cites_id': ''
        },
        'versions': {
            'total': 6}
    }
}

DUMMY_DATA_CITE = dict()
DUMMY_DATA_CITE['citations'] = (
    {'title': 'MLA',
        'snippet': 'Sherman, Melanie A., Dominique A. Weber, and Peter E. Jensen. "Article." Immunity 3.2 (1995): 197-205.'},
    {'title': 'APA', 'snippet': ''},
    {'title': 'Chicago', 'snippet': ''},
    {'title': 'Harvard', 'snippet': ''},
    {'title': 'Vancouver',
     'snippet': 'Sherman MA, Weber DA, Jensen PE. Article. Immunity. 1995 Aug 1;3(2):197-205.'}
)
DUMMY_DATA_CITE['links'] = (
    {'name': 'Bibtex', 'link': ''},
    {'name': 'EndNote', 'link': ''},
    {'name': 'RefWorks', 'link': ''},
    {'name': 'RefMan', 'link': ''}
)

n = n0 = 10
orgres = []
while n > 0:
    DUMMY_DATA_ORGANIC_RESULT['title'] = f'dummy({n0-n})'
    orgres.append(deepcopy(DUMMY_DATA_ORGANIC_RESULT))
    n -= 1

DUMMY_DATA_SEARCH['organic_results'] = orgres
DUMMY_DATA_CITED_BY = deepcopy(DUMMY_DATA_SEARCH)  # may be distinct
DUMMY_DATA_SEARCH_TERMINAL = deepcopy(DUMMY_DATA_SEARCH)
del DUMMY_DATA_SEARCH_TERMINAL['serpapi_pagination']['next']


class DummyResult(dict):
    def json(self):
        return self


class DummyServer:
    def __init__(self):
        self.dummy_counter = 0
        self.pagination = 0

    def route(self, URL, params):
        try:
            if params['engine'] == 'google_scholar':
                try:
                    params['cites']
                    return self.get_cited_by()
                except KeyError:
                    return self.get_search()
            elif params['engine'] == 'google_scholar_cite':
                return self.get_cite()
        except Exception:
            return self.get_other()

    def get(self, dummy_data):
        self.dummy_counter += 1
        return DummyResult(dummy_data)

    def get_cited_by(self):
        for c, orgr in enumerate(DUMMY_DATA_CITED_BY['organic_results']):
            orgr['title'] = f'{self.dummy_counter}/{c}'
        return 0, self.get(DUMMY_DATA_CITED_BY)

    def get_search(self):
        for c, orgr in enumerate(DUMMY_DATA_SEARCH['organic_results']):
            orgr['title'] = f'{self.dummy_counter}/{c}'
        return 0, self.get(DUMMY_DATA_SEARCH)

    def get_cite(self):
        return 0, self.get(DUMMY_DATA_CITE)

    def get_other(self):
        self.pagination += 1
        if self.pagination > 10:
            dds = DUMMY_DATA_SEARCH_TERMINAL
            dds['serpapi_pagination']['current'] = 10
            self.pagination = 0
        else:
            dds = DUMMY_DATA_SEARCH
            dds['serpapi_pagination']['current'] = self.pagination

        for c, orgr in enumerate(dds['organic_results']):
            orgr['title'] = f'{self.dummy_counter}/{c}'
        return 0, self.get(dds)


dummy_server = DummyServer()


def dummy_reqget(URL, params):
    global dummy_server
    return dummy_server.route(URL, params)
