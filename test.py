import core
from dummy import DUMMY_DATA, dummy_request

core.json_request = dummy_request
core.query('my_query')
pub = core.Publication.from_json(DUMMY_DATA)
pub.get_cite()
core.global_indent += 2
pub.get_cited_by()
print('total number of searches', core.global_checker.cum_search)
