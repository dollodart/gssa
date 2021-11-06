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

DUMMY_DATA_CITE = DUMMY_DATA_ORGANIC_RESULT.copy()
DUMMY_DATA_CITE['citations'] = (
            {'title':'MLA','snippet':None},
            {'title':'APA','snippet':''},
            {'title':'Chicago','snippet':''},
            {'title':'Harvard','snippet':''},
            {'title':'Vancouver','snippet':''}
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

def dummy_reqget(URL, params): 
    raise KeyError
    # only directly called by pagination

def dummy_json_request(parameters):
    try:
        if parameters['engine'] == 'google_scholar':
            try:
                parameters['cites']
                return 0, DUMMY_DATA_CITED_BY # could also be searching within
            except KeyError:
                return 0, DUMMY_DATA_SEARCH
        elif parameters['engine'] == 'google_scholar_cite':
                return 0, DUMMY_DATA_CITE
    except KeyError: # pagination result, or other
        return 0, DUMMY_DATA_SEARCH
