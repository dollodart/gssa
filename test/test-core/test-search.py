import serp.userenv
serp.userenv.CACHE_DIR = serp.userenv.DUMMY_CACHE_DIR

from serp.env import test_logger
import serp.query
from serp.dummy import dummy_reqget
serp.query.reqget = dummy_reqget
import serp.core

searches = [serp.core.search('DUMMY_SEARCH'),
        serp.core.search('DUMMY_SEARCH', nres=20),
        serp.core.search('DUMMY_SEARCH', overwrite=True),
        serp.core.search('DUMMY_SEARCH', nres=30, overwrite=True)]
for c, publist in enumerate(searches):
    print(c)
    assert len(publist) == len(set(publist))
    
test_logger.info(f'total number of searches {serp.env.global_checker.cum_search}')
