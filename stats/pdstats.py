import numpy as np
import pandas as pd

def make_citer_citee_df(publist, position=0):
    l = []
    for pub in publist:
        pubcite = pub.get_cite()
        fa = pubcite.authors
        if fa is None or len(fa) == 0:
            continue
        for pub2 in pub.get_cited_by():
            pub2cite = pub2.get_cite()
            fa2 = pub2cite.authors
            if fa2 is None or len(fa2) == 0:
                continue
            l.append((pub.title, pubcite.journal, fa[position], pub2.title, pub2cite.journal, fa2[position]))

    rtitle, rjourn, rname, etitle, ejourn, ename = zip(*l)
    df = pd.DataFrame({'citing pub':rtitle, 'citing journal':rjourn, 'citer':rname,
        'cited pub':etitle, 'cited journal':ejourn, 'citee':ename})
    return df

def make_publication_df(publist):
    """
    Returns a dataframe containing publication data (most of which is derived
    from the cite data, or Citation object).
    """
    nl = []
    for pub in publist:
        cbc = pub.cited_by_count
        c = pub.get_cite()

        nd = {'cited by count':cbc,
                'authors':c.authors, 'title':c.title, 'journal':c.journal,
                'date':c.date, 'vol':c.vol, 'issue':c.issue,
                'pageupper':c.pageupper, 'pagelower':c.pagelower}
        nl.append(nd)
    df = pd.DataFrame(nl)
    return df
