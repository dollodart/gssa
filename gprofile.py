import gssa.core
from .env import global_indent, core_logger
from bs4 import BeautifulSoup


def schol_list(tbody):
    """
    Takes <tbody class="gsc_a_b"> html input from google scholar profile and
    returns title, author, and journal.
    """

    html = BeautifulSoup(tbody, features='html.parser')

    l = []
    while html:
        el = html.tr
        if el is None:
            break
        if el.a is None:
            continue
        title = el.a.text
        el.a.decompose()
        if el.div is None:
            continue
        authors = el.div.text
        el.div.decompose()
        if el.div is None:
            journal = None
        else:
            journal = el.div.text
        if el is not None:
            el.decompose()

        title = title.strip('\n')
        authors = tuple(x.strip() for x in authors.split(','))
        journal = journal.strip('\n')

        l.append((title, authors, journal))

    return l


def gprofile_search(taj):
    publist = []
    for title, authors, journal in taj:
        core_logger.info(f'querying {title}--{",".join(authors)}--{journal}')
        query = title + ' ' + journal
        pubs = gssa.core.search(query, nres=20)
        pub = pubs[0]
        # gprofile article title may not match the search result one
        # one can use edit distance to quantify the match and choose the best one
        if len(pubs) > 1:
            core_logger.warn(
                global_indent + f'more than one result found for "{query}"')
            core_logger.warn(
                global_indent + f'returning first result "{pub.title}"')
        # note the search result is still cached, and gssa.core.search returns publications which are also cached
        publist.append(pub)
    return publist
