import matplotlib.pyplot as plt
import networkx as nx
from serp.structio import publist2digraph

def visualize(G):
    nx.draw(G)
    plt.show()

def plot_degree_dists(G):

    outd = list(G.out_degree)
    ind = list(G.in_degree)
    rat = [outd[c][1] / ind[c][1] for c in range(len(ind)) if ind[c][1] > 0]

    plt.figure()
    y = [x[1] for x in outd if x[1] > 0]
    plt.semilogy(range(len(y)), sorted(y))
    plt.xlabel(f'number ({len(outd) - len(y)} were 0)')
    plt.ylabel('out-degree')

    plt.figure()
    y = [x[1] for x in ind if x[1] > 1]
    n0 = len([x[1] for x in ind if x[1] == 0])
    plt.semilogy(range(len(y)), sorted(y))
    plt.xlabel(f'number ({len(ind) - len(y) + n0} were 1)')
    plt.ylabel('in-degree')

    plt.figure()
    y = [x for x in rat if x > 0]
    plt.semilogy(range(len(y)), sorted(y))
    plt.xlabel(f'number (note {len(rat) - len(y)} were 0 '
            +  f'and {len(ind) - len(rat)} were inf')
    plt.ylabel('ratio out-degree / in-degree')
    plt.show()

if __name__ == '__main__':
    from serp.core import load_cached_publications_all_data
    publist = load_cached_publications_all_data()
    G = publist2digraph(publist)

    #visualize(G)
    plot_degree_dists(G)
