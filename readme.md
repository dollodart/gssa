# Quick Start

To find articles made by an author without a Google Scholar profile, 

1. Make `secretenv.py` in project directory with the following, substituting your parameters:
```
SERP_API_KEY = '1111111111111111111111111111111111111111111111111111111111111111'

author_first = 'albert'
author_last = 'einstein'
vancouver_author = 'Einstein A' # your author may have a middle initial
```

2. Make directory `serp_cache` under the project directory. Make subdirectories `search`, `cite`,
   `cited_by`, and `publication` in `serp_cache`. You can use different names if you change 
   `userenv.py`.

3. Go to `example` directory and execute `python author-search.py`. Make sure the project directory is in your PYTHONPATH.

This will cache all the results. You can then run any of the tests like
`test-stats.py` for statistics to be calculated from the cached data. The
log file will be continually updated and placed in the directory from which the
interpreter was called and can be monitored as queries are made.

Note that for Einstein, who has a Google Scholar profile, you could use instead the `gprofile` module. In that case

1. Copy the `tbody` part of the google scholar profile, containing all HTML
   table entries for articles, to your machine.

2. Make the directory `input` under the project directory. Make the cache
   directories like in step 2 of the above. You can use different names if you
   change `userenv.py`.

3. Move the HTML under the `input` directory. Here the file will be given the name `aeinstein.html`.

4. Make `secretenv.py` in project directory with the following, substituting your parameters:
```
SERP_API_KEY = '1111111111111111111111111111111111111111111111111111111111111111'
author_gprofile = 'aeinstein.html'
```

5. Go to `example` directory and execute `python gprofile-search.py`. Make sure the project directory is in your PYTHONPATH.

# Package Description

