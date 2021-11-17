import serp.env
from serp.dummy import DUMMY_DATA_ORGANIC_RESULT
import serp.core

pub = serp.core.Publication.from_json(DUMMY_DATA_ORGANIC_RESULT)
pub.get_cite()
serp.env.global_indent += 2
pub.get_cited_by()

