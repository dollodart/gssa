from serp.env import global_indent, test_logger

from serp.dummy import dummy_reqget, DUMMY_DATA_ORGANIC_RESULT
import serp.query
serp.query.reqget = dummy_reqget

import serp.core
from serp.graph_search import (depth_first_search as dfs,
        breadth_first_search as bfs)

def myfilter(x):
    # just used to test_logger.info, not apply a filter
    test_logger.info(global_indent + x.title)
    return True

pub0 = serp.core.Publication.from_json(DUMMY_DATA_ORGANIC_RESULT)

n = 4

cited_by = []
for _ in range(n):
    DUMMY_DATA_ORGANIC_RESULT['title'] = str(_)
    cited_by.append(DUMMY_DATA_ORGANIC_RESULT.copy())

pub0.set_cited_by([serp.core.Publication.from_json(x) for x in cited_by])

for c, pub1 in enumerate(pub0.get_cited_by()):
    cited_by = []
    for _ in range(n):
        DUMMY_DATA_ORGANIC_RESULT['title'] = str(n*c + n + _)
        cited_by.append(DUMMY_DATA_ORGANIC_RESULT.copy())
    pub1.set_cited_by([serp.core.Publication.from_json(x) for x in cited_by])

test_logger.info('dfs')
dfs(pub0, levels=3, filters=(myfilter,))
test_logger.info('bfs')
bfs(pub0, levels=3, filters=(myfilter,))