This package is designed around a Data Access Object for the Google Scholar
database queried through SerpAPI. Queries go through the public-facing Google
Scholar search and so are limited to word or term searches using the search bar
(advanced search would be possible, but isn't supported here). All filtering,
aggregating, and other transformations are done with the DAO or some other data
structures the DAO are converted to (see Package Structure section). The DAO is
the Publication class instance and its component class Citation and corresponds
to an 'organic result' found through:

1. Search using terms, including author names for those authors without GoogleScholar profiles.
2. Search using publication titles from GoogleScholar author pages for those authors who have GoogleScholar profiles.

After getting a set of articles from either a term search or a GoogleScholar
profile, the citing articles are found, and then second citing articles, and
potentially more. This recursive graph construction is possible because of
GoogleScholar's "cited by" links. From this analytics can be calculated, by
graph algorithms for structural information or by flattening into a tabular
format to do aggregate calculations on properties.

# Package Structure

SerpAPI is an API for scraping data from search engines like GoogleScholar.
It's existence may be more short-lived than GoogleScholar, or its interfaces
may change more frequently than GoogleScholar. As a result the Publication and
Citation classes (in `core`) are given constructor methods using the SerpAPI
json results, and get methods using the SerpAPI, which are separate from other
methods and properties. The class properties and methods rely on certain data
existing which is expected from GoogleScholar HTML results. 

Environment variables are configured in `secretenv` (not included) and
`userenv`, which are called as imports in `env` which supplies global variables
for all the modules in the package. These include variables for logging
including a nest level using an instance of `Indent`, controlling and
mitigating query failures using an instance of `Checker`, and checking for
cached results through `global_cache`. 

The DAO are not serialized but constructed on application start. Because there
are query costs they are preferentially constructed from data in a cache.
Every request made to SerpAPI is cached as plain text JSON to using subroutines in `cache`. 

The general API querying subroutine is `query` in the `query` module. It
equivalently enters a search term in the search bar and flattens pagination to
obtain all results (or a specified number of results).

The data application objects can be converted to different structures provided by
packages (see dependencies) for analytics, such as a graph representation or a
relational database representation, in `structio`.

To explore citation networks, graph search methods, simply depth-first or
breadth-first search to a certain degree of separation, are provided in
`graph_search`. 

Some subroutines for calculating statistics are in the `stats` module, as well
as the definition of some bibilometrics. But generally one should use the
functions or methods from data science libraries like numpy or pandas, and so
this module is limited.

# Dependencies

- BeautifulSoup4: HTML parsing
- numpy: general vectorized array routines
- pandas: for calcuating statistics and making a relational database schema from application objects
- networkx: for graph algorithms running on citation networks
- matplotlib: visualization

# Further Development

There are significant improvements to be made. I still choose to publish at
this stage, though, because there is no alternative (to my knowledge). I was
surprised to find no use of SerpAPI for Google Scholar beyond that from the
developers of SerpAPI (see https://github.com/topics/serp-api where a limited
number of projects are listed not by the developers of SerpAPI). Though changes
will be made that remove backwards compatibility for a prematurely published
project, that only applies to scripts made with the package. It doesn't remove
any compatibility with the SerpAPI results which are saved as received. And
what I found lacking when I first used SerpAPI was a way to explore citation
networks without wasting queries, which this accomplishes at version 1.

Given 1 cent per query, and 20 page results for a search, it costs 1.05 cents
to query a given publication (because each publication also requires a cite
query to ensure author and journal information is present, though these are
also usually given in search results). This means citation networks on
thousands of publications can be constructed for around 50 dollars given
SerpAPIs developer pricing.

There is a tutorial on scraping Google Scholar which use general proxy services
(https://dev.to/iankerins/build-your-own-google-scholar-api-with-python-scrapy-4p73).
Given that Google Scholar HTML is relatively simple to parse (see below), there
may be cost reasons to only use general proxy services, but I have no intent of
doing that.

There is no way get the data from GoogleScholar on how it determines search
relevance for a search term. In addition to cited by links, one can follow
"related articles" link, though at the time of writing (2021-11-30) SerpAPI
only provides the google link as `related_pages_link` and does not host the
data at the link on its own servers.  Similarly, SerpAPI does not provide a
(serpAPI) link to BiBTeX or other structured data from the Cite query. This
doesn't limit development since the query parameters could be parsed from the
google link and made into a query for SerpAPI, but it poses some barrier.

## TODOs

- Fix handling of dropped and partial queries: nominally the logic using
  `overwrite` and `nres` in the `query` subroutine does this but it is
  untested.
- Fix dummy data creation and caching duplication.
- Fix publication object duplication generally (even outside of dummy data).
- Add edge case handling for 0 or 1 returned results. Currently handled ad hoc using
  exceptions in different places.
- Implement a unit-testing framework and make an exhaustive test suite.
- Implement systematic exception handling with logging.
- Improve logging specificity and verbosity. Use propagation and
  handlers/filters for making main log file.

# Similar projects

Particular for bibliometrics there is already the Tethne package, which uses
the graph algorithms of NetworkX. The purpose of this project is mainly to
provide a DAO for efficiently (in terms of queries) getting the data from
GoogleScholar through SerpAPI and persisting it locally in a cache. Functions
for calculating statistics using optional dependencies of networkx and pandas
are limited to the tests.

# GoogleScholar HTML Structure

As GoogleScholar's UI has not appreciably changed over at least 5 years, some
discussion of it is warranted. This package uses SerpAPI's default HTML parsing
and queries for json but it would be straightforward to parse the relatively
simple document structure of Google Scholar.

Each paper result, regardless of where its found (author profile page,
search page, or cited by page) is simply structured in GoogleScholar,
as the below simplified HTML shows. The data contained in the result
is: a title, a link, the authors, the journal, and the publication
date. Only some of the data for each field is usually presented, and
the ordering and specificity can change, especially depending on the
publication type (book, journal article, patent, et cetera). 

The "Cite" link can be followed, where it will give citations following
several standard formats. However, those also are not always having the
same data, specificity of data, ordering, and formatting (e.g., choice
of delimiter), especially for different publication types.

In general, the links within the "Cite" link, in particular BiBTeX,
need to be followed to get structured data. Even then there may be
inconsistencies because author names are changed, either because of
surname changes upon marriage, or because the authors or the journals
reported different initialization (often omitting or including middle
names).

## GoogleScholar result HTML (simplified)

```
<div>
<h3>
  <span>
    <span> <!-- optional specification of media type (omitted if a journal article) -->
    [BOOK]
    </span>
  </span>
 <a href="external-link">
 text link
  </a>
</h3>
<div> <!-- publication metadata, field present, their specificity, and their order can vary -->
Author - Journal - Year - Publisher
</div>
<div>
Abstract text...
</div>
<div>
  <a> <!-- save button -->
    <svg> svg code for image </svg>
  </a>
  <a> <!-- cite button -->
    <svg> svg code for image </svg>
  </a>
  <a href="internal link">
  Cited by n
  </a>
  <a href="internal link">
  Related articles
  </a>
  <a href="internal link">
  All n versions
  </a>
  <a> <!-- "more" button, leads to, e.g., library search -->
    <svg> svg code for image </svg>
  </a>
  <a href="external link">
  Library Search
  </a>
  <a> <!-- less button, closes out -->
    <svg> svg code for image </svg>
  </a>
</div>
</div>
```

## Cite page HTML (simplified)

```
<div>
<table>
<tbody>
  <tr>
    <th scope="row">
    MLA
    </th>
    <td>
      <div>
       the mla citation
      </div>
    </td>
  </tr>
  <tr>
    <th scope="row">
    APA
    </th>
    <td>
      <div>
      the apa citation
      </div>
    </td>
  </tr>
  <!-- repeated for Chicago, Harvard, and Vancouver -->
</tbody>
</table>
</div>
<div>
  <a href="internal link (text)">
  BibTeX
  </a>
  <a href="internal link (download)">
  EndNote
  </a>
  <a href="internal link (download)">
  RefMan
  </a>
  <a href="internal link (download)">
  RefWorks
  </a>
</div>
```
