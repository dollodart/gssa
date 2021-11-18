from serp.stats.tempmodule import load_data 
import serp.stats.nxstats as nxs

publist = load_data()
G = nxs.construct_publication_graph(publist)

st1 = nxs.characterize(G)
G.remove_nodes_from([x[0] for x in G.out_degree if x[1] < 1])
st2 = nxs.characterize(G)
print(st1, st2)

ind, outd, rat = nxs.degree_deciles(G)
print('in-degree deciles', '-'.join(f'{x:.1f}' for x in ind))
print('out-degree deciles', '-'.join(f'{x:.1f}' for x in outd))
print('out-degree/in-degree deciles', '-'.join(f'{x:.1E}' for x in rat))

top3s = nxs.centralities_top3(G)
for k in top3s:
    print(str(k))
    for pub, value in top3s[k]:
        print(pub.title, 'has centrality', round(value, 2))
