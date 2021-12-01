from gssa.env import global_indent, test_logger
from gssa.core import load_cached_publications_all_data
from gssa.stats.stats import value_counts

publist = load_cached_publications_all_data()

for pub in publist:
    cited_by = pub.get_cited_by()
    for pub2 in cited_by:
        test_logger.info(
            global_indent + f'found {pub2.title} as citing article of {pub.title}')
    delta = len(cited_by) - len(set(cited_by))
    if delta != 0:
        # , '\n', '-'.join(pub.title for pub in cited_by), '\n\n')
        print(pub.title)
        print([f'{pub.title} {count}' for pub,
               count in value_counts(cited_by).items() if count > 1])
    #assert len(cited_by) == len(set(cited_by))
