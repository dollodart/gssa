from serp.env import test_logger
from serp.dummy import DUMMY_DATA_CITE
import serp.core
cit = serp.core.Citation.from_json(DUMMY_DATA_CITE)
for attr in 'authors', 'title', 'journal', 'date', 'vol', 'issue', 'pageupper', 'pagelower':
    aval = getattr(cit, attr)
    test_logger.info(f'{attr} {str(aval)}')
