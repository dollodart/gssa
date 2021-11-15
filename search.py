import serp.core
import serp.env

def depth_first_search(pub, levels=1, filters=tuple(), black=[]):
    if levels == 0:
        return

    for f in filters:
        if not f(pub):
            return

    if pub in black:
        return
    else:
        black.append(pub)

    serp.env.global_indent += 2
    pub.get_cite()
    for x in pub.get_cited_by():
        depth_first_search(x, levels-1, filters, black)

    serp.env.global_indent -= 2

def breadth_first_search(publist, levels=1, filters=tuple(), black=[]):

    if levels == 0:
        # core.global_indent -= core.global_indent # return to 0
        # can't tell if end of the breadth, though
        return 

    if type(publist) not in [list, tuple]:
        publist = [publist]

    serp.env.global_indent += 2

    next_breadth = []
    for pub in publist:
        for f in filters:
            if not f(pub):
                continue
        if pub in black:
            continue
        else:
            black.append(pub)
        pub.get_cite()
        next_breadth.extend(pub.get_cited_by())

    breadth_first_search(next_breadth, levels-1, filters, black)
