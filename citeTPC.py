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
Paper = namedtuple('Paper', ['doi', 'hardlink'])

def readNames():
    """
    returns a list of members to search for from standard in
    """
    import sys
    #print [s.decode('latin-1') for s in sys.stdin.readlines()]
    return [s.decode('latin-1') for s in sys.stdin.readlines()]
    #return sys.stdin.readlines()

def createOutputPage(htmltags):
    """
    takes the strings of the TPC results and makes a web page
    """
    header = '<html><head><title>Papers to cite</title></head><body>'
    body= "\n".join(htmltags)
    #body = "\n".join(s.decode('latin-1') for s in htmltags )
    footer = '</body></html>'
    print header
    print body
    print footer
    pass

def formatMemberText(member):
    """does some regular expression stuff to clean up the member text"""
    #print member.encode('latin-1')
    member = member.encode('latin-1')
    #member = re.sub('\t',' ',member)
    member = member.replace("\n","")
    member = re.sub('[\s\t]+',' ',member)
    print member
    member = member.replace(" ","+")
    member = member.replace(",","")
    member = member.replace("/","")
    member = cgi.escape(member)
    print member
    return member

def searchForTPC(members):
    """takes a list of members, returns their papers"""
    outputstrings = []
    for member in members:
        outputstrings.append('<div class="member">')
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
                outputstrings.append('</br>')
            except:
                pass
        outputstrings.append('</ul>')
        outputstrings.append('</div>')#close the member div
    #print outputstrings
    return outputstrings

def findMembersPapers(memberString):
    """takes a member to search for, returns a list of html urls.
    
    the urls come as """
    url = "http://scholar.google.com/scholar?q="+memberString
    print url
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
                p = Paper(cite.div.a, cite.span.a)#we know there will be two links with data
            elif citationString in cite.span['class']: #its a citation not a paper
                #print "skipping",cite.div
                continue
            else:#no paper link
                p = Paper(cite.div.a,None)
            results.append(p)
    return results

if __name__ == "__main__":
    listofnames = readNames()
    createOutputPage(searchForTPC(listofnames))
