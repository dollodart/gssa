from serp.env import INPUT_DIR, core_logger
from serp.secretenv import author_gprofile
from serp.gprofile import schol_list, gprofile_search 

with open(INPUT_DIR.joinpath(author_gprofile), 'r') as _:
    taj = schol_list(_)

publist = []
publist = gprofile_search(taj)

# the same thing as below can be achieved using graph_search, but without error control
for pub in publist:
    pub.get_cite()
    try:
        publist2 = pub.get_cited_by(nres=50) # only get the first 50 results
        print(len(publist2))
        for pub2 in publist2:
            try:
                pub2.get_cite()
            except TypeError:
                core_logger.warning(f'{pub2.title} had get_cite error')
    except KeyError:
        core_logger.warning(f'{pub.title} had query error for cited by')
