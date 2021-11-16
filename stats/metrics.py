from datetime import datetime
from numpy import log, sqrt, array

# graph-based metrics
# author level eigenfactor
# see doi:10.1002/asi.22790

# hindex refinement
# see doi:10.1002/asi.22790

# c-index
# based on nearest neighbors


def hindex(citations):
    citations = sorted(citations)[::-1]
    for i in range(len(citations)):
        if citations[i] < i + 1:
            break
    return i


def gindex(citations):
    citations = sorted(citations)[::-1]
    sum_cites = 0
    for i in range(len(citations)):
        sum_cites += citations[i]
        if sum_cites < (i + 1)**2:
            break
    return i


def i10index(citations):
    return sum(array(citations) >= 10)


def mindex(citations, first_year):
    return hindex(citations) / (datetime.now().year - first_year)


def oindex(citations):
    return sqrt(max(citations) * hindex(citations))


def Lindex(citations, nauthors, years):
    years = datetime.now().year - array(years) + 1
    # to ensure no division by zero for current year articles add 1
    num = array(citations)
    den = array(nauthors) * years
    return 1 + log(sum(num / den))


def windex(citations):
    citations = array(citations)
    # is there a way to calculate this other than blind search?
    for w in range(1, 20):
        w *= 10
        bl = citations > w
        num = bl.sum()
        cond1 = num * 10 >= w
        cond2 = (citations[~bl] < w + 10).all()
        if cond1 and cond2:
            return w // 10
    return 0
