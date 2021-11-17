import serp.env
from serp.dummy import DUMMY_DATA_CITE
import serp.core
cit = serp.core.Citation.from_json(DUMMY_DATA_CITE)
for attr in 'authors', 'title', 'journal', 'date', 'vol', 'issue', 'pages':
    print(attr, getattr(cit, attr))
