from serp.stats.metrics import hindex, gindex, i10index, oindex, windex
from serp.stats.tempmodule import load_data
from serp.stats import citer_citee_pairs, citee_ncitations

def test_citer_citee_pairs(publist):
    ccp = citer_citee_pairs(publist)
    s = sum(ccp[k] for k in ccp)
    ccp_items = sorted(ccp.items(), key=lambda i:-i[1])
    print('citer citee pairs')
    for k, v in ccp_items[:10]:
        print(k, f'{v:.2f}')

    tot = self = 0
    for k in ccp:
        a1, a2 = k.split('-', maxsplit=1)
        if a1 == a2:
            self += ccp[k]
        tot += ccp[k]
    print(f'fraction self-citations = {100*self / tot:.1f}%')

def test_citee_ncitations(publist):
    cnc = citee_ncitations(publist)
    cnc_items = sorted(((k, sum(v)) for k, v in cnc.items()), key=lambda i:-i[1])
    print('citee ncitations')
    for k, v in cnc_items[:10]:
        print(k, v)

    print('\nmetrics')
    for metric in hindex, gindex, i10index, oindex, windex:
        smetrics = sorted([(k, metric(cnc[k])) for k in cnc], key = lambda x:-x[1])
        print('\n', metric, sep='')
        for k, v in smetrics[:10]:
            print(k, f'{v:.2f}')

if __name__ == '__main__':
    publist = load_data()
    test_citer_citee_pairs(publist)
    test_citee_ncitations(publist)
