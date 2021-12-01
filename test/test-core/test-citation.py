import gssa.core
from gssa.dummy import DUMMY_DATA_CITE
from gssa.env import test_logger
import gssa.userenv
gssa.userenv.CACHE_DIR = gssa.userenv.DUMMY_CACHE_DIR

cit = gssa.core.Citation.from_json(DUMMY_DATA_CITE)
for attr in 'authors', 'title', 'journal', 'date', 'vol', 'issue', 'pageupper', 'pagelower':
    aval = getattr(cit, attr)
    test_logger.info(f'{attr} {str(aval)}')
