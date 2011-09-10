"""
A program to obtain a list of all the papers that you need to cite to get
accepted at your conference.
 __
/  \        _____________
|  |       /             \
@  @       | It looks    |
|| ||      | like you    |
|| ||   <--| are writing |
|\_/|      | a paper.    |
\___/      \_____________/
"""
from BeautifulSoup import BeautifulSoup
from collections import namedtuple
import urllib2
#The hardcoded strings for tags
paperContainerString = "gs_r"
linkToPaperString = "gs_ggs"
citationString = "gs_ctu"
#Create opener with Google-friendly user agent
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

#Make a container type for the pc members
Paper = namedtuple('Paper', ['doi', 'hardlink'])

#Who we are searching for
listofnames = [
    #"Kevin Almeroth University of California",
    #"Sun-Ki Chai University of Hawaii",
    #"Adrian David Cheok National University of Singapore",
    #"Noshir Contractor Northwestern University",
    #"Irfan Essa Georgia Institute of Technology",
    #"David Lazer Northeastern/Harvard University",
    "Dongman Lee KAIST",
    "Ramesh Jain University of California",
    #"Tom Malone Massachusetts Institute of Technology",
    #"Kenji Mase Nagoya University",
]

def searchForTPC(members):
    """takes a list of members, returns their papers"""
    for member in members:
        print "Member:",member
        member = member.replace(" ","+")
        for paper in findMembersPapers(member):
            try:
                print paper.doi
                print paper.hardlink
                print "-"
            except:
                print "no links"
        print "---"
        print "---"

def findMembersPapers(memberString):
    """takes a member to search for, returns a list of html urls.
    
    the urls come as """
    url = "http://scholar.google.com/scholar?q="+memberString
    page = opener.open(url)
    soup = BeautifulSoup(page)
    results = [] #the result papers go in here
    #print soup.prettify()
    #Parse and find the gs_r tags
    for cite in soup.findAll(name='div',attrs={"class" : paperContainerString}):
        #pass
        if linkToPaperString in cite.span['class']: # contains a link to the hardcopy
            p = Paper(cite.div.a, cite.span.a)#we know there will be two links with data
        elif citationString in cite.span['class']: #its a citation not a paper
            #print "skipping",cite.div
            continue
        else:#no paper link
            p = Paper(cite.div.a,None)
        results.append(p)
    return results

searchForTPC(listofnames)
