import numpy as np
import networkx as nx

def construct_publication_graph(publist):
    G = nx.DiGraph()
    G.add_nodes_from(publist)
    edges = []
    for pub in publist:
        for pub2 in pub.get_cited_by():
            edges.append([pub, pub2])

    G.add_edges_from(edges)

    return G

def characterize(G):
    recip = nx.algorithms.reciprocity(G)
    windex = nx.algorithms.wiener_index(G)
    # fh = nx.algorithms.flow_hierarchy(G) # flow_hierarchy = 1 - reciprocity? 
    acluster = nx.algorithms.average_clustering(G)
    return (f'reciprocity = {recip:.2f}, Wiener index = {windex:.2f}\n' + 
            f'average clustering = {acluster:.2f}')

def centralities_top3(G):

    top3s = dict() 
    for alg in (nx.algorithms.centrality.degree_centrality,
            nx.algorithms.centrality.eigenvector_centrality,
            nx.algorithms.centrality.closeness_centrality,
            nx.algorithms.centrality.betweenness_centrality):
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
