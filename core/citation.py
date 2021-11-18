import re
from datetime import datetime

def mla_parse_article_name(mla_string):
    st = ''
    start = False
    for char in mla_string:
        if start:
            st += char
        if char == '"':
            start *= -1
    return st[:-1]


def vancouver_date_process(date):
    date = date.strip()
    nfields = len(date.split(' '))
    if nfields == 1:
        date = datetime.strptime(date, '%Y')
    elif nfields == 2:
        date = datetime.strptime(date, '%Y %b')
    elif nfields == 3:
        date = datetime.strptime(date, '%Y %b %d')
    return date


def vancouver_parse(vancouver_string, mla_string):
    """

    The Vancouver citation format is the most consistent. It
    doesn't escape the article name, however, so use MLA to get
    that. Unfortunately the journal name used between MLA and Vancouver
    can differ, as well.

    """

    if mla_string is not None and len(vancouver_string.split(
            '.')) > 3:  # there is, monimally, a journal
        article_name = mla_parse_article_name(mla_string)
        vancouver_string = vancouver_string.replace(
            article_name, article_name.replace('.', '//'))
        nominal_journal = vancouver_string.split('.')[2].strip()
        nominal_journal_2 = mla_string.split('"')[-1].strip()

        sctr = 0
        i = nominal_journal[sctr]
        j = nominal_journal_2[sctr]
        maxsctr = min(len(nominal_journal), len(nominal_journal_2))

        while i == j and sctr < maxsctr:
            i = nominal_journal[sctr]
            j = nominal_journal_2[sctr]
            sctr += 1

        journal_name = nominal_journal[:sctr + 1]
        vancouver_string = vancouver_string.replace(
            journal_name, journal_name.replace('.', '//'))

    vancouver_string2 = ''
    paranthesized = False
    for char in vancouver_string:
        if char == '(':
            paranthesized = True
        if paranthesized and char == '.':
            char = '//'
        if char == ')':
            paranthesized = False
        vancouver_string2 += char

    vancouver_string = vancouver_string2

    # last should be an empty string, ending period is not a delimiter
    vancouver = vancouver_string.split('.')[:-1]

    if len(vancouver) > 4:  # there were periods in, e.g., the journal name
        raise Exception("more than four fields")

    length = len(vancouver)

    authors = vancouver[0].split(', ')
    title = vancouver[1].strip()
    if length == 2:  # at minimum, author and title
        return authors, title, None, None, None, None, None, None
    journal = vancouver[2].strip()
    if length == 3:  # author, title, journal
        return authors, title, journal, None, None, None, None, None
    journal_info = vancouver[3]
    try:
        date, volissuepage = journal_info.split(';')
        date = vancouver_date_process(date)
    except ValueError:  # too many to unpack
        try:
            date = vancouver_date_process(journal_info)
            return authors, title, journal, date, None, None, None, None
        except ValueError:
            return authors, title, journal, None, None, None, None, None
    try:
        volissue, page = volissuepage.split(':')
    except ValueError:
        return authors, title, journal, date, volissuepage, None, None, None
    volissue = volissue.split('(')
    if len(volissue) > 1:
        vol, issue = volissue
        vol = int(vol)
        issue = issue.rstrip(')')
        if not '-' in issue:
            issue = int(issue)
    else:
        vol = int(volissue[0])
        issue = None

    pages = page.split('-')
    if len(pages) > 1:
        pagelower, pageupper = page.split('-')
        try:
            pagelower = int(pagelower)
            pageupper = int(pageupper)
            if pageupper < pagelower:
                pageupper = pagelower + pageupper
        except ValueError:
            return authors, title, journal, date, vol, issue, None, None
    else:
        pageupper = None
        if re.match('[a-z]', page.lower()) is not None:
            pagelower = pages[0]
        else:
            pagelower = int(pages[0])

    return authors, title, journal, date, vol, issue, pagelower, pageupper

class Citation:
    def __init__(self,
                 mla,
                 apa,
                 bibtex,
                 endnote,
                 refman,
                 refworks,
                 chicago=None,
                 harvard=None,
                 vancouver=None,
                 iso690=None):
        self.mla = mla
        self.apa = apa
        self.chicago = chicago
        self.harvard = harvard
        self.vancouver = vancouver
        self.bibtex = bibtex
        self.endnote = endnote
        self.refman = refman
        self.refworks = refworks

        # there is some data which can be consistently obtained from these citations
        # but other data cannot be
        try:
            struct_data = vancouver_parse(self.vancouver, self.mla)
            self.authors = struct_data[0]
            self.title = struct_data[1]
            self.journal = struct_data[2]
            self.date = struct_data[3]
            self.vol = struct_data[4]
            self.issue = struct_data[5]
            self.pagelower = struct_data[6]
            self.pageupper = struct_data[7]
            
        except Exception:
            self.authors = self.title = self.journal = self.date = self.vol = self.issue = self.pagelower = self.pageupper = None

    def get_pages(self):
        if self.pageupper is None:
            return self.pagelower
        else:
            return self.pageupper

    @classmethod
    def from_json(cls, json):
        d = dict()

        for adct in json['citations']:
            d[adct['title'].lower().replace(' ','')] = adct['snippet']

        for ldct in json['links']:
            # eventually, follow some of these links
            # but there is no, at the time of writing, SERP API link (direct link would require self-proxying)
            d[ldct['name'].lower()] = ldct['link']

        if 'refwork' in d.keys(): # hack for bad data
            d['refworks'] = d['refwork']
            del d['refwork'] 

        return cls(**d)
