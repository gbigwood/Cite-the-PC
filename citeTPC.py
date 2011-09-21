"""
A program to obtain a list of all the papers that you need to cite to get
accepted at your conference.

Takes a list of names from standard in, Returns html

Call like so:
< testinput python citeTPC.py
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
import urllib
import re
import cgi

#The hardcoded strings for google scholar tags
paperContainerString = "gs_r"
linkToPaperString = "gs_ggs"
citationString = "gs_ctu"

#Create opener with Google-friendly user agent
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

#Make a container type for the pc members
Paper = namedtuple('Paper', ['doi', 'hardlink','title'])

def readNames():
    """
    returns a list of members to search for from standard in
    """
    import sys
    #print [s.decode('latin-1') for s in sys.stdin.readlines()]
    #return [s.decode('latin-1') for s in sys.stdin.readlines()]
    return sys.stdin.readlines()

def createOutputPage(htmltags):
    """
    takes the strings of the TPC results and makes a web page
    """
    header = '<html><head><title>Papers to cite</title></head><body>'
    body= "\n".join(htmltags)
    #body = "\n".join(s.encode('latin-1') for s in htmltags )
    footer = '</body></html>'
    print header
    print body
    print footer
    pass

def formatMemberTextPrint(member):
    """does some regular expression stuff to clean up the member text for print"""
    #print member.encode('latin-1')
    #member = member.encode('latin-1')
    #member = re.sub('\t',' ',member)
    member = member.replace("\n","")
    member = member.replace(",","")
    member = member.replace("-","")
    member = member.replace("/"," ")
    #member = re.sub('[,-\n]+',' ',member)
    member = re.sub('[\s\t]+',' ',member)
    member = member.strip()
    member = cgi.escape(member)
    try:
        member = member.decode('utf8')#convert from utf8
    except:
        pass
    member = member.encode('ascii', 'xmlcharrefreplace')#convert to ascii
    return member

def formatMemberText(member):
    """does some regular expression stuff to clean up the member text"""
    member = member.replace(" ","+")
    return member

def searchForTPC(members,cmd=False):
    """takes a list of members, returns their papers
    
    cmd is whether or not we are calling from command line"""
    outputstrings = []
    for member in members:
        outputstrings.append('<div class="member">')
        member = formatMemberTextPrint(member)#for printing out
        #outputstrings.append('<div class="membername">%s</div>' 
        #%member.decode('latin-1'))
        outputstrings.append('<div class="membername">%s</div>' % member)
        member = formatMemberText(member)
        outputstrings.append('<ul>')
        for paper in findMembersPapers(member):
            try:
                outputstrings.append('<li>Paper:')
                outputstrings.append('<span class="paperdoi">%s</span>' % paper.doi)
                outputstrings.append('</li>')
                if paper.hardlink:
                    outputstrings.append('<li>Hardcopy:')
                    outputstrings.append('<span class="paperlink">%s</span>' % paper.hardlink)
                    outputstrings.append('</li>')
                outputstrings.append('<li>BibTeX:')
                outputstrings.append('<span class="bibtexlink"><a href="%s" title="BibTeX">%s</a></span>' % (getBibTex(paper.title[0],cmd), paper.title[0]) )
                outputstrings.append('</li>')
                outputstrings.append('</br>')
            except Exception as inst:
                print inst
                pass
        outputstrings.append('</ul>')
        outputstrings.append('</div>')#close the member div
    #print outputstrings
    return outputstrings

def findMembersPapers(memberString):
    """takes a member to search for, returns a list of html urls.
    
    the urls come as """
    url = "http://scholar.google.com/scholar?q="+memberString
    results = [] #the result papers go in here
    try:
        page = opener.open(url)
        soup = BeautifulSoup(page)
    except Exception as inst:
        print inst
    else:#if no error
        #print soup.prettify()
        #Parse and find the gs_r tags
        for cite in soup.findAll(name='div',attrs={"class" : paperContainerString}):
            if linkToPaperString in cite.span['class']: # contains a link to the hardcopy
                p = Paper(cite.div.a, cite.span.a,cite.div.a.contents)#we know there will be two links with data
            elif citationString in cite.span['class']: #its a citation not a paper
                #print "skipping",cite.div
                continue
            else:#no paper link
                p = Paper(cite.div.a,None,cite.div.a.contents)
            results.append(p)
    return results

def getBibTex(titleSearch, cmd):
    """tries to obtain the bibtex for the paper title passed in"""
    url = 'http://liinwww.ira.uka.de/csbib'
    cgilink = findBibTeXlink(titleSearch, url)
    url = 'http://liinwww.ira.uka.de'
    if cmd:#its command line, get the link to his
        return url+cgilink
    else:#it's web, find the url
        #get the bibtex
        #bibtex = findBibTeX(url+cgilink)
        #return a reference to the webserver so that we get the link to parse it ourselves
        #return "/bibTeX/"+cgilink.encode("hex")# uses the cherrypy webserver
        return url+cgilink

def findBibTeX(url):
    """makes the cgi request and gets the bibtex data"""
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent,
            'Referer' : 'http://liinwww.ira.uka.de/bibliography/index/html',
            }
    testsoup="""<html>
