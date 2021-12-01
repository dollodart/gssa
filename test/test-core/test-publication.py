import gssa.core
import gssa.query
from gssa.dummy import dummy_reqget
from gssa.dummy import DUMMY_DATA_ORGANIC_RESULT
from gssa.env import global_indent, test_logger
import gssa.userenv
gssa.userenv.CACHE_DIR = gssa.userenv.DUMMY_CACHE_DIR


gssa.query.reqget = dummy_reqget


ROOT = DUMMY_DATA_ORGANIC_RESULT.copy()
ROOT['title'] = 'root'
pub0 = gssa.core.Publication.from_json(ROOT)
test_logger.info(f'created {pub0.title}')
citation = pub0.get_cite()
global_indent += 2
publist = pub0.get_cited_by()
for pub in publist:
    pub.get_cite()
    test_logger.info(
        global_indent + f'found {pub.title} as citing article of {pub0.title}')

assert len(publist) == len(set(publist))
