from serp.stats.tempmodule import load_data
from serp.structio import extract_publication_df, extract_citer_citee_df

publist = load_data()

df = extract_publication_df(publist)
df['plen'] = df['pageupper'] - df['pagelower']
df['plen'] = df['plen'].astype('float64') # not sure why this is needed, but maybe specify dtypes

ndf = df.explode('authors')
print('author productivity (cited by count, statistics w.r.t. publications)')
print(ndf.groupby('authors')['cited by count'].agg(['sum', 'mean', 'std']).sort_values(by='sum'))

# journal metrics
journ_df = ndf.groupby('journal')[['cited by count', 'plen']].agg(['mean', 'std'])
print('journal publication metrics')
print(journ_df.sort_values(by=('cited by count', 'mean')))
print(journ_df.sort_values(by=('plen', 'mean')).dropna())

df = extract_citer_citee_df(publist, position=-1)
bl = df['citer'] == df['citee']
self_cite = df[bl].groupby('citer')['citee'].agg('count').sort_values()
all_cite = df.groupby('citer')['citee'].agg('count').sort_values()
print('self-cite')
print(self_cite)
print('all-cite')
print(all_cite)
print('fraction self-cite')
print(self_cite / all_cite)
print('\nfraction self-citations overall', self_cite.sum() / all_cite.sum())

j2j = df.groupby(['citing journal', 'cited journal'])['citee'].agg('count').sort_values()
print('which journals cite which journals')
print(j2j)
