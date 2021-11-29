import numpy as np
import networkx.algorithms as nxa
from serp.structio import publist2digraph
from serp.env import test_logger

def characterize(G):
    recip = nxa.reciprocity(G)
    windex = nxa.wiener_index(G)
    # fh = nxa.flow_hierarchy(G) # flow_hierarchy = 1 - reciprocity? 
    acluster = nxa.average_clustering(G)
    return (f'reciprocity = {recip:.2f}, Wiener index = {windex:.2f}\n' + 
            f'average clustering = {acluster:.2f}')

def centralities_top3(G):

    top3s = dict() 
    for alg in (nxa.centrality.degree_centrality,
            nxa.centrality.eigenvector_centrality,
            nxa.centrality.closeness_centrality,
            nxa.centrality.betweenness_centrality):
        d = alg(G)
        skeys = sorted(d, key=lambda x:d[x])
        top3s[alg] = []
        for key in skeys[-3:][::-1]:
            top3s[alg].append((key, d[key]))
    return top3s

def degree_deciles(G):

    ind = np.array(tuple(x[1] for x in G.in_degree))
    outd = np.array(tuple(x[1] for x in G.out_degree))
    bl = ind > 0
    rat = outd[bl] / ind[bl]
    q = np.linspace(0, 1, 11)
    return np.quantile(ind, q), np.quantile(outd, q), np.quantile(rat, q)

if __name__ == '__main__':
    from serp.core import load_cached_publications_hq
    publist = load_cached_publications_hq()

    G = publist2digraph(publist)

    st1 = characterize(G)
    G.remove_nodes_from([x[0] for x in G.out_degree if x[1] < 1])
    st2 = characterize(G)
    test_logger.info(f'{st1} {st2}')

    ind, outd, rat = degree_deciles(G)
    test_logger.info('in-degree deciles ' + '-'.join(f'{x:.1f}' for x in ind))
    test_logger.info('out-degree deciles ' + '-'.join(f'{x:.1f}' for x in outd))
    test_logger.info('out-degree/in-degree deciles ' + '-'.join(f'{x:.1E}' for x in rat))

    top3s = centralities_top3(G)
    for k in top3s:
        test_logger.info(str(k))
        for pub, value in top3s[k]:
            test_logger.info(f'{pub.title} has centrality {value:.2f}')
