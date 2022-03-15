import numpy as np
import networkx
import networkx.algorithms as nxa
from gssa.structio import publist2digraph, publist2authordigraph
from gssa.env import test_logger
from scipy.special import binom
from scipy.stats import linregress
from time import time

def networks_newman_101(G):
    """
    Makes a row entry for the graph similar to the rows in table 10.1 of Networks 2nd Ed., by Newman.

    n: number of nodes
    m: number of edges
    c: mean degree
    S: fraction of nodes in the largest component 
    l: mean of all pairs shortest path lengths
    alpha: exponent of the degree distribution if power law (note: naive
      evaluation assuming the entire distribution, rather than possible piecewise
      as often observed in practice).
    C: clustering coefficient from Eq. (7.28) of source
    CWS: clustering coefficient from Eq. (7.31) of source
    r: degree correlation (Pearson's correlation coefficient for degree)
    """

    network_name = G.name
    t0 = time();
    n = G.number_of_nodes()
    print(f'nnodes = {n} calculated in {time() - t0:.3f}s'); t0 = time()
    m = G.number_of_edges()
    print(f'nnodes = {n} calculated in {time() - t0:.3f}s'); t0 = time()

    if type(G) == networkx.classes.graph.Graph: # there is also G.is_directed()
        c = n/(2*m) # eqn (6.15)
        ccs = networkx.connected_components(G)
    else:
        c = n/m
        ccs =  networkx.weakly_connected_components(G)
    
    S = len(max(ccs)) / n
    print(f'S = {S} calculated in {time() - t0:.3f}s'); t0 = time()
    # computing l
    # don't use average because unconnected will raise error (technically infinite path length)
    l = 0
    for _, adjl in nxa.shortest_paths.all_pairs_bellman_ford_path_length(G):
        l += sum(adjl.values())
    l /= n*(n+1) / 2
    print(f'l = {l} calculated in {time() - t0:.3f}s'); t0 = time()

    # computing alpha
    # note: estimating the power law coeficient by a logarithmic fit introduces bias
    # and there are formulas for the degree which introduce no bias
    sdeg = np.log(sorted(deg for _, deg in G.degree if deg > 0))
    # don't look at isolated nodes
    #
    # one can test for linearity in the logarithm by constant deltas between
    # adjacent elements and quantify the root variance relative to the mean.
    # linear regression is used because it returns standard statistics 
    sdeg, _, r, p, *_ = linregress(range(len(sdeg)), sdeg)
    if p > .05 or r < .75:
        sdeg = None # no power law observed
    print(f'sdeg = {sdeg} calculated in {time() - t0:.3f}s'); t0 = time()
        
    # computing C
    # the number of connected triples is simply the number of combinations of
    # neighbors for each node, considering it to be the 'center' of the
    # connected triple.
    try:
        ntriangles = nxa.cluster.triangles(G) 
        nconnected_triples = sum(binom(deg, 2) if deg > 1 else 0 for _, deg in G.degree)
        C = ntriangles * 3 / nconnected_triples
        print(f'C = {C} calculated in {time() - t0:.3f}s'); t0 = time()
    except networkx.exception.NetworkXNotImplemented:
        C = None
    try:
        CWS = nxa.average_clustering(G)
        print(f'CWS = {CWS} calculated in {time() - t0:.3f}s'); t0 = time()
    except networkx.exception.NetworkXNotImplemented:
        CWS = None
    r = nxa.assortativity.degree_pearson_correlation_coefficient(G)
    print(f'r = {r} calculated in {time() - t0:.3f}s'); t0 = time()

    return dict(Network=network_name, Type=G.__class__.__name__,
               n=n, m=m, c=c, # this is only for undirected, need boolean
               S=S, l=l, C=C,
               CWS=CWS, r=r)

def characterize_directed(G):
    """
    These are for properties only for directed graphs.
    """
    recip = nxa.reciprocity(G)
    recipstr = f'reciprocity = {recip:.2f} {"!= 0, not DAG" if recip > 0 else "= 0, is DAG"}'

    return '\n'.join((recipstr,))

def centralities_top3(G):
    # note for DAGs (like ideal citation graphs), eigenvector_centrality is zero. use PageRank, instead.

    top3s = dict()
    for alg in (nxa.centrality.degree_centrality,
                nxa.centrality.eigenvector_centrality, 
                nxa.centrality.closeness_centrality,
                nxa.centrality.betweenness_centrality):
        try:
            d = alg(G)
            skeys = sorted(d, key=lambda x: d[x])
            top3s[alg] = []
            for key in skeys[-3:][::-1]:
                top3s[alg].append((key, d[key]))
        except Exception:  # can be convergence exception
            test_logger.warning(f'data failed to converge for {alg}')
    return top3s


def degree_deciles(G):

    ind = np.array(tuple(x[1] for x in G.in_degree))
    outd = np.array(tuple(x[1] for x in G.out_degree))
    bl = ind > 0
    rat = outd[bl] / ind[bl]
    q = np.linspace(0, 1, 11)
    return np.quantile(ind, q), np.quantile(outd, q), np.quantile(rat, q)


def test_networks_101(G):
    test_logger.info(networks_newman_101(G))

def test_degree_deciles(G):
    ind, outd, rat = degree_deciles(G)
    test_logger.info('in-degree deciles ' + '-'.join(f'{x:.1f}' for x in ind))
    test_logger.info('out-degree deciles ' +
                     '-'.join(f'{x:.1f}' for x in outd))
    test_logger.info('out-degree/in-degree deciles ' +
                     '-'.join(f'{x:.1E}' for x in rat))

def test_centralities(G):
    top3s = centralities_top3(G)
    for k in top3s:
        test_logger.info(str(k))
        for pub, value in top3s[k]:
            test_logger.info(f'{pub.title} has centrality {value:.2f}')

def test_author_bipartition(G2):
    part1, part2 = nxa.community.kernighan_lin_bisection(G2.to_undirected())
    x1 = len(part1) / (len(part1) + len(part2))
    test_logger.info(f'community partition for author citations into fraction {x1*100:.0f}%')

def test_characterize_directed(G2):
    print(characterize_directed(G))

if __name__ == '__main__':
    from gssa.core import load_cached_publications_all_data
    publist = load_cached_publications_all_data()

    G = publist2digraph(publist)
    test_networks_101(G)
    test_degree_deciles(G)
    test_centralities(G)

    G2 = publist2authordigraph(publist)
    test_author_bipartition(G2)
    test_characterize_directed(G2)
