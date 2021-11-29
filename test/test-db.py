from serp.structio import publist2df
from serp.env import test_logger

def journal_metrics(publication_df):
    publication_df['plen'] = publication_df['pageupper'] - publication_df['pagelower']
    journ_df = publication_df.groupby('journal')[['cited_by_count', 'plen']].agg(['mean', 'std'])
    test_logger.info(journ_df.sort_values(by=('cited_by_count', 'mean')))
    test_logger.info(journ_df.sort_values(by=('plen', 'mean')).dropna())
    # this doesn't reproduce pdstats

def citer_citee(publication_df, author_df, cited_by_df):
    """
    Valid because an author's name appears once in any publication.  Any author
    in a citing publication is considered citing every author in a cited
    publication.
    """
    publication_author_df = publication_df.merge(author_df,
            how='inner', on='primary_key').drop_duplicates()
    df_r = publication_author_df.merge(cited_by_df,
            how='inner', on='primary_key').drop_duplicates()
    df_r = df_r.drop('primary_key', axis=1) 
    df_e = publication_author_df.merge(cited_by_df.drop('primary_key',axis=1),
            how='inner', left_on='primary_key', right_on='secondary_key').drop_duplicates()
    df_e = df_e.drop('secondary_key', axis=1)
    df = df_r.merge(df_e,how='inner', left_on='secondary_key', right_on='primary_key',
            suffixes=('-citer', '-citee')).drop_duplicates()

    gr = df.groupby(['author-citer', 'author-citee'])['title-citer']
    agg = gr.agg('count').sort_values()
    # self-citing (need separate for normalization by publication counts)
    bl = agg.index.get_level_values(0) == agg.index.get_level_values(1)
    test_logger.info('who cites who')
    test_logger.info(agg)
    test_logger.info('\nsummary of self citation')
    test_logger.info(agg[bl])

    # normalized self-citation by publication counts
    # citations made by an author, all and to themselves
    total_citations = df.groupby('author-citer')['title-citee'].agg('nunique')
    sdf = df[df['author-citer'] == df['author-citee']]
    total_self_citations = sdf.groupby('author-citer')['title-citee'].agg('nunique')
    frac_self = total_self_citations / total_citations
    frac_self = frac_self.dropna().sort_values()
    test_logger.info('\nself-citation fraction of citations')
    test_logger.info(frac_self)
    test_logger.info('\ntotal fraction of citations which are self-citing: ' + 
         f'{100*total_self_citations.sum()/total_citations.sum():.1f}%')
    # this doesn't reproduce test-stats, or pdstats, if the data contains publications without authors

if __name__ == '__main__':
    from serp.core import load_cached_publications_hq
    publist = load_cached_publications_hq()

    publication_df, author_df, cited_by_df = publist2df(publist)
    journal_metrics(publication_df)
    citer_citee(publication_df, author_df, cited_by_df)
