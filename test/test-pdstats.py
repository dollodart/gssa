from serp.stats.tempmodule import load_data
from serp.structio import extract_publication_df, extract_citer_citee_df
from serp.env import test_logger

publist = load_data()

df = extract_publication_df(publist)
df['plen'] = df['pageupper'] - df['pagelower']
df['plen'] = df['plen'].astype('float64') # not sure why this is needed, but maybe specify dtypes

ndf = df.explode('authors')
test_logger.info('author productivity (cited by count, statistics w.r.t. publications)')
test_logger.info(ndf.groupby('authors')['cited by count'].agg(['sum', 'mean', 'std']).sort_values(by='sum'))

# journal metrics
journ_df = ndf.groupby('journal')[['cited by count', 'plen']].agg(['mean', 'std'])
test_logger.info('journal publication metrics')
test_logger.info(journ_df.sort_values(by=('cited by count', 'mean')))
test_logger.info(journ_df.sort_values(by=('plen', 'mean')).dropna())

df = extract_citer_citee_df(publist, position=-1)
bl = df['citer'] == df['citee']
self_cite = df[bl].groupby('citer')['citee'].agg('count').sort_values()
all_cite = df.groupby('citer')['citee'].agg('count').sort_values()
test_logger.info('self-cite')
test_logger.info(self_cite)
test_logger.info('all-cite')
test_logger.info(all_cite)
test_logger.info('fraction self-cite')
test_logger.info(self_cite / all_cite)
test_logger.info(f'\nfraction self-citations overall {100*self_cite.sum() / all_cite.sum():.1f}%')

j2j = df.groupby(['citing journal', 'cited journal'])['citee'].agg('count').sort_values()
test_logger.info('which journals cite which journals')
test_logger.info(j2j)
