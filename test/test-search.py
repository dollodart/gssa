import serp.env
import serp.query
from serp.dummy import dummy_reqget
serp.query.reqget = dummy_reqget
import serp.core

serp.core.search('DUMMY_SEARCH')
serp.core.search('DUMMY_SEARCH', nres=35)
print('total number of searches', serp.env.global_checker.cum_search)
