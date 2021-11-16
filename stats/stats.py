from tempmodule import load_data
publist = load_data()

def ncitations(publist):
    tcites = []
    for pub in publist:
        cbc = pub.cited_by_count
        if cbc != len(pub.get_cited_by()):
            pass # can do something in case disagreement
        fa = pub.get_cite().authors
        if fa is None or len(fa) == 0:
            continue
        tcites.append((fa[0], cbc))
    return tcites

def groupby(lst_doubles):
    d = dict()
    for k, v in lst_doubles:
        if v is None:
            continue
        try:
            d[k].append(v)
        except KeyError:
            d[k] = [v]
    return d

def citing_authors(publist, author_index=0):
    # list of citer-citee for use in series
    tcites = []
    for pub in publist:
        fa = pub.get_cite().authors 
        if fa is None or len(fa) == 0:
            continue
        flist = []
        for p2 in pub.get_cited_by():
            fa2 = p2.get_cite().authors
            if fa2 is None or len(fa) == 0:
                continue
            flist.append(fa2)

        tcites.extend([fa[-1] + '-' + x[-1] for x in flist])
    return tcites

def value_counts(lst):
    d = dict()
    for k in lst:
        try:
            d[k] += 1
        except KeyError:
            d[k] = 1
    return d

if __name__ == '__main__':
    tcites = citing_authors(publist)
    d = value_counts(tcites)
    print(sorted([(x, f'{d[x] / len(tcites):.2f}') for x in d], key=lambda x:x[1]))

    ncites = ncitations(publist)
    d = groupby(ncites)
    print(sorted([(x, sum(d[x])) for x in d], key=lambda x:x[1]))

    from metrics import hindex, gindex, i10index, oindex, windex
    for metric in hindex, gindex, i10index, oindex, windex:
        l = sorted([(k, metric(d[k])) for k in d], key = lambda x:x[1])
        print(metric, '\n', l[-10:])
