import pandas as pd
from datetime import datetime

def mydatetime(obj):
    if type(obj) is datetime:
        return obj
    raise Exception

pr_dtype = {'primary_key':int,
            'title': str,
            'abstract': str,
            'publication_summary': str,
            'cited_by_count': float,
            'journal': str,
            'date': 'datetime64[ns]', # is datetime when parsed
            'vol': float,
            'issue': float,
            'pagelower': float,
            'pageupper': float}

pr_typecaster = pr_dtype.copy()
pr_typecaster['date'] = mydatetime

def publist2df(publist):
    pub_records = []
    auth_records = []
    citedby_records = []
    for pub in publist:
        primary_key = hash(pub.title)
        fields1 = 'title', 'abstract', 'publication_summary', 'cited_by_count'
        precord = [primary_key]
        for f in fields1:
            try:
                typecaster = pr_typecaster[f]
                precord.append(typecaster(getattr(pub, f)))
            except Exception:
                precord.append(None)

        cite = pub.get_cite()
        fields2 = 'journal', 'date', 'vol', 'issue', 'pagelower', 'pageupper'
        for f in fields2:
            try:
                typecaster = pr_typecaster[f]
                precord.append(typecaster(getattr(cite, f)))
            except Exception:
                precord.append(None)

        pub_records.append(precord) 

        if cite.authors is not None:
            for auth in cite.authors:
                auth_records.append([primary_key, auth])

        for pub2 in pub.get_cited_by():
            secondary_key = hash(pub2.title)
            citedby_records.append([primary_key, secondary_key])

    pub_cols = tuple(zip(*pub_records))
    cols = ('primary_key',) + fields1 + fields2
    series = dict()
    for c in range(len(cols)):
        ser = pd.Series(pub_cols[c], name=cols[c], dtype=pr_dtype[cols[c]])
        series[cols[c]] = ser

    pub_df = pd.DataFrame(series)
    auth_df = pd.DataFrame(auth_records, columns = ['primary_key', 'author'])
    citedby_df = pd.DataFrame(citedby_records, columns=['primary_key', 'secondary_key'])
    return pub_df, auth_df, citedby_df

def publist2db(publist, sqlconnection):
    # TO DO
    # use pandas.DataFrame.tosql method, with append option, to update tables in a relational database
    # requires sqlalchemy
    pass
