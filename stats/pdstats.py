import numpy as np
import pandas as pd

def citer_citee(publist, position=0):
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

def pubdf(publist):
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
                'pages':c.pages}
        nl.append(nd)
    df = pd.DataFrame(nl)
    return df

if __name__ == '__main__':
    from tempmodule import load_data
    publist = load_data()
    df = citer_citee(publist, position=-1)
    bl = df['citer'] == df['citee']
    self_cite = df[bl].groupby('citer')['citee'].agg('count').sort_values()
    all_cite = df.groupby('citer')['citee'].agg('count').sort_values()
    print(self_cite, all_cite, self_cite / all_cite)

    j2j = df.groupby(['citing journal', 'cited journal'])['citee'].agg('count').sort_values()
    print(j2j)

    def plen(x):
        if type(x) is not tuple:
            x = x,
        if len(x) == 2:
            return x[1] - x[0]
        return np.nan

    df = pubdf(publist)
    df['plen'] = df['pages'].map(plen)

    ndf = df.explode('authors')
    print(ndf.groupby('authors')['cited by count'].agg(['sum', 'mean', 'std']).sort_values(by='sum'))
    # journal metrics
    journ_df = ndf.groupby('journal')[['cited by count', 'plen']].agg(['mean', 'std'])
    print(journ_df.sort_values(by=('cited by count', 'mean')))
    print(journ_df.sort_values(by=('plen', 'mean')).dropna())
