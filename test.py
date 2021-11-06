import core
from dummy import DUMMY_DATA_ORGANIC_RESULT, dummy_reqget, dummy_json_request

core.reqget = dummy_reqget
core.json_request = dummy_json_request
core.query('my_query')
pub = core.Publication.from_json(DUMMY_DATA_ORGANIC_RESULT)
pub.get_cite()
core.global_indent += 2
pub.get_cited_by()
print('total number of searches', core.global_checker.cum_search)
