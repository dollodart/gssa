import serp.env

import serp.query
from serp.dummy import dummy_reqget
serp.query.reqget = dummy_reqget

import serp.core
from serp.dummy import DUMMY_DATA_ORGANIC_RESULT
from serp.dummy import DUMMY_DATA_CITE

serp.core.search('DUMMY_SEARCH')
serp.core.search('DUMMY_SEARCH', nres=35)
pub = serp.core.Publication.from_json(DUMMY_DATA_ORGANIC_RESULT)
pub.get_cite()
serp.env.global_indent += 2
pub.get_cited_by()
print('total number of searches', serp.env.global_checker.cum_search)

cit = serp.core.Citation.from_json(DUMMY_DATA_CITE)
for attr in 'authors', 'title', 'journal', 'date', 'vol', 'issue', 'pages':
    print(attr, getattr(cit, attr))
