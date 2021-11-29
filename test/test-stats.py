from serp.stats.metrics import hindex, gindex, i10index, oindex, windex
from serp.stats import citer_citee_pairs, citee_ncitations
from serp.env import test_logger

def test_citer_citee_pairs(publist):
    ccp = citer_citee_pairs(publist)
    s = sum(ccp[k] for k in ccp)
    ccp_items = sorted(ccp.items(), key=lambda i:-i[1])
    test_logger.info('citer citee pairs')
    for k, v in ccp_items[:10]:
        test_logger.info(f'{k}:{v:.2f}')

    tot = self = 0
    for k in ccp:
        a1, a2 = k.split('-', maxsplit=1)
        if a1 == a2:
            self += ccp[k]
        tot += ccp[k]
    test_logger.info(f'fraction self-citations = {100*self / tot:.1f}%')

def test_citee_ncitations(publist):
    cnc = citee_ncitations(publist)
    cnc_items = sorted(((k, sum(v)) for k, v in cnc.items()), key=lambda i:-i[1])
    test_logger.info('citee ncitations')
    for k, v in cnc_items[:10]:
        test_logger.info(f'{k}:{v:n}')

    test_logger.info('\nmetrics')
    for metric in hindex, gindex, i10index, oindex, windex:
        smetrics = sorted([(k, metric(cnc[k])) for k in cnc], key = lambda x:-x[1])
        test_logger.info(f'\n{metric}')
        for k, v in smetrics[:10]:
            test_logger.info(f'{k}:{v:.2f}')

if __name__ == '__main__':
    from serp.core import (load_cached_publications, has_cached_cite,
                           has_cached_cited_by)

    filters = has_cached_cite,
    publist = load_cached_publications(filters)
    test_logger.info(f'{len(publist)} publications with cite are being analyzed by citee_ncitations')
    test_citee_ncitations(publist)

    filters = has_cached_cite, has_cached_cited_by
    publist = load_cached_publications(filters)
    test_logger.info(f'{len(publist)} publications with cited_by are being analyzed by citer_citee_pairs')
    test_logger.info(f'dropping all cited_by publications without cite')
    for pub in publist:
        cited_by = pub.get_cited_by()
        ncited_by = [p for p in cited_by if has_cached_cite(p)]
        pub.set_cited_by(ncited_by)
    test_citer_citee_pairs(publist)
