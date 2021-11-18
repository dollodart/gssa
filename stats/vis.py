import matplotlib.pyplot as plt

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
