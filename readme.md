# Scope

This is a wrapper for the python SerpAPI for GoogleScholar to obtain publication and citation data through:

1. Search using terms, including author names for those authors without GoogleScholar profiles.
2. Search using publication titles from GoogleScholar author pages for those authors who have GoogleScholar profiles.

After getting a set of articles from either a term search or a GoogleScholar
profile, the citing articles are found, and then second citing articles, and
potentially more. This recursive graph construction is possible because of
GoogleScholar's "cited by" links. From this graph structure analytics can be
calculated, by graph algorithms for structural information or by flattening
into a tabular format to do aggregate calculations on properties.

There is no way get the data from GoogleScholar on how it determines search
relevance for a search term. However, in addition to following cited by links,
the "relevant articles" link can be descended into, though at the time of
writing (2021-02-09) SerpAPI only provides the link and does not host the data
at the link.

# Package Structure

SerpAPI is an API for extracting data from search engines like GoogleScholar.
It's existence may be more short-lived than GoogleScholar, or its interfaces
may change more frequently than GoogleScholar. As a result the classes (in
`core`) are given constructor methods using the SerpAPI json results, and get
methods using the SerpAPI, which are separate from other methods and
properties. The class properties and methods rely on certain data existing
which is expected from GoogleScholar html results. 

The application objects are never serialized, instead being constructed from a
cache provided the corresponding json query exists. Every request which can be
made to SerpAPI is able to be cached to minimize the number of redundant
queries. The caching and general API querying logic is in the `query` module.
The SerpAPI results are saved as plain text JSON. 

The application objects can be converted to different structures provided by
packages (see dependencies) for analytics, such as a graph representation or a
relational database representation (in `structio`).

To explore citation networks, graph search methods, simply depth-first or
breadth-first search to a certain degree of separation, are provided in
`graph_search`.

## GoogleScholar Result Structure

As GoogleScholar's UI has not appreciably changed over at least 5 years,
some discussion of it is warranted.

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

### GoogleScholar result HTML (simplified)

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

### Cite page HTML (simplified)

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

# Dependencies

- pandas: for cacluating statistics and making a relational database schema from application objects
- networkx: for graph algorithms running on citation networks
- matplotlib: visualization

# Similar projects

In fact particular for bibliometrics there is already the Tethne package, which
uses the graph algorithms of NetworkX. The purpose of this project is only to
provide a way of efficiently obtaining the data through GoogleScholar, though
it provides some functions for calculating statistics using optional
dependencies of networkx and pandas.

# References

Gálvez, R.H. Assessing author self-citation as a mechanism of
relevant knowledge diffusion. Scientometrics 111, 1801–1812 (2017).
https://doi.org/10.1007/s11192-017-2330-1
