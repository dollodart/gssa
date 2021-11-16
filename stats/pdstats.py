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
