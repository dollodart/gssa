import gssa.core
from gssa.dummy import dummy_reqget
import gssa.query
from gssa.env import test_logger
import gssa.userenv
gssa.userenv.CACHE_DIR = gssa.userenv.DUMMY_CACHE_DIR

gssa.query.reqget = dummy_reqget

searches = [gssa.core.search('DUMMY_SEARCH'),
            gssa.core.search('DUMMY_SEARCH', nres=20),
            gssa.core.search('DUMMY_SEARCH', overwrite=True),
            gssa.core.search('DUMMY_SEARCH', nres=30, overwrite=True)]
for c, publist in enumerate(searches):
    print(c)
    assert len(publist) == len(set(publist))

test_logger.info(
    f'total number of searches {gssa.env.global_checker.cum_search}')