<head><title>Computer Science Bibliography Collection</title><link rel="stylesheet" href="/bibliography/bibliography.css" type="text/css" /></head>
<body>
<h1 class="page_title">The Collection of<br />Computer Science Bibliographies</h1><ul class="top_nav"><li><strong><a href="http://liinwww.ira.uka.de/bibliography/index.html" title="Home page of The Collection of Computer Science Bibliographies">Home</a></strong></li>
<li><a href="http://liinwww.ira.uka.de/bibliography/index.html#about" title="About the collection">About</a></li>
<li><a href="http://liinwww.ira.uka.de/bibliography/FAQ.html" title="Frequenly Asked Questions">FAQ</a></li>
<li><a href="http://liinwww.ira.uka.de/bibliography/index.html#browse" title="Browsing the collection by topics">Browse</a></li>
<li><a href="http://liinwww.ira.uka.de/bibliography/Contributing.html" title="Contributing new bibliographies to the collection">Add</a></li>
<li><a href="http://liinwww.ira.uka.de/bibliography/Statistics.html" title="Current coverage statistics">Statistics</a></li>
</ul>
<p class="biblink_bar">From <a href="http://liinwww.ira.uka.de/bibliography/Misc/DBLP/index.html" title="See the source subcollection of this record and limit your search to DBLP">DBLP (2011)</a>:</p>
<pre class="bibtex">@InProceedings{conf/wowmom/BigwoodH11,
  title =	"<span class="b_title">Bootstrapping opportunistic networks using social
		 roles</span>",
  author =	"<a href="/csbib?query=%2Bau:BigwoodG*+%2Bau:Bigwood&amp;maxnum=200&amp;sort=year" title="Search for publications authored by Greg Bigwood">Greg Bigwood</a> and <a href="/csbib?query=%2Bau:HendersonT*+%2Bau:Henderson&amp;maxnum=200&amp;sort=year" title="Search for publications authored by Tristan Henderson">Tristan Henderson</a>",
  publisher =	"IEEE",
  year = 	"2011",
  bibdate =	"2011-09-01",
  bibsource =	"DBLP,
		 <a href="http://dblp.uni-trier.de/db/conf/wowmom/wowmom2011.html#BigwoodH11">http://dblp.uni-trier.de/db/conf/wowmom/wowmom2011.html#BigwoodH11</a>",
  booktitle =	"WOWMOM",
  crossref =	"conf/wowmom/2011",
  ISBN = 	"<a href="http://www.ubka.uni-karlsruhe.de/kvk.html?kataloge=alle&amp;autosubmit=true&amp;SB=978-1-4577-0352-2" title="Try searching KVK for the ISBN:978-1-4577-0352-2">978-1-4577-0352-2</a>",
  pages =	"1--6",
  URL =  	"<a href="http://ieeexplore.ieee.org/xpl/mostRecentIssue.jsp?punumber=5976314">http://ieeexplore.ieee.org/xpl/mostRecentIssue.jsp?punumber=5976314</a>",
}
</pre><p class="biblinks"><br /><br /><a href="http://ieeexplore.ieee.org/xpl/mostRecentIssue.jsp?punumber=5976314" title="Full text of the document">Unknown&nbsp;Format</a><br /><a href="http://ieeexplore.ieee.org/search/searchresult.jsp?queryText=bootstrapping+opportunistic+networks+using+social+roles+%3Cin%3E+ti&amp;coll1=ieeejrns&amp;coll2=ieejrns&amp;coll3=ieeecnfs&amp;coll4=ieecnfs&amp;coll5=ieeestds&amp;coll6=preprint&amp;py1=1950&amp;py2=2013&amp;SortField=Score&amp;SortOrder=desc&amp;ResultCount=15" title="Try searching IEEExplore for this document">Try IEEExplore</a></p><p class="footer">
<a href="http://liinwww.ira.uka.de/bibliography/Copyright.html">Copyright</a> &copy; 1995-2011 Alf-Christian Achilles, All rights reserved.
<br />
This service is brought to you by Alf-Christian Achilles 
and <a href="http://3miasto.net.pl/~ortylp">Paul Ortyl</a>
<br />
Please direct <a href="/bibliography/Comments.html" title="Send your comments via form.">comments</a> 
to <kbd><a href="mailto:liinwwwa@ira.uka.de">liinwwwa@ira.uka.de</a></kbd>
</p>
</body></html>
"""    
    result = ""
    try:
        page = opener.open(url)
        soup = BeautifulSoup(page)
    except Exception as inst:
        print inst
    try:
        bibtex = soup.find(name='pre', attrs={"class" : "bibtex"})
        result = bibtex.contents
    except:
        print "fail to find bibtex reference"
        print soup

    return result


def findBibTeXlink(titleSearch, url):
    """find the link to use for getting the bibtex link"""
    values = {'query': titleSearch,
          'field' : 'ti',# find the title
          'year' : '',
          'since':'',
          'before': '',
          'results': 'citation',
          'maxnum': '40',
          'sort': 'score',
          'online': 'on',
          }
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent,
            'Referer' : 'http://liinwww.ira.uka.de/bibliography/index/html',
            }
    try:
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)
        the_page = response.read()
        soup = BeautifulSoup(the_page)
    except Exception as inst:
        print inst
        print "failed to find bibtex"
        return
    try:
        biblink = soup.find(name='a', attrs={"title" : "Full BibTeX record"})
    except:
        print "fail to find bibtex soup"
    return urllib.unquote(biblink['href'])
    
if __name__ == "__main__":
    listofnames = readNames()
    createOutputPage(searchForTPC(listofnames,cmd=True))

