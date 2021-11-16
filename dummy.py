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
        'pagination':{
            'current': 1,
            'next': 'https://scholar.google.com/scholar?start=10&...'
            },
        'serpapi_pagination':{
            'current':1,
            'next': 'https://dummyurl.com/search.json?as_sdt=0%2C5&engine=google_scholar&hl=en&...'
            }
        }

DUMMY_DATA_ORGANIC_RESULT = {
        'title':'dummy(0)',
        'link':None,
        'position':None,
        'result_id':None,
        'snippet':None,
        'serpapi_pagination':{'link':None},
        'publication_info':{'summary':None,
                            'authors':({'name':None,
                                        'link':None},)},
        'inline_links':{
                        'cited_by':{
                                    'total':None,'cites_id':''
                                    },
                        'versions': {
                                    'total':6}
                        }
        }

DUMMY_DATA_CITE = dict()
DUMMY_DATA_CITE['citations'] = (
            {'title':'MLA','snippet':'Sherman, Melanie A., Dominique A. Weber, and Peter E. Jensen. "Article." Immunity 3.2 (1995): 197-205.'},
            {'title':'APA','snippet':''},
            {'title':'Chicago','snippet':''},
            {'title':'Harvard','snippet':''},
            {'title':'Vancouver','snippet':'Sherman MA, Weber DA, Jensen PE. Article. Immunity. 1995 Aug 1;3(2):197-205.'}
            )
DUMMY_DATA_CITE['links'] = (
            {'name':'Bibtex','link':''},
            {'name':'EndNote','link':''},
            {'name':'RefWorks','link':''},
            {'name':'RefMan','link':''}
            )

n = n0 = 10
while n > 0:
    DUMMY_DATA_ORGANIC_RESULT['title'] = f'dummy({n0-n})'
    DUMMY_DATA_SEARCH['organic_results'].append(DUMMY_DATA_ORGANIC_RESULT.copy())
    n -= 1

DUMMY_DATA_CITED_BY = DUMMY_DATA_SEARCH.copy() # may be distinct

class DUMMY_RES(dict):
    def json(self):
        return self

DUMMY_DATA_CITED_BY = DUMMY_RES(DUMMY_DATA_CITED_BY)
DUMMY_DATA_SEARCH = DUMMY_RES(DUMMY_DATA_SEARCH)
DUMMY_DATA_CITE = DUMMY_RES(DUMMY_DATA_CITE)

n = 10
def dummy_reqget(URL, params): 
    try:
        if params['engine'] == 'google_scholar':
            try:
                params['cites']
                return 0, DUMMY_DATA_CITED_BY # could also be searching within
            except KeyError:
                return 0, DUMMY_DATA_SEARCH
        elif params['engine'] == 'google_scholar_cite':
                return 0, DUMMY_DATA_CITE
    except KeyError: # pagination result, or other
        # required to terminate
        DUMMY_DATA_SEARCH['serpapi_pagination']['current'] += 1
        if DUMMY_DATA_SEARCH['serpapi_pagination']['current'] > 10:
            del DUMMY_DATA_SEARCH['serpapi_pagination']['next']
        return 0, DUMMY_DATA_SEARCH
