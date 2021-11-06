DUMMY_DATA = {
        'title':'dummy()',
        'link':None,
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
