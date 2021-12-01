from serp.core import search
from serp.graph_search import breadth_first_search
from serp.secretenv import author_first, author_last, vancouver_author

author = author_first + ' ' + author_last
publist = search(author, nres=100, overwrite=False)

def has_author(pub):
    if author_last in ''.join(x.lower() for x in pub.authors_summary):
        return True
    cite = pub.get_cite() # note this will run a query if not had
    return cite.authors is not None

def has_specific_author(pub, vancouver_author):
    if author_last in ''.join(x.lower() for x in pub.authors_summary):
        return True
    cite = pub.get_cite()
    return vancouver_author in cite.authors

special = lambda pub:has_specific_author(pub, vancouver_author)

breadth_first_search(publist[:100], levels=2, filters=(has_author, special))
