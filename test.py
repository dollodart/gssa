import core
import env
from dummy import DUMMY_DATA_ORGANIC_RESULT, dummy_reqget, dummy_json_request

core.query.reqget = dummy_reqget
core.query.json_request = dummy_json_request
#core.search('DUMMY_SEARCH')
pub = core.Publication.from_json(DUMMY_DATA_ORGANIC_RESULT)
pub.get_cite()
env.global_indent += 2
pub.get_cited_by()
print('total number of searches', env.global_checker.cum_search)
