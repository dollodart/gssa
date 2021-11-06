import core

def depth_first_search(pub, levels=1, filters=tuple()):
    if levels == 0:
        return

    for f in filters:
        if not f(pub):
            return

    core.global_indent += 2
    pub.get_cite()
    for x in pub.get_cited_by():
        depth_first_search(x, levels-1)

    core.global_indent -= 2

def breadth_first_search(publist, levels=1, filters=tuple()):

    if levels == 0:
        # core.global_indent -= core.global_indent # return to 0
        # can't tell if end of the breadth, though
        return 

    if type(publist) not in [list, tuple]:
        publist = [publist]

    core.global_indent += 2

    next_breadth = []
    for pub in publist:
        for f in filters:
            if not f(pub):
                continue
        pub.get_cite()
        next_breadth.extend(pub.get_cited_by())

    breadth_first_search(next_breadth, levels-1, filters)
