from serp.env import INPUT_DIR, test_logger
from serp.dummy import dummy_reqget

import serp.query
serp.query.reqget = dummy_reqget

from serp.gprofile import schol_list, gprofile_search 

with open(f'{INPUT_DIR}/aeinstein.html', 'r') as _:
    l = schol_list(_)
    for title, authors, journal in l:
        test_logger.info(f'{title}--{",".join(authors)}--{journal}')
    publist = gprofile_search(l)
