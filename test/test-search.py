from serp.env import test_logger
import serp.query
from serp.dummy import dummy_reqget
serp.query.reqget = dummy_reqget
import serp.core

serp.core.search('DUMMY_SEARCH')
serp.core.search('DUMMY_SEARCH', nres=35)
queries = serp.core.search('DUMMY_SEARCH', overwrite=True)
test_logger.info(f'total number of searches {serp.env.global_checker.cum_search}')

assert len(queries) == len(set(queries))
