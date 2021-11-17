import pandas as pd
from datetime import datetime

def mydatetime(obj):
    if type(obj) is datetime:
        return obj
    raise Exception

pr_dtype = {'primary_key':int,
            'title': str,
            'abstract': str,
            'publication_summary': str,
            'cited_by_count': float,
            'journal': str,
            'date': 'datetime64[ns]', # is datetime when parsed
            'vol': float,
            'issue': float,
            'pagelower': float,
            'pageupper': float}

pr_typecaster = pr_dtype.copy()
pr_typecaster['date'] = mydatetime

def publist2df(publist):
    pub_records = []
    auth_records = []
    citedby_records = []
    for pub in publist:
        primary_key = hash(pub.title)
        fields1 = 'title', 'abstract', 'publication_summary', 'cited_by_count'
        precord = [primary_key]
        for f in fields1:
            try:
                typecaster = pr_typecaster[f]
                precord.append(typecaster(getattr(pub, f)))
            except Exception:
                precord.append(None)

        cite = pub.get_cite()
        fields2 = 'journal', 'date', 'vol', 'issue', 'pagelower', 'pageupper'
        for f in fields2:
            try:
                typecaster = pr_typecaster[f]
                precord.append(typecaster(getattr(pub, f)))
            except Exception:
                precord.append(None)

        pub_records.append(precord) 

        if cite.authors is not None:
            for auth in cite.authors:
                auth_records.append([primary_key, auth])

        for pub2 in pub.get_cited_by():
            secondary_key = hash(pub2.title)
            citedby_records.append([primary_key, secondary_key])

    pub_cols = tuple(zip(*pub_records))
    cols = ('primary_key',) + fields1 + fields2
    series = dict()
    for c in range(len(cols)):
        ser = pd.Series(pub_cols[c], name=cols[c], dtype=pr_dtype[cols[c]])
        series[cols[c]] = ser

    pub_df = pd.DataFrame(series)
    auth_df = pd.DataFrame(auth_records, columns = ['primary_key', 'author'])
    citedby_df = pd.DataFrame(citedby_records, columns=['primary_key', 'secondary_key'])
    return pub_df, auth_df, citedby_df

if __name__ == '__main__':
    from tempmodule import load_data
    publist = load_data()
    pubdf, authdf, citedby_df = publist2df(publist)

    pubdf['plen'] = pubdf['pageupper'] - pubdf['pagelower']
    journ_df = pubdf.groupby('journal')[['cited_by_count', 'plen']].agg(['mean', 'std'])
    print(journ_df.sort_values(by=('cited_by_count', 'mean')))
    print(journ_df.sort_values(by=('plen', 'mean')).dropna())
    # this doesn't reproduce pdstats

    # who cites who
    # valid because an author's name appears once in any publication
    # any author in a citing publication is considered citing every author in a cited publication
    pubauthdf = pubdf.merge(authdf, how='inner', on='primary_key').drop_duplicates()
    df_r = pubauthdf.merge(citedby_df, how='inner', on='primary_key').drop_duplicates()
    df_r = df_r.drop('primary_key', axis=1) 
    df_e = pubauthdf.merge(citedby_df.drop('primary_key',axis=1), how='inner',
            left_on='primary_key', right_on='secondary_key').drop_duplicates()
    df_e = df_e.drop('secondary_key', axis=1)
    df = df_r.merge(df_e, how='inner', left_on='secondary_key', right_on='primary_key', suffixes=('-citer', '-citee')).drop_duplicates()

    gr = df.groupby(['author-citer', 'author-citee'])['title-citer']
    agg = gr.agg('count').sort_values()
    # self-citing (need separate for normalization by publication counts)
    bl = agg.index.get_level_values(0) == agg.index.get_level_values(1)
    print('who cites who')
    print(agg)
    print('\nsummary of self citation')
    print(agg[bl])

    # normalized self-citation by publication counts
    # citations made by an author, all and to themselves
    total_citations = df.groupby('author-citer')['title-citee'].agg('nunique')
    sdf = df[df['author-citer'] == df['author-citee']]
    total_self_citations = sdf.groupby('author-citer')['title-citee'].agg('nunique')
    frac_self = total_self_citations / total_citations
    frac_self = frac_self.dropna().sort_values()
    print('\nself-citation fraction of citations')
    print(frac_self)
    print('\ntotal fraction of citations which are self-citing: ' + 
         f'{100*total_self_citations.sum()/total_citations.sum():.1f}%')
    # this doesn't reproduce test-stats, or pdstats
