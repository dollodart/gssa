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


def citee_ncitations(publist, author_index=0):
    tcites = []
    for pub in publist:
        cbc = pub.cited_by_count
        # if cbc != len(pub.get_cited_by()):
        #    pass # can do something in case disagreement
        fa = pub.get_cite().authors
        if fa is None or len(fa) == 0:
            continue
        tcites.append((fa[author_index], cbc))
    return groupby(tcites)


def value_counts(lst):
    d = dict()
    for k in lst:
        try:
            d[k] += 1
        except KeyError:
            d[k] = 1
    return d


def citer_citee_pairs(publist, author_index=-1):
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

        tcites.extend([fa[author_index] + '-' + x[author_index]
                       for x in flist])
    return value_counts(tcites)
