import pandas as pd

def publist2df(publist):
    pub_records = []
    auth_records = []
    citedby_records = []
    for pub in publist:
        primary_key = hash(pub.title)
        fields1 = 'title', 'abstract', 'publication_summary'
        precord = [primary_key]
        for f in fields1:
            precord.append(getattr(pub, f))
        cite = pub.get_cite()
        fields2 = 'journal', 'date', 'vol', 'issue', 'pagelower', 'pageupper'
        for f in fields2:
            precord.append(getattr(cite, f))

        pub_records.append(precord) 

        if cite.authors is not None:
            for auth in cite.authors:
                auth_records.append([primary_key, auth])

        for pub2 in pub.get_cited_by():
            secondary_key = hash(pub2.title)
            citedby_records.append([primary_key, secondary_key])

    pub_df = pd.DataFrame(pub_records, columns = ('primary_key',) + fields1 + fields2)
    pub_df = pub_df.set_index('primary_key')
    auth_df = pd.DataFrame(auth_records, columns = ['primary_key', 'author'])
    auth_df = auth_df.set_index('primary_key')
    citedby_df = pd.DataFrame(citedby_records, columns=['primary_key', 'secondary_key'])
    citedby_df = citedby_df.set_index('primary_key')
    return pub_df, auth_df, citedby_df

if __name__ == '__main__':
    from tempmodule import load_data
    publist = load_data()
    pubdf, authdf, citedby_df = publist2df(publist)
