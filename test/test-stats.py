from serp.stats.tempmodule import load_data
from serp.stats.stats import citing_authors, value_counts, ncitations, groupby

publist = load_data()

tcites = citing_authors(publist)
d = value_counts(tcites)
print(sorted([(x, f'{d[x] / len(tcites):.2f}') for x in d], key=lambda x:x[1])[-10:])

tot = self = 0
for k in d:
    a1, a2 = k.split('-', maxsplit=1)
    if a1 == a2:
        self += d[k]
    tot += d[k]

print(f'fraction self-citations = {100*self / tot:.1f}%')

ncites = ncitations(publist)
d = groupby(ncites)
print(sorted([(x, sum(d[x])) for x in d], key=lambda x:x[1])[-10:])

from serp.stats.metrics import hindex, gindex, i10index, oindex, windex

for metric in hindex, gindex, i10index, oindex, windex:
    l = sorted([(k, metric(d[k])) for k in d], key = lambda x:x[1])
    print(metric, '\n', l[-10:])
