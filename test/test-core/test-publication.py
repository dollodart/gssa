import serp.userenv
serp.userenv.CACHE_DIR = serp.userenv.DUMMY_CACHE_DIR

from serp.env import global_indent, test_logger
from serp.dummy import DUMMY_DATA_ORGANIC_RESULT

from serp.dummy import dummy_reqget
import serp.query
serp.query.reqget = dummy_reqget

import serp.core

ROOT = DUMMY_DATA_ORGANIC_RESULT.copy()
ROOT['title'] = 'root'
pub0 = serp.core.Publication.from_json(ROOT)
test_logger.info(f'created {pub0.title}')
citation = pub0.get_cite()
global_indent += 2
publist = pub0.get_cited_by()
for pub in publist:
    pub.get_cite()
    test_logger.info(global_indent + f'found {pub.title} as citing article of {pub0.title}')

assert len(publist) == len(set(publist))
