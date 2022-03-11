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

def publist2authordigraph(publist):
    """
    Unweighted.
    """
    G = nx.DiGraph()

    for pub in publist:
        cite = pub.get_cite()
        citee = cite.authors

        for pub2 in pub.get_cited_by():
            cite = pub2.get_cite()
            citor = cite.authors 
            try:
                for a1 in citee:
                    for a2 in citor:
                        G.add_edge(a2, a1)
            except Exception:
                pass
    return G
