"""
A program to obtain a list of all the papers that you need to cite to get
accepted at your conference.

Returns html 
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

#The hardcoded strings for google scholar tags
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

def createOutputPage(htmltags):
    """
    takes the strings of the TPC results and makes a web page
    """
    header = '<html><head><title>Papers to cite</title></head><body>'
    body= "\n".join(htmltags)
    footer = '</body></html>'
    print header
    print body
    print footer
    pass

def searchForTPC(members):
    """takes a list of members, returns their papers"""
    outputstrings = []
    for member in members:
        outputstrings.append('<p>')
        outputstrings.append('<div class="member">')
        outputstrings.append( '<div class="membername">%s</div>' % member)
        member = member.replace(" ","+")
        for paper in findMembersPapers(member):
            try:
                outputstrings.append('<div class="paperdoi">%s</div>' % paper.doi)
                if paper.hardlink:
                    outputstrings.append('<div class="paperlink">%s</div>' % paper.hardlink)
                outputstrings.append('</br>')
            except:
                pass
        outputstrings.append('</p>')
        outputstrings.append('</div>')#close the member div
    return outputstrings

def findMembersPapers(memberString):
    """takes a member to search for, returns a list of html urls.
    
    the urls come as """
    url = "http://scholar.google.com/scholar?q="+memberString
    results = [] #the result papers go in here
    try:
        page = opener.open(url)
        soup = BeautifulSoup(page)
    except:#error
        print "error with the search"
    else:#if no error
        #print soup.prettify()
        #Parse and find the gs_r tags
        for cite in soup.findAll(name='div',attrs={"class" : paperContainerString}):
            if linkToPaperString in cite.span['class']: # contains a link to the hardcopy
                p = Paper(cite.div.a, cite.span.a)#we know there will be two links with data
            elif citationString in cite.span['class']: #its a citation not a paper
                #print "skipping",cite.div
                continue
            else:#no paper link
                p = Paper(cite.div.a,None)
            results.append(p)
    return results

createOutputPage(searchForTPC(listofnames))
