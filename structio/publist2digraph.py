import networkx as nx


def publist2digraph(publist):
    G = nx.DiGraph()
    G.add_nodes_from(publist)
    edges = []
    for pub in publist:
        for pub2 in pub.get_cited_by():
            edges.append([pub, pub2])

    G.add_edges_from(edges)

    return G
