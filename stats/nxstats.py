import matplotlib.pyplot as plt
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

def visualize(G):
    nx.draw(G)
    plt.show()

def plot_degree_hists(G):

    outd = list(G.out_degree)
    ind = list(G.in_degree)
    rat = [outd[c][1] / ind[c][1] for c in range(len(ind)) if ind[c][1] > 0]

    plt.figure()
    plt.xlabel('out-degree')
    plt.hist([x[1] for x in outd])
    plt.figure()
    plt.xlabel('in-degree')
    plt.hist([x[1] for x in ind])
    plt.figure()
    plt.xlabel('ratio out-degree / in-degree')
    plt.hist(rat)
    plt.show()

def centralities_top3(G):

    top3 = []
    for alg in (nx.algorithms.centrality.degree_centrality,
            nx.algorithms.centrality.eigenvector_centrality,
            nx.algorithms.centrality.closeness_centrality,
            nx.algorithms.centrality.betweenness_centrality):
        d = alg(G)
        skeys = sorted(d, key=lambda x:d[x])
        top3.append(str(alg))
        for key in skeys[-3:]:
            top3.append(f'{key.title}\t{d[key]:.3f}')
        top3.append('\n')
    return '\n'.join(top3)

if __name__ == '__main__':
    from tempmodule import load_data 
    publist = load_data()
    G = construct_publication_graph(publist)

    st1 = characterize(G)
    G.remove_nodes_from([x[0] for x in G.out_degree if x[1] < 1])
    st2 = characterize(G)
    print(st1, st2)

    #print(centralities_top3(G))
