import core

DUMMY_DATA = {
        'title':'dummy()',
        'position':None,
        'result_id':None,
        'snippet':None,
        'serpapi_pagination':{'link':None},
        'citations':({'title':'MLA','snippet':None},
        {'title':'APA','snippet':''},
        {'title':'Chicago','snippet':''},
        {'title':'Harvard','snippet':''},
        {'title':'Vancouver','snippet':''}),
        'links':({'name':'Bibtex','link':''},
                 {'name':'EndNote','link':''},
                 {'name':'RefWorks','link':''},
                 {'name':'RefMan','link':''}),
        'publication_info':{'summary':None,'authors':({'name':None,'link':None},)},
        'organic_results': [],
        'inline_links':{'cited_by':{'total':None,'cites_id':''}}
        }

def dummy_request(parameters, level=None):
    return 0, DUMMY_DATA
core.json_request = dummy_request

core.query('my_query')
pub = core.Publication.from_json(DUMMY_DATA)
pub.get_cite()
core.global_indent += 2
pub.get_cited_by()
print('total number of searches', core.global_checker.cum_search)